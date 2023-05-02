import json

def show_student_by_id():
    student_id = request.vars.id

    if student_id is None:
        response.status=400
        return response.json({"error": "Invalid student ID."})

    try:
        student_id = int(student_id)
    except ValueError:
        response.status=400
        return response.json({"error": "Invalid student ID."})

    student = get_student_by_id(student_id)

    if student is None:
        response.status=404
        return response.json({"error": "Student not found."})
    response.status=200
    return response.json({"student": student.as_dict()})


def show_students():
    students = get_students()
    if not students:
        response.status = 500
        return {'error': 'Internal error, no students retrieved.'}
    response.status = 200
    return students


def show_student_by_registration_key():
    
    registration_key = request.vars.registration_key

    if registration_key is None:
        response.status = 400
        return response.json({"error": "Invalid registration key."})

    try:
        registration_key = str(registration_key)
    except ValueError:
        response.status = 400
        return response.json({"error": "Invalid registration key."})

    student = get_student_by_registration_key(registration_key)

    if student is None:
        response.status = 404
        return response.json({"error": "Student not found."})
    
    response.status = 200
    return response.json({"student": student.as_dict()})

def create_student():
    first_name = request.vars.first_name
    last_name = request.vars.last_name
    email = request.vars.email
    password = request.vars.password
    registration_key = request.vars.registration_key
    reset_password_key = request.vars.reset_password_key
    registraion_id = request.vars.registraion_id
    
    if not all([first_name, last_name, email, password, registration_key, reset_password_key, registraion_id]):
        response.status = 400
        return response.json({"error": "Missing required fields."})
    
    new_student = db.students.insert(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        registration_key=registration_key,
        reset_password_key=reset_password_key,
        registraion_id=registraion_id
    )
    
    response.status = 200
    return response.json({"success": True, "student_id": new_student})

def update_student():
    student_id = request.vars.id
    if not student_id:
        return response.json({"error": "Missing student ID."}, status=400)
    
    student = db.students(student_id)
    if not student:
        return response.json({"error": "Student not found."}, status=404)
    
    first_name = request.vars.first_name
    last_name = request.vars.last_name
    email = request.vars.email
    password = request.vars.password
    registration_key = request.vars.registration_key
    
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
    
    return response.json({"success": True})

