import falcon
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine("sqlite:///pden.db")
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = falcon.API()

import models
import routes as rs

app.add_route("/students/", rs.Students())
app.add_route("/student/{studentid}/", rs.Student())

app.add_route("/teachers/", rs.Teachers())
app.add_route("/teacher/{teacherid}/", rs.Teacher())
app.add_route("/teacher/{teacherid}/students/homeroom/", rs.TeacherStudentsHomeroom())
app.add_route("/teacher/{teacherid}/students/today/", rs.TeacherStudentsToday())

app.add_route("/schedules/", rs.Schedules())
app.add_route("/schedules/today", rs.SchedulesToday())
