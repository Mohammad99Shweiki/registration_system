# # -*- coding: utf-8 -*-


# db.executesql("""
#     CREATE TABLE public.rooms (
#         code varchar(255) NOT NULL PRIMARY KEY
#     );
# """)

# db.executesql("""
#     CREATE TABLE public.students (
#         id SERIAL PRIMARY KEY,
#         first_name VARCHAR(255) NOT NULL,
#         last_name VARCHAR(255) NOT NULL,
#         email VARCHAR(255) NOT NULL,
#         password VARCHAR(255) NOT NULL,
#         registration_key VARCHAR(255) NOT NULL,
#         reset_password_key VARCHAR(255) NOT NULL,
#         registraion_id VARCHAR(255) NOT NULL
#     );
# """)

# db.executesql("""
#     CREATE TABLE public.courses (
#         code VARCHAR PRIMARY KEY NOT NULL,
#         name VARCHAR,
#         description VARCHAR,
#         instructor VARCHAR,
#         capacity INTEGER,
#         registered INTEGER,
#         days VARCHAR NOT NULL,
#         startTime TIME NOT NULL DEFAULT '00:00:00',
#         endTime TIME NOT NULL DEFAULT '00:00:00',
#         room_code VARCHAR NOT NULL REFERENCES rooms(code),
#         prereq_code VARCHAR
#     );
# """)

# db.executesql("""
#         CREATE TABLE IF NOT EXISTS public.students_reg (
#             id SERIAL PRIMARY KEY,
#             student_id INTEGER NOT NULL REFERENCES students(id),
#             course_code VARCHAR NOT NULL REFERENCES courses(code)
#         );
# """)

db.define_table('rooms',
    Field('code', 'string', length=255, notnull=True, unique=True, primarykey=True)
)

db.define_table('auth_user',
    Field('id', 'integer', readable=False, primarykey = True),
    Field('first_name', 'string', length=255, notnull=True),
    Field('last_name', 'string', length=255, notnull=True),
    Field('email', 'string', length=255, notnull=True),
    Field('password', 'string', length=255, notnull=True),
    Field('registration_key', 'string', length=255, notnull=True),
    Field('reset_password_key', 'string', length=255, notnull=True),
    Field('registration_id', 'string', length=255, notnull=True)
)

db.define_table('courses',
    Field('code', 'string', length=255, unique=True, notnull=True, primarykey=True),
    Field('name', 'string', length=255),
    Field('description', 'string', length=255),
    Field('instructor', 'string', length=255),
    Field('capacity', 'integer'),
    Field('registered', 'integer'),
    Field('days', 'string', length=255, notnull=True),
    Field('startTime', 'time', notnull=True, default='00:00:00'),
    Field('endTime', 'time', notnull=True, default='00:00:00'),
    Field('room_code', 'string', length=255, notnull=True, requires=IS_IN_DB(db, 'rooms.code')),
    Field('prereq_code', 'string', length=20, requires=IS_IN_DB(db,'courses.code'))
)

db.define_table('students_reg',
    Field('id', 'id', readable=False, primarykey = True),
    Field('student_id', 'reference students', notnull=True),
    Field('course_code', 'reference courses', notnull=True)
)

db.define_table('auth_group',
    Field('id', 'id', readable=False, primarykey = True),
    Field('role', length=512, notnull=True, unique=True),
    Field('description', 'text')
)

db.define_table('auth_membership',
    Field('id', 'id', readable = False, primarykey = True),
    Field('user_id', 'reference auth_user', requires=IS_IN_DB(db, 'auth_user.id',)),
    Field('group_id', 'reference auth_group', requires=IS_IN_DB(db, 'auth_group.id'))
)



