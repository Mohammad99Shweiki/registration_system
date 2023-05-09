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


def show_all_courses():
    courses = get_all_courses()
    return response.render('courses/show_all_courses.html', dict(courses=courses))


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
        try:
            course_code = create_course(code, name, description, instructor, capacity, days, start_time, end_time, room_code)
        except psycopg2.Error as e:
                if e.pgcode == 23505:
                    session.flash = 'course code provided already exists'
                redirect(URL(show_all_courses))
        except CoursesTimesConflict as time_conflict:
            session.flash = 'there is an overlap between the course you are trying to add and another course in the system' + str(time_conflict)
            redirect(URL(add_course))
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
        Field('startTime', 'time'),
        Field('endTime', 'time'),
        Field('room_code'),
        submit_button='Update Course'
    )

    if form.process().accepted:
        data = {}
        for key, value in form.vars.items():
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
        submit_button='Update Course'
    )
    if form.process().accepted:
        data = {}
        for key, value in form.vars.items():
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
