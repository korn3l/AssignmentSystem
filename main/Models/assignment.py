
class Assignment:
    def __init__(self, id, teacherName, courseName):
        self.id = id
        self.teacherName = teacherName
        self.courseName = courseName

    def as_tuple(self):
        return (self.id, self.teacherName, self.courseName)