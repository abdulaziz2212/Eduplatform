from models.user import User
from models.assignment import Assignment
from models.student import Student

class Teacher(User):
    def __init__(self, _id, full_name, email, password_hash):
        super().__init__(_id, full_name, email, password_hash, "Teacher")
        self.subjects = []
        self.classes = []
        self.assignments = {}
        self.schedule = {}

    def create_assignment(self, assignment_id, assignment):
        self.assignments[assignment_id] = assignment

    def grade_assignment(self, assignment: Assignment, student_id, grade):
        assignment.set_grade(student_id, grade)

    def view_student_progress(self, student:Student):
        return student.view_grades()
    
    def add_subjects(self, subject_name):
        self.subjects.append(subject_name)

   
    def add_classes(self, class_name):
        self.classes.append(class_name)

    def change_schedule(self, class1, time, subject):
        if time in self.schedule.keys():
            print("You have already lesson at that time.")
            input1 = input("Write 1 if you want to reschedule for this time (or write anything to cancel): ")
            if input1 == "1":
                self.schedule[time] = [class1, subject]
            else:
                pass
        else:
            self.schedule[time] = [class1, subject]

    def view_schedule(self):
        return self.schedule