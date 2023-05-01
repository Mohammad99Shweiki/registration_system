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
#     CREATE TABLE public.courses_schedules (
#         id SERIAL PRIMARY KEY,
#         days VARCHAR NOT NULL,
#         startTime TIME NOT NULL DEFAULT '00:00:00',
#         endTime TIME NOT NULL DEFAULT '00:00:00',
#         room_code VARCHAR NOT NULL REFERENCES rooms(code)
#     );
# """)

# db.executesql("""
#     CREATE TABLE public.courses (
#         code VARCHAR PRIMARY KEY NOT NULL,
#         name VARCHAR,
#         description VARCHAR,
#         instructor VARCHAR,
#         capacity INTEGER,
#         schedule_id INTEGER NOT NULL REFERENCES courses_schedules(id)
#     );
# """)

# db.executesql("""
#         CREATE TABLE IF NOT EXISTS public.students_reg (
#             id SERIAL PRIMARY KEY,
#             student_id INTEGER NOT NULL REFERENCES students(id),
#             course_code VARCHAR NOT NULL REFERENCES courses(code)
#         );
# """)

# db.executesql("""
#     CREATE TABLE IF NOT EXISTS public.prerequists (
#         id INTEGER PRIMARY KEY,
#         course_code VARCHAR NOT NULL REFERENCES courses(code),
#         prerequest_course_code VARCHAR NOT NULL REFERENCES courses(code)
#         );
# """)