import falcon
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import *

engine = sqlalchemy.create_engine(test_database_string if test_run else database_string)
Base = declarative_base()

import models

if test_run:
    models.drop_metadata(engine)

models.create_metadata(engine)

Session = sessionmaker(bind=engine)
session = Session()

if test_run:
    from test_data import students, teachers, schedules
    session.add_all(students)
    session.add_all(teachers)
    session.add_all(schedules)
    session.commit()

import hooks as hs

app = falcon.API(media_type="application/json", before=[hs.set_access_origin])

import routes as rs

app.add_route("/students/", rs.Students())
app.add_route("/student/{studentid}/", rs.Student())
app.add_route("/student/search/", rs.StudentCompleteSearch())

app.add_route("/teachers/", rs.Teachers())
app.add_route("/teacher/{teacherid}/", rs.Teacher())
app.add_route("/teacher/{teacherid}/students/homeroom/", rs.TeacherStudentsHomeroom())
app.add_route("/teacher/{teacherid}/students/{year}/{month}/{day}/", rs.TeacherStudentsOnDate())
app.add_route("/teacher/{teacherid}/students/today/", rs.TeacherStudentsToday())
app.add_route("/teacher/search/", rs.TeacherCompleteSearch())
app.add_route("/teacher/register/", rs.TeacherRegister())

app.add_route("/schedules/", rs.Schedules())
app.add_route("/schedules/today/", rs.SchedulesToday())
app.add_route("/schedules/date/{year}/", rs.SchedulesInYear())
app.add_route("/schedules/date/{year}/{month}/", rs.SchedulesInMonth())
app.add_route("/schedules/date/{year}/{month}/{day}/", rs.SchedulesOnDay())
app.add_route("/schedules/student/{studentid}/", rs.SchedulesWithStudent())
app.add_route("/schedules/teacher/{teacherid}/homeroom/", rs.SchedulesWithHomeRoomTeacher())
app.add_route("/schedules/teacher/{teacherid}/newroom/", rs.SchedulesWithNewTeacher())
