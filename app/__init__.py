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

import routes as rs

app.add_route("/teacher/{teacherid}/", rs.Teacher())
app.add_route("/teacher/{teacherid}/students/today", rs.StudentsWithTeacherToday())
