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
        resp.body = json.dumps(student.to_dict())


class Students():

    def on_get(self, req, resp):
        students = sess.query(ms.Student).all()
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([student.to_dict() for student in students])


class StudentCompleteSearch():

    def on_get(self, req, resp):
        field = req.get_param("f")
        if not (field in ms.Student.completable):
            resp.status = falcon.HTTP_400
            resp.body = "Invalid Field"
            return
        mf = getattr(ms.Student, field)
        toq = req.get_param("q")
        if toq is None:
            resp.status = falcon.HTTP_400
            resp.body = "No Query Found"
            return
        page = req.get_param("p")
        page = int(page) if page else 1
        query = sess.query(ms.Student).filter(mf.like("%s%%" % toq))
        count = query.count()
        if (page-1)*10 > count:
            resp.status = falcon.HTTP_404
            resp.body = "Page not found"
            return
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"students": [student.to_dict() for student in
                                             query.order_by(mf).slice((page-1)*10, page*10).all()],
                                "page": page,
                                "amount": count})


class Teacher():

    def on_get(self, req, resp, teacherid):
        teacher = sess.query(ms.Teacher).get(teacherid)
        if teacher is None:
            resp.status = falcon.HTTP_404
            resp.body = "A teacher with the id of %s was not found." % teacherid
            return
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(teacher.to_dict())


class Teachers():

    def on_get(self, req, resp):
        teachers = sess.query(ms.Teacher).all()
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([teacher.to_dict() for teacher in teachers])


class TeacherStudentsHomeroom():

    def on_get(self, req, resp, teacherid):
        teacher = sess.query(ms.Teacher).get(teacherid)
        if teacher is None:
            resp.status = falcon.HTTP_404
            resp.body = "A teacher with the idea of %s was not found." % teacherid
            return
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([student.to_dict() for student in teacher.home_room_students])


# TODO Fix this... it's not working
class TeacherStudentsToday():

    def on_get(self, req, resp, teacherid):
        teacher = sess.query(ms.Teacher).get(teacherid)
        if teacher is None:
            resp.status = falcon.HTTP_404
            resp.body = "A teacher with the idea of %s was not found." % teacherid
            return
        today = datetime.date.today()
        default = teacher.home_room_students
        removedstudents = sess.query(ms.Schedule).filter(ms.Student.home_room_teacher_id == teacherid,
                                                         ms.Schedule.date == today)
        default = default.outerjoin(removedstudents)
        newstudents = sess.query(ms.Schedule).filter(ms.Schedule.teacher_id == teacherid,
                                                     ms.Schedule.date == today)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"moved": [student.to_dict() for student in removedstudents],
                                "default": [student.to_dict() for student in default],
                                "new": [student.to_dict() for student in newstudents]})


class TeacherCompleteSearch():

    def on_get(self, req, resp):
        field = req.get_param("f")
        if not (field in ms.Teacher.completable):
            resp.status = falcon.HTTP_400
            resp.body = "Invalid Field"
            return
        mf = getattr(ms.Teacher, field)
        toq = req.get_param("q")
        if toq is None:
            resp.status = falcon.HTTP_400
            resp.body = "No Query Found"
            return
        page = req.get_param("p")
        page = int(page) if page else 1
        query = sess.query(ms.Teacher).filter(mf.like("%s%%" % toq))
        count = query.count()
        if (page-1)*10 > count:
            resp.status = falcon.HTTP_404
            resp.body = "Page not found"
            return
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"teachers": [teacher.to_dict() for teacher in
                                             query.order_by(mf).slice((page-1)*10, page*10).all()],
                                "page": page,
                                "amount": count})


class Schedule():

    def on_get(self, req, resp, student_id, new_teacher_id, date):
        pass


class Schedules():

    def on_get(self, req, resp):
        schedules = sess.query(ms.Schedule).all()
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])


class SchedulesToday():

    def on_get(self, req, resp):
        today = datetime.datetime.today()
        schedules = sess.query(ms.Schedule).filter_by(date=today)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])


class SchedulesOnDate():

    def on_get(self, req, resp, date):
        schedules = sess.query(ms.Schedule).filter_by(date=datetime.datetime.strptime(date, "%m-%d-%y"))
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])


class SchedulesWithStudent():

    def on_get(self, req, resp, studentid):
        schedules = sess.query(ms.Schedule).filter_by(student_id=studentid)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])

class SchedulesWithHomeRoomTeacher():

    def on_get(self, req, resp, studentid):
        schedules = sess.query(ms.Schedule).filter_by(student_id=studentid)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])

