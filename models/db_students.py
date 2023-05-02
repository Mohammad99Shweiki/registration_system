

def get_students():
    students =  db(db.students).select()
    return dict(students = students)

def get_student_by_id(student_id):
    student = db(db.students.id == student_id).select().first()
    return student

def get_student_by_registration_key(registration_key):
    student = db(db.students.registration_key == registration_key).select().first()
    return student