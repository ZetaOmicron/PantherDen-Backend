from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app import Base


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    home_room_teacher_id = Column(String(30), ForeignKey("teacher.id"))
    inactive = Column(Boolean())

    schedules = relationship("Schedule", backref="student")
    absences = relationship("Absence", backref="student")

    completable = ["first_name", "last_name", "id"]

    def __init__(self, id, first_name, last_name, home_room_teacher_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.home_room_teacher_id = home_room_teacher_id
        self.inactive = False

    def to_dict(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "home_room_teacher_id": self.home_room_teacher_id,
                "inactive": self.inactive}

    def __repr__(self):
        return "<Student %r>" % self.id


class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(String(30), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    room_id = Column(String(6))
    data_manager = Column(Boolean())

    home_room_students = relationship("Student", backref="teacher")
    schedules = relationship("Schedule", backref="teacher")

    completable = ["first_name", "last_name", "id"]

    def __init__(self, id, first_name, last_name, room_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.room_id = room_id
        self.data_manager = False

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
    comment = Column(String(256))

    def __init__(self, student_id, teacher_id, date, comment="(NONE)"):
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.date = date
        self.comment = comment

    def to_dict(self):
        return {"student_id": self.student_id,
                "teacher_id": self.teacher_id,
                "date": str(self.date),
                "comment": self.comment}

    def __repr__(self):
        return "<Schedule %r, %r, %r>" % self.student_id, self.teacher_id, self.date


class Absence(Base):
    __tablename__ = "absence"

    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
    date = Column(Date, primary_key=True)

    def __init__(self, student_id, date):
        self.student_id = student_id
        self.date = date

    def to_dict(self):
        return {"student_id": self.student_id,
                "date": str(self.date)}

    def __repr__(self):
        return "<Absence %r, %r>" % self.student_id, self.date


def create_metadata(engine):
    Base.metadata.create_all(engine)


def drop_metadata(engine):
    Base.metadata.drop_all(engine)