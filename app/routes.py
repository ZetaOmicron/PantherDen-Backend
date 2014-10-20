import json
import datetime

import falcon
import models as ms
from app import session as sess


class Student():

    def on_get(self, req, resp, studentid):
        if not studentid.isdigit():
            resp.status = falcon.HTTP_404
            resp.body = "Invalid student id"
            return
        stid = int(studentid)
        student = sess.query(ms.Student).get(stid)
        if student is None:
            resp.status = falcon.HTTP_404
            resp.body = "A student with the id of %s was not found." % studentid
            return
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        resp.body = json.dumps(student.to_dict())


class Students():

    def on_get(self, req, resp):
        students = sess.query(ms.Student).all()
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        resp.body = json.dumps([student.to_dict() for student in students])


class Teacher():

    def on_get(self, req, resp, teacherid):
        teacher = sess.query(ms.Teacher).get(teacherid)
        if teacher is None:
            resp.status = falcon.HTTP_404
            resp.body = "A teacher with the id of %s was not found." % teacherid
            return
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        resp.body = json.dumps(teacher.to_dict())


class Teachers():

    def on_get(self, req, resp):
        teachers = sess.query(ms.Teacher).all()
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        resp.body = json.dumps([teacher.to_dict() for teacher in teachers])


class TeacherStudentsHomeroom():

    def on_get(self, req, resp, teacherid):
        if not teacherid.isdigit():
            resp.status = falcon.HTTP_404
            resp.body = "Invalid teacher id"
            return
        tid = int(teacherid)
        teacher = sess.query(ms.Teacher).get(tid)
        if teacher is None:
            resp.status = falcon.HTTP_404
            resp.body = "A teacher with the idea of %s was not found." % teacherid
            return
        roomid = teacher.roomid
        students = sess.query(ms.Student).filter_by(homeroomid=roomid)
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        resp.body = json.dumps([student.to_dict() for student in students])


# I put my id in: I want to see what students are in my class today
#/<teachid>/
class TeacherStudentsToday():

    def on_get(self, req, resp, teacherid):
        if not teacherid.isdigit():
            resp.status = falcon.HTTP_404
            resp.body = "Invalid teacher id"
            return
        tid = int(teacherid)
        teacher = sess.query(ms.Teacher).get(tid)
        if teacher is None:
            resp.status = falcon.HTTP_404
            resp.body = "A teacher with the idea of %s was not found." % teacherid
            return
        roomid = teacher.roomid
        today = datetime.date.today()
        default = sess.query(ms.Student).filter_by(homeroomid=roomid)
        removedscheds = sess.query(ms.Schedule).filter_by(oldroomid=roomid, date=today)
        newscheds = sess.query(ms.Schedule).filter_by(newroomid=roomid, date=today)
        resp.body = "hello"


class Schedule():

    def on_get(self, req, resp, studentid, date):
        pass


class Schedules():

    def on_get(self, req, resp):
        schedules = sess.query(ms.Schedule).all()
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])


class SchedulesToday():

    def on_get(self, req, resp):
        today = datetime.datetime.today()
        schedules = sess.query(ms.Schedule).filter_by(date=today)
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])
