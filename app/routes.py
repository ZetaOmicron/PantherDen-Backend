import json
import datetime

import falcon
import models as ms
from app import session


class Teacher():

    def on_get(self, req, resp, teacherid):
        if not teacherid.isdigit():
            resp.status = falcon.HTTP_404
            resp.body = "Invalid teacher id"
            return
        tid = int(teacherid)
        teacher = session.query(ms.Teacher).get(tid)
        if teacher is None:
            resp.status = falcon.HTTP_404
            resp.body = "A teacher with the idea of %s was not found." % teacherid
            return
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        resp.body = json.dumps(teacher.to_dict())


class Teachers():

    def on_get(self, req, resp):
        teachers = session.query(ms.Teacher).all()
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        #resp.body = json.dumps({[teacher.to_dict() for teacher in teachers]})
        resp.body = json.dumps([teacher.to_dict() for teacher in teachers])


# I put my id in: I want to see what students are in my class today
#/<teachid>/
class StudentsWithTeacherToday:

    def on_get(self, req, resp, teacherid):
        if not teacherid.isdigit():
            resp.status = falcon.HTTP_404
            resp.body = "Invalid teacher id"
            return
        tid = int(teacherid)
        teacher = session.query(ms.Teacher).get(tid)
        if teacher is None:
            resp.status = falcon.HTTP_404
            resp.body = "A teacher with the idea of %s was not found." % teacherid
            return
        roomid = teacher.roomid
        today = datetime.date.today()
        default = session.query(ms.Student).filter_by(homeroomid=roomid)
        removedscheds = session.query(ms.Schedule).filter_by(oldroomid=roomid, date=today)
        newscheds = session.query(ms.Schedule).filter_by(newroomid=roomid, date=today)
        resp["body"] = "hello"


