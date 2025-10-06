
class Teacher:
    def __init__(self,id,name,department,email,phoneNumber):
        self.id=id
        self.name=name
        self.department=department
        self.email=email
        self.phoneNumber=phoneNumber

    def as_tuple(self):
        return (self.name, self.department, self.email, self.phoneNumber)
