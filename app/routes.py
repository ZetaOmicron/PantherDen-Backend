import json
import datetime

import falcon
import models as ms
from app import session as sess

from sqlalchemy.sql.expression import extract


# Students

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


class EditStudent():

    def on_put(self, req, resp):
        pass


class ScheduleStudent():

    def on_post(self, req, resp):
        body = req.stream.read()
        body = json.loads(body)
        stid = body["student_id"]
        tid = body["teacher_ID"]
        date = datetime.datetime.strptime(body["date"], "%Y-%m-%d").date()
        if sess.query(ms.Schedule).filter(student_id=stid, date=date).first() is None:
            resp.status = falcon.HTTP_409
            resp.body = "A schedule already exists on this date."
            return
        sess.add(ms.Schedule(stid, tid, date))
        sess.commit()
        resp.status = falcon.HTTP_200
        resp.body = "Successfully Schedule Student"


class RequestScheduleStudent():

    def on_post(self, req, resp):
        body = req.stream.read()
        body = json.loads(body)
        stid = body["student_id"]
        tid = body["teacher_id"]
        comment = body["comment"]
        if len(comment) > 256:
            resp.status = falcon.HTTP_500
            resp.body = "That comment is too long."
            return
        date = datetime.datetime.strptime(body["date"], "%Y-%m-%d").date()
        today = datetime.date.today()
        if (date-today).days < 2:
            resp.status = falcon.HTTP_409
            resp.body = "You have to schedule your students two days in advance."
            return
        if sess.query(ms.Schedule).filter(student_id=stid, date=date).first() is None:
            resp.status = falcon.HTTP_409
            resp.body = "A schedule already exists on this date."
            return
        sess.add(ms.Schedule(stid, tid, date, comment))
        sess.commit()
        resp.status = falcon.HTTP_200
        resp.body = "Successfully Schedule Student"


class UnscheduleStudent():

    def on_delete(self, req, resp):
        body = req.stream.read()
        body = json.loads(body)
        stid = body["student_id"]
        tid = body["teacher_ID"]
        date = datetime.datetime.strptime(body["date"], "%Y-%m-%d").date()
        schedule = sess.query(ms.Schedule).get(stid, tid, date)
        if schedule is None:
            resp.status = falcon.HTTP_400
            resp.body = "Student Not Found"
        sess.delete(schedule)
        sess.commit()
        resp.body = "Schedule Successfully Removed"


class StudentsAbsentToday():

    def on_post(self, req, resp):
        body = req.stream.read()
        body = json.loads(body)
        tid = body["teacher_id"]
        today = datetime.date.today()
        for stid in body["moved"]:
            sched = sess.query(ms.Schedule).get(int(stid), tid, today)
            sched.absent = True
        sess.commit()
        resp.status = falcon.HTTP_200
        resp.body = "Attendance Successfully Taken"


# Teachers

class TeacherRegister():

    def on_post(self, req, resp):
        body = req.stream.read()
        body = json.loads(body)
        if sess.query(ms.Teacher).get(body["id"]) is None:
            resp.status = falcon.HTTP_409
            resp.body = "That id is already taken"
            return
        teach = ms.Teacher(body["id"], body["first_name"], body["last_name"], body["room_id"])
        sess.add(teach)
        sess.commit()
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(teach.to_dict())


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


class TeacherStudentsToday():

    def on_get(self, req, resp, teacherid):
        teacher = sess.query(ms.Teacher).get(teacherid)
        if teacher is None:
            resp.status = falcon.HTTP_404
            resp.body = "A teacher with the idea of %s was not found." % teacherid
            return
        today = datetime.date.today()
        default = teacher.home_room_students
        removedstudents = sess.query(ms.Student).join(ms.Schedule).filter(ms.Student.home_room_teacher_id == teacherid,
                                                                          ms.Schedule.date == today)
        default = [e for e in default if e not in removedstudents]
        newstudents = sess.query(ms.Student).join(ms.Schedule).filter(ms.Schedule.teacher_id == teacherid,
                                                                      ms.Schedule.date == today)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"moved": [student.to_dict() for student in removedstudents],
                                "default": [student.to_dict() for student in default],
                                "new": [student.to_dict() for student in newstudents]})


class TeacherStudentsOnDate():

    def on_get(self, req, resp, teacherid, year, month, day):
        teacher = sess.query(ms.Teacher).get(teacherid)
        if teacher is None:
            resp.status = falcon.HTTP_404
            resp.body = "A teacher with the idea of %s was not found." % teacherid
            return
        date = datetime.date(year, month, day)
        default = teacher.home_room_students
        removedstudents = sess.query(ms.Student).join(ms.Schedule).filter(ms.Student.home_room_teacher_id == teacherid,
                                                                          ms.Schedule.date == date)
        default = [e for e in default if e not in removedstudents]
        newstudents = sess.query(ms.Student).join(ms.Schedule).filter(ms.Schedule.teacher_id == teacherid,
                                                                      ms.Schedule.date == date)
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


# Schedules

class Schedule():

    #TODO finish this
    def on_get(self, req, resp, student_id, new_teacher_id, date):
        pass


class Schedules():

    def on_get(self, req, resp):
        schedules = sess.query(ms.Schedule).all()
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])


class SchedulesToday():

    def on_get(self, req, resp):
        today = datetime.date.today()
        schedules = sess.query(ms.Schedule).filter_by(date=today)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])


class SchedulesInYear():

    def on_get(self, req, resp, year):
        schedules = sess.query(ms.Schedule).filter(extract("year", ms.Schedule.date) == year)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])


class SchedulesInMonth():

    def on_get(self, req, resp, year, month):
        schedules = sess.query(ms.Schedule).filter(extract("year", ms.Schedule.date) == year,
                                                   extract("month", ms.Schedule.date) == month)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])


class SchedulesOnDay():

    def on_get(self, req, resp, year, month, day):
        schedules = sess.query(ms.Schedule).filter_by(date=datetime.date(int(year), int(month), int(day)))
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])


class SchedulesInDateRange():

    def on_get(self, req, resp):
        qs = req.query_string
        # TODO FINISH THIS


class SchedulesWithStudent():

    def on_get(self, req, resp, studentid):
        schedules = sess.query(ms.Schedule).filter_by(student_id=studentid)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])


class SchedulesWithHomeRoomTeacher():

    def on_get(self, req, resp, teacherid):
        schedules = sess.query(ms.Schedule).join(ms.Student).filter_by(home_room_teacher_id=teacherid)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])


class SchedulesWithNewTeacher():

    def on_get(self, req, resp, teacherid):
        schedules = sess.query(ms.Schedule).filter_by(teacher_id=teacherid)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([schedule.to_dict() for schedule in schedules])
