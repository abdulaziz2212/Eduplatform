class Assignment:
    def __init__(self, _id, title, description, deadline, subject, teacher_id, class_id):
        self.id = _id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.subject = subject
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.submissions = {}
        self.grades = {}

    def add_submission(self, student_id, content):
        self.submissions[student_id] = content

    def set_grade(self, student_id, grade):
        self.grades[student_id] = grade

    def get_status(self):
        return {
            "submitted": list(self.submissions.keys()),
            "graded": list(self.grades.keys())
        }
