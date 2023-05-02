

def get_students():
    students =  db(db.students).select()
    return dict(students = students)

def get_student_by_id(student_id):
    student = db(db.students.id == student_id).select().first()
    return student

def get_student_by_registration_key(registration_key):
    student = db(db.students.registration_key == registration_key).select().first()
    return student

def save_student(first_name, last_name, email, password, registration_key, reset_password_key, registraion_id):
    new_student = db.students.insert(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        registration_key=registration_key,
        reset_password_key=reset_password_key,
        registraion_id=registraion_id
    )
    
    return new_student


def edit_student(student, first_name, last_name, email, password, registration_key):
    if first_name:
        student.update_record(first_name=first_name)
    if last_name:
        student.update_record(last_name=last_name)
    if email:
        student.update_record(email=email)
    if password:
        student.update_record(password=password)
    if registration_key:
        student.update_record(registration_key=registration_key)

