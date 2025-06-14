from models.user import User
from models.student import Student

class Parent(User):
    def __init__(self, _id, full_name, email, password_hash):
        super().__init__(_id, full_name, email, password_hash, "Parent")
        self.children = []

    def view_child_grades(self, student:Student):
        return student.view_grades()

    def view_child_assignments(self, student:Student):
        return student.assignments

    def receive_child_notification(self, student:Student):
        return student.view_notifications()
