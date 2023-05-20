# # -*- coding: utf-8 -*-


# db.executesql("""
#     CREATE TABLE public.rooms (
#         code varchar(255) NOT NULL PRIMARY KEY
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
#         start_time TIME NOT NULL DEFAULT '00:00:00',
#         end_time TIME NOT NULL DEFAULT '00:00:00',
#         room_code VARCHAR NOT NULL REFERENCES rooms(code),
#         prereq_code VARCHAR
#     );
# """)

# db.executesql("""
#         CREATE TABLE IF NOT EXISTS public.students_reg (
#             id SERIAL PRIMARY KEY,
#             student_id INTEGER NOT NULL REFERENCES auth_user(id),
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
    Field('start_time', 'time', notnull=True, default='00:00:00'),
    Field('end_time', 'time', notnull=True, default='00:00:00'),
    Field('room_code', 'string', length=255, notnull=True, requires=IS_IN_DB(db, 'rooms.code')),
    Field('prereq_code', 'string', length=20, requires=IS_IN_DB(db,'courses.code'))
)

db.define_table('students_reg',
    Field('id', 'id', readable=False, primarykey = True),
    Field('student_id', 'reference auth_user', notnull=True),
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

db.define_table('auth_event',
    Field('id', 'integer'),
    Field('time_stamp', 'datetime'),
    Field('client_ip', 'string', length=512),
    Field('user_id', 'integer'),
    Field('origin', 'string', length=512),
    Field('description', 'text')
)
