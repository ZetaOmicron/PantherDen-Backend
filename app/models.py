from sqlalchemy import Column, Integer, String, Date

from app import Base, engine


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    homeroomid = Column(Integer)


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    roomid = Column(Integer)


class Schedule(Base):
    __tablename__ = "schedules"

    studentid = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)
    newroomid = Column(Integer)
    homeroomid = Column(Integer)

print Student.__table__
print Teacher.__table__
print Schedule.__table__

Base.metadata.create_all(engine)
