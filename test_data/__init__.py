from datetime import datetime
import app.models as ms

# You need students, teachers, and schedules csv files.

students = [ms.Student(*s.split(","))
            for s in open("test_data/students.csv").read().splitlines()[1:]]

teachers = [ms.Teacher(*t.split(","))
            for t in open("test_data/teachers.csv").read().splitlines()[1:]]

schedules = [ms.Schedule(s[0], s[1], s[2], datetime.strptime(s[3], "%m-%d-%y"))
             for s in [l.split(",") for l in open("test_data/schedules.csv").read().splitlines()[1:]]]
