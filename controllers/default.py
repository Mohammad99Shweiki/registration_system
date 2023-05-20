# -*- coding: utf-8 -*-

import datetime

def index():
    response.flash = 'Welcome to PPU Registration Platform!'
    response.title = 'PPU Registration System'
    return response.render('home.html')

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)


from gluon.tools import Auth
auth = Auth(db)

def row_count():
    return db(db.auth_user.id > 0).count() + 1

def get_current_year():
    return datetime.date.today().year

def register():
    if request.method == 'POST':
        first_name = request.vars.first_name
        last_name = request.vars.last_name
        email = request.vars.email
        password = request.vars.password
        encrypted_password = CRYPT()(password)[0] # encrypt the password using the CRYPT() function
        # registration_key = str(get_current_year()) + str(row_count())
        # reset_password_key = registration_key
        # registration_id = reset_password_key
        
        db.auth_user.insert(first_name=first_name, last_name=last_name, email=email, password=encrypted_password,
                            # registration_key=registration_key, 
                            reset_password_key=reset_password_key,
                            registration_id=registration_id,)
        
        response.flash = 'Registration successful'
        redirect(URL('default', 'login'))
    else:
        response.flash = 'Please fill the form'
        
    return dict()



def login():
    if request.method == 'POST':
        email = request.vars.email
        password = request.vars.password
        user = db(db.auth_user.email == email).select().first()
        encrypted_password = CRYPT()(password)[0]
        if user and encrypted_password == user.password:
            auth.login_user(user)
            redirect(URL('default', 'index'))
        else:
            response.flash = 'Invalid login'
            redirect(URL('default', 'login'))
    return dict()


def logout():
    auth = Auth(db)
    auth.logout()
    redirect(URL('default', 'index'))
    
def admin_panel():
    try:
        courses = db.executesql('SELECT name, registered FROM courses ORDER BY registered DESC', as_dict = True)
        most_reg_course = db.executesql('SELECT * FROM courses WHERE registered = (SELECT MAX(registered) FROM courses)', as_dict = True)[0]
    except:
        most_reg_course = None
        courses = None
    try:
        total_students = db.executesql('SELECT count(*) FROM auth_user')[0][0]
    except:
        total_students = None
    return response.render('admin.html', dict(courses=courses, most_reg_course=most_reg_course, total_students=total_students))

from datetime import datetime, timedelta

def schedule_notification():
    # notification_time = datetime.now() + timedelta(minutes=1)
    # notification_message = request.vars.message
    # print('message')
    # scheduler.queue_task(notification_message, 
                        #   scheduled_time=notification_time,
                        #   repeats=0)
    session.flash = 'notifications sent successfully'
    redirect(URL('default', 'admin_panel'))
    
    
def student_dashboard():
    student_id = auth.user.id 
    courses = get_courses_by_student(student_id)
    print(courses)
    return response.render('student.html', dict(courses = courses))

    
