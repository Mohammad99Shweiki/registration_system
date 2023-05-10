# -*- coding: utf-8 -*-

import datetime

def index():
    response.flash = 'Welcome to PPU Registration Platform!'
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
        registration_key = str(get_current_year()) + str(row_count())
        reset_password_key = registration_key
        registration_id = reset_password_key
        
        db.auth_user.insert(first_name=first_name, last_name=last_name, email=email, password=encrypted_password,
                            registration_key=registration_key, 
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
    auth.logout()
    redirect(URL('default', 'index'))
