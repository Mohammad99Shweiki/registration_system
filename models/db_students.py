
def get_students():
    students =  db(db.auth_user).select()
    return dict(students = students)

def get_student_by_id(student_id):
    student = db(db.auth_user.id == student_id).select().first()
    return student

def save_student(first_name, last_name, email, password, registration_key, reset_password_key, registration_id):
    new_student = db.auth_user.insert(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        registration_key=registration_key,
        reset_password_key=reset_password_key,
        registration_id=registration_id
    )
    
    return new_student


def update_student_by_id(id, **data):
    query = 'UPDATE auth_user SET '
    values = []
    for key, value in data.items():
        query += f"{key}=%s, "
        values.append(value)
    query = query.rstrip(', ') + ' WHERE id=%s'
    values.append(id)
    result = db.executesql(query, values)
    db.commit()
    return result

def delete_student_by_id(student_id):
    db(db.auth_user.id == student_id).delete()

def delete_all():
    db(db.auth_user).delete()
