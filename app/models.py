from sqlalchemy import Column, Integer, String, Date
from app import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    homeroomid = Column(String(6))

    completable = ["firstname", "lastname"]

    def __init__(self, id, firstname, lastname, homeroomid):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.homeroomid = homeroomid

    def to_dict(self):
        return {"id": self.id,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "homeroomid": self.homeroomid}

    def __repr__(self):
        return "<Student %r>" % self.id


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(String(30), primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    roomid = Column(String(6))

    completable = ["firstname", "lastname"]

    def __init__(self, id, firstname, lastname, roomid):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.roomid = roomid

    def to_dict(self):
        return {"id": self.id,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "roomid": self.roomid}

    def __repr__(self):
        return "<Teacher %r>" % self.id


class Schedule(Base):
    __tablename__ = "schedules"

    studentid = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)
    newroomid = Column(String(6), primary_key=True)
    homeroomid = Column(String(6))

    def __init__(self, studentid, date, newroomid, homeroomid):
        self.studentid = studentid
        self.date = date
        self.newroomid = newroomid
        self.homeroomid = homeroomid

    def to_dict(self):
        return {"studentid": self.studentid,
                "date": str(self.date),
                "newroomid": self.newroomid,
                "homeroomid": self.homeroomid}

    def __repr__(self):
        return "<Schedule %r, %r>" % self.studentid, self.date


def create_metadata(engine):
    Base.metadata.create_all(engine)


def drop_metadata(engine):
    Base.metadata.drop_all(engine)