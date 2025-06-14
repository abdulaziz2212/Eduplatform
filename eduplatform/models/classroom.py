class Classroom:
    def __init__(self, class_id, name):
        self.class_id = class_id
        self.name = name
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student_id):
        self.students = [s for s in self.students if s._id != student_id]

    def list_students(self):
        return [s.get_profile() for s in self.students]