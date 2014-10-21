from sqlalchemy import Column, Integer, String, Date
from app import Base, engine


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    homeroomid = Column(Integer)

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
    roomid = Column(Integer)

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
    newroomid = Column(Integer)
    homeroomid = Column(Integer)

    def __init__(self, studentid, date, newroomid, homeroomid):
        self.studentid = studentid
        self.date = date
        self.newroomid = newroomid
        self.homeroomid = homeroomid

    def to_dict(self):
        return {"studentid": self.studentid,
                "date": self.date,
                "newroomid": self.newroomid,
                "homeroomid": self.homeroomid}

    def __repr__(self):
        return "<Schedule %r, %r>" % self.studentid, self.date

Base.metadata.create_all(engine)
