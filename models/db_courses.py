
CoursesTimesConflict = type('MyException', (Exception,), {})

def get_student_by_id(student_id):
    student = db(db.auth_user.id == student_id).select().first()
    return student

def get_course_by_code(code):
    query = '''SELECT c.*, p.name AS prerequisite_name
            FROM courses c
            LEFT JOIN courses p
            ON c.prereq_code = p.code
            WHERE c.code = \'''' +  str(code) + str('\'')
    row = db.executesql(query, [code], as_dict=True)
    if row:
        return row[0]
    else:
        return None

def get_course_by_name(name):
    query = '''SELECT c.*, p.name AS prerequisite_name
            FROM courses c
            LEFT JOIN courses p
            ON c.prereq_code = p.code
            WHERE c.name = \'''' +  str(name) + str('\'')
    row = db.executesql(query, [name], as_dict=True)
    if row:
        return row[0]
    else:
        return None


def get_all_courses():
    courses = db.executesql('''SELECT c.code, c.name, c.instructor, c.description, c.capacity, c.registered, c.days, c.start_time, c.end_time, c.room_code, p.name AS prerequisite_name
        FROM courses c
        LEFT JOIN courses p ON c.prereq_code = p.code;
    ''', as_dict = True)
    return courses



def create_course(code, name, description, instructor, capacity, days, start_time, end_time, room_code):
    existing_courses_query = "SELECT code, start_time, end_time, days, room_code \
            FROM courses \
            WHERE days = \'" + str(days) + "\' AND start_time < '" + start_time + "' AND end_time > '" + end_time + "' AND room_code = '" + room_code + "' \
                AND ((start_time <= '" + end_time + "' AND end_time > '" + start_time + "') OR (start_time >= '" + start_time + "' AND end_time < '" + end_time + "') \
                OR (start_time >= '" + start_time + "' AND start_time < '" + end_time + "' AND end_time > '" + start_time + "') \
                OR (end_time >= '" + end_time + "' AND end_time > '" + start_time + "' AND start_time < '" + end_time + "'))"
    existing_courses = db.executesql(existing_courses_query, as_dict=True)
    if not existing_courses:
        query = "INSERT INTO courses (code, name, description, instructor, capacity, days, start_time, end_time, room_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        course = db.executesql(query, (code, name, description, instructor, capacity, days, start_time, end_time, room_code))
        db.commit()
        return course
    else:
        raise CoursesTimesConflict('can not add due to conflict in course time with other existsing course')


def update_course_by_code(code, **data):
    query = 'UPDATE courses SET '
    values = []
    for key, value in data.items():
        query += f"{key}=%s, "
        values.append(value)
    query = query.rstrip(', ') + ' WHERE code=%s'
    values.append(code)
    result = db.executesql(query, values)
    db.commit()
    return result



def update_course_by_name(name, **data):
    query = 'UPDATE courses SET '
    values = []
    for key, value in data.items():
        query += f"{key}=%s, "
        values.append(value)
    query = query.rstrip(', ') + ' WHERE name=%s'
    values.append(name)
    result = db.executesql(query, values)
    db.commit()
    return result


def delete_course_by_code(code):
    return db(db.courses.code==code).delete()

def delete_course_by_name(name):
    return db(db.courses.name==name).delete()

def delete_all_courses():
    return db(db.courses.code != '').delete()

def check_if_registered(course_code, student_id):
    query = '''
        SELECT COUNT(*) AS count
        FROM students_reg
        WHERE course_code = \''''+ str(course_code) +  '''\'  AND student_id = \'''' + str(student_id) + "\';"
    result = db.executesql(query)[0][0]
    return result > 0

def check_avaliable(course_code, student_id):
    course = get_course_by_code(course_code)
    query = """
        SELECT COUNT(*) FROM courses c
        JOIN students_reg sr ON sr.course_code = c.code
        WHERE sr.student_id = \'""" + str(student_id) + """\'
         AND (
            (c.start_time >= \'""" + str(course['start_time']) + """\' AND c.start_time <= \'""" + str(course['end_time']) + """\') 
            OR (c.end_time >= \'""" + str(course['start_time']) + """\' AND c.end_time <= \'""" + str(course['end_time']) +  """\')
        )
        """
    conflicts = db.executesql(query)[0][0]
    return conflicts == 0

def check_course_capacity(course_code):
    course = get_course_by_code(course_code)
    return course['registered'] < course['capacity']

def register_course_for_student(course, student):
    try:
        db.executesql('INSERT INTO students_reg (student_id, course_code) VALUES (%s, %s)', (student, course))
        db.executesql('UPDATE courses SET registered = registered + 1 WHERE code = %s', (course,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False
    
def get_courses_by_student(student_id):
    query = """
        SELECT c.* FROM courses c
        INNER JOIN students_reg sr ON sr.course_code = c.code
        WHERE sr.student_id = \' """ + str(student_id) + """\' 
    """
    courses = db.executesql(query, as_dict=True)
    return courses

def delete_course_from_student_schedule(course_code,student_id):
    query = f"""DELETE FROM students_reg
        WHERE student_id = \'{student_id}\'
        AND course_code = \'{course_code}\'
    """
    db.executesql(query)
    query = f"""UPDATE courses SET registered = registered - 1 WHERE code = \'{course_code}\';"""
    deleted = db.executesql(query)
    return deleted

def check_course_prerequisite(course_code, student_id):
    prerequisite = db.executesql(f"select prereq_code from courses where code = \'{course_code}\'",as_dict = True)
    if prerequisite[0]['prereq_code'] is None:
        return True
    print('second')
    prerequisite_code = prerequisite[0]['prereq_code']
    query = f"select count(*) from students_reg where course_code = \'{prerequisite_code}\' AND student_id = \'{student_id}\'"
    count = db.executesql(query)[0]
    return count == 0
    