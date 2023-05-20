import psycopg2

def find_course_by_code():
    code = request.vars.code
    if code is None:
        response.flash = 'Course code required to perform search.'
        redirect(URL('show_all_courses'))
        
    code = str(code)
    course = get_course_by_code(code)
    if course:
        form = SQLFORM.factory(
            Field('name', default=course['name']),
            Field('description', default=course['description']),
            Field('instructor', default=course['instructor']),
            Field('capacity', 'integer', default=course['capacity']),
            Field('registered', default=course['registered']),
            Field('days', default=course['days']),
            Field('startTime', 'time',rname="start time", default=course['start_time']),
            Field('endTime', 'time', rname = "end time", default=course['end_time']),
            Field('room_code', default=course['room_code']),
            Field('prerequisite_name', default=course['prerequisite_name']),
            
            readonly=True
        )
        form.vars = course
        return dict(form=form)
    else:
        response.flash = 'course with code = ' + str(code) + ' was not found in database'
        redirect(URL('show_all_courses'))



def find_course_by_name():
    name = request.vars.name
    if name is None:
        esponse.flash = 'Course name required to perform search.'
        redirect(URL('show_all_courses'))
    name = str(name)
    course = get_course_by_name(name)
    if course is not None:
        form = SQLFORM.factory(
            Field('name', default=course['name']),
            Field('description', default=course['description']),
            Field('instructor', default=course['instructor']),
            Field('capacity', 'integer', default=course['capacity']),
            Field('registered', 'integer', default=course['registered']),
            Field('days', default=course['days']),
            Field('startTime', 'time', default=course['start_time']),
            Field('endTime', 'time', default=course['end_time']),
            Field('room_code', default=course['room_code']),
            Field('prerequisite_name', default=course['prerequisite_name']),
            readonly=True
        )
        form.vars = course
        return dict(form=form)
    else:
        response.flash = 'course with name = ' + str(name) + ' was not found in database'
        redirect(URL('show_all_courses'))


def check_access():
    user_id = auth.user.id
    return user_id == 27


def show_all_courses():
    if check_access():
        courses = get_all_courses()
        return response.render('courses/show_all_courses.html', dict(courses=courses))
    else:
        session.flash = 'only accessible by admin'
        return response.render('default/index.html')


def add_course():
    form = SQLFORM.factory(
        Field('code', requires=IS_NOT_EMPTY()),
        Field('name', requires=IS_NOT_EMPTY()),
        Field('description'),
        Field('instructor', requires=IS_NOT_EMPTY()),
        Field('capacity', 'integer', requires=IS_NOT_EMPTY()),
        Field('days', requires=IS_NOT_EMPTY()),
        Field('start_time', 'time', requires=IS_NOT_EMPTY()),
        Field('end_time', 'time', requires=IS_NOT_EMPTY()),
        Field('room_code', requires=IS_NOT_EMPTY()),
        # Field('prerequisite_code'),
        submit_button='Add Course'
    )
    if form.process().accepted:
        code = form.vars.code
        name = form.vars.name
        description = form.vars.description
        instructor = form.vars.instructor
        capacity = form.vars.capacity
        days = form.vars.days
        start_time = form.vars.start_time
        end_time = form.vars.end_time
        room_code = form.vars.room_code
        # prereq_code = form.vars.prerequisite_code
        
        try:
            course_code = create_course(code, name, description, instructor, capacity, days, start_time, end_time, room_code)
        except psycopg2.Error as e:
                if e.pgcode == 23505:
                    session.flash = 'course code provided already exists'
                redirect(URL(show_all_courses))
        except CoursesTimesConflict as time_conflict:
            session.flash = 'there is an overlap between the course you are trying to add and another course in the system' + str(time_conflict)
            redirect(URL(add_course))
        print(course_code)
        session.flash = 'Course added successfully!'
        redirect(URL(show_all_courses))
    return dict(form=form)

def update_by_code():
    course_code = str(request.vars.code)
    if course_code is None:
        return 'course code is not provided'
    course = get_course_by_code(course_code)
    if course is None:
        session.flash = 'Course not found!'
        redirect(URL('show_all_courses'))

    
    form = SQLFORM.factory(
        Field('name'),
        Field('description'),
        Field('instructor'),
        Field('capacity', 'integer'),
        Field('registered', 'integer'),
        Field('days'),
        Field('start_time', 'time'),
        Field('end_time', 'time'),
        Field('room_code'),
        Field('prerequisite_code'),
        submit_button='Update Course'
    )

    if form.process().accepted:
        data = {}
        for key, value in form.vars.items():
            if key == 'prerequisite_code' and value is not None:
                data['prereq_code'] = value
                continue
            if value is not None:
                data[key] = value
        try:        
            update_course_by_code(course_code, **data)
        except CoursesTimesConflict as time_conflict:
            session.flash = 'there is an overlap between the course you are trying to update and another course in the system' + str(time_conflict)
            redirect(URL(add_course))
        session.flash = 'Course updated successfully!'
        redirect(URL(show_all_courses))
    return dict(form=form)


def update_by_name():
    course_name = str(request.vars.name)
    if course_name is None:
        session.flash = 'Course name not provided!'
        redirect(URL('show_all_courses'))
        
    course = get_course_by_name(course_name)
    if course is None:
        session.flash = 'Course not found!'
        redirect(URL('show_all_courses'))
    
    form = SQLFORM.factory(
        Field('code'),
        Field('description'),
        Field('instructor'),
        Field('capacity', 'integer'),
        Field('registered', 'integer'),
        Field('days'),
        Field('startTime', 'time'),
        Field('endTime', 'time'),
        Field('room_code'),
        Field('prerequisite_code'),
        submit_button='Update Course'
    )
    if form.process().accepted:
        data = {}
        for key, value in form.vars.items():
            if key == 'prerequisite_code' and value is not None:
                data['prereq_code'] = value
            if value is not None:
                data[key] = value
        try:
            update_course_by_name(course_name, **data)
        except psycopg2.Error as e:
                if e.pgcode == 23505:
                    session.flash = 'new course code provided already exists'
                redirect(URL(show_all_courses))
        except CoursesTimesConflict as time_conflict:
            session.flash = 'there is an overlap between the course you are trying to update and another course in the system' + str(time_conflict)
            redirect(URL(add_course))
        session.flash = 'Course updated successfully!'
        redirect(URL(show_all_courses))
    return dict(form=form)

def delete_by_code():
    course_code = request.vars.code
    if not course_code:
        session.flash = 'Missing course code.'
        redirect(URL('show_all_courses'))


    course = get_course_by_code(course_code)
    if not course:
        session.flash = 'Course not found.'
        redirect(URL('show_all_courses'))

    delete_course_by_code(course_code)

    session.flash = 'Course deleted successfully.'
    redirect(URL('show_all_courses'))



def delete_by_name():
  course_name = request.vars.name
  if not course_name:
        session.flash = 'Missing course name.'
        redirect(URL('show_all_courses'))


  course = get_course_by_code(course_name)
  if not course:
        session.flash = 'Course not found.'
        redirect(URL('show_all_courses'))


  delete_course_by_name(course_name)

  session.flash = 'Course deleted successfully.'
  redirect(URL('show_all_courses'))

def delete_all():
    deleted = delete_all_courses()
    if deleted:
        session.flash = 'All Courses deleted successfully.'
    else:
        session.flash = 'Something went wrong while trying to delete All courses'
    redirect(URL('show_all_courses'))

def register_courses():
    student_id = auth.user.id
    courses = get_all_courses()
    return response.render('courses/register_courses.html', dict(courses=courses, student_id = student_id))
    
def register_course():
    course = str(request.vars.course_code)
    student = auth.user.id
    if check_if_registered(course,student):
        session.flash = 'course already passed'
    elif not check_avaliable(course, student):
        session.flash = 'there is a course in your schedule at this course time'
    elif not check_course_capacity(course):
        session.flash = 'the course capacity is fulfilled cant receive more students currently'
    elif not check_course_prerequisite(course, student):
        session.flash = 'you must pass courses\' prerequisite to register it'
    elif register_course_for_student(course, student):
        session.flash = 'course registered successfully'
    else:
        session.flash = 'error occured while trying to register course'
    redirect(URL('register_courses'))
    
    
def student_schedule():
    student_id = auth.user.id
    courses = get_courses_by_student(student_id)
    student = get_student_by_id(student_id)
    student_name = student['first_name'] + ' ' + student['last_name']
    response.title = 'Courses Schedule'
    return response.render('courses/courses_schedule.html', dict(courses=courses, student_name = student_name))

def delete_from_schedule():
    student_id = auth.user.id
    course_code = request.vars.course_code
    try:
        delete_course_from_student_schedule(course_code, student_id)
    except Exception as e:
        session.flash = 'error occured in database'
        redirect(URL('student_schedule'))
    session.flash = 'course deleted from your schedule successfully'
    redirect(URL('student_schedule'))
    
def course_description():
    code = request.vars.code
    course = get_course_by_code(code)
    try:
        session.flash = str(course['description'])
    except Exception as e:
        session.flash = 'no description provided for the course at the moment'
    redirect(URL('student_schedule'))


def get_courses_by_student(student_id):
    return db.executesql(f'''
                        SELECT * FROM courses
                            JOIN students_reg ON courses.code = students_reg.course_code
                            WHERE students_reg.student_id = {student_id}
    ''', as_dict = True)