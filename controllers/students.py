import datetime

def row_count():
    return db(db.auth_user.id > 0).count() + 1

def get_current_year():
    return datetime.date.today().year

def show_student_by_id():
    id = request.vars.id
    if id is None:
        response.flash = 'student id required to perform search.'
        redirect(URL('show_students'))
        
    id = int(id)
    student = get_student_by_id(id)
    if student:
        form = SQLFORM.factory(
            Field('id', default=student['id']),
            Field('first_name', default=student['first_name']),
            Field('last_name', default=student['last_name']),
            Field('email', default=student['email']),
            Field('registration_key', default=student['registration_key']),
            Field('reset_password_key', default=student['reset_password_key']),
            Field('registration_id', default=student['registration_id']),
            readonly=True
        )
        form.vars = student
        return dict(form=form)
    else:
        response.flash = 'student with id = ' + str(id) + ' was not found in database'
        redirect(URL('show_tudents'))

def show_students():
    students = get_students()
    return response.render('students/show_all_students.html', students)

def create_student():
    form = SQLFORM.factory(
        Field('first_name', requires=IS_NOT_EMPTY()),
        Field('last_name', requires=IS_NOT_EMPTY()),
        Field('email', requires=IS_NOT_EMPTY()),
        Field('password', requires=IS_NOT_EMPTY()),
        submit_button='Add Student'
    )
    if form.process().accepted:
        first_name = form.vars.first_name
        last_name = form.vars.last_name
        email = form.vars.email
        password = form.vars.instructor
        registration_key = str(get_current_year()) + str(row_count())
        reset_password_key = registration_key
        registration_id = registration_key
        student = save_student(first_name, last_name, email, password, registration_key, reset_password_key, registration_id)
        session.flash = 'Student added successfully!'
        redirect(URL(show_students))
    return dict(form=form)

def update_student():
    student_id = int(request.vars.id)
    if student_id is None:
        return 'student id is not provided'
    student = get_student_by_id(student_id)
    if student is None:
        session.flash = 'Student not found!'
        redirect(URL('show_students'))

    
    form = SQLFORM.factory(
            Field('id'),
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Field('registration_key'),
            Field('reset_password_key'),
            Field('registration_id'),
            submit_button = 'Update Student'
        )

    if form.process().accepted:
        data = {}
        for key, value in form.vars.items():
            if value is not None:
                data[key] = value
        update_student_by_id(student_id, **data)
        session.flash = 'Student updated successfully!'
        redirect(URL(show_students))
    return dict(form=form)


def delete_student():
    student_id = request.vars.id
    if not student_id:
        session.flash = 'Missing student id.'
        redirect(URL('show_students'))


    student = get_student_by_id(student_id)
    if not student:
        session.flash = 'Student not found.'
        redirect(URL('show_students'))

    delete_student_by_id(student_id)

    session.flash = 'Student deleted successfully.'
    redirect(URL('show_students'))

def delete_all_students():
    delete_all()
    session.flash = 'All Students deleted successfully.'
    return redirect(URL('show_students'))