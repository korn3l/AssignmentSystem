class Course:
    def __init__(self,id,courseCode,title,creditHours,semester):
        self.id=id
        self.courseCode=courseCode
        self.title=title
        self.creditHours=creditHours
        self.semester=semester


    def as_tuple(self):
        return (self.courseCode, self.title, self.creditHours, self.semester)