
CoursesTimesConflict = type('MyException', (Exception,), {})

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