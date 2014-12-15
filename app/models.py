from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app import Base


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    home_room_teacher_id = Column(String(30), ForeignKey("teacher.id"))

    schedules = relationship("Schedule", backref="student")

    completable = ["first_name", "last_name"]

    def __init__(self, id, first_name, last_name, home_room_teacher_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.home_room_teacher_id = home_room_teacher_id

    def to_dict(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "home_room_teacher_id": self.home_room_teacher_id}

    def __repr__(self):
        return "<Student %r>" % self.id


class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(String(30), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    room_id = Column(String(6))

    home_room_students = relationship("Student", backref="teacher")
    schedules = relationship("Schedule", backref="teacher")

    completable = ["first_name", "last_name"]

    def __init__(self, id, first_name, last_name, room_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.room_id = room_id

    def to_dict(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "room_id": self.room_id}

    def __repr__(self):
        return "<Teacher %r>" % self.id


class Schedule(Base):
    __tablename__ = "schedule"

    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
    teacher_id = Column(String(30), ForeignKey("teacher.id"), primary_key=True)
    date = Column(Date, primary_key=True)
    absent = Column(Boolean)

    def __init__(self, student_id, teacher_id, date):
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.date = date
        self.absent = False

    def to_dict(self):
        return {"student_id": self.student_id,
                "teacher_id": self.teacher_id,
                "date": str(self.date),
                "absent": self.absent}

    def __repr__(self):
        return "<Schedule %r, %r, %r>" % self.student_id, self.teacher_id, self.date


def create_metadata(engine):
    Base.metadata.create_all(engine)


def drop_metadata(engine):
    Base.metadata.drop_all(engine)