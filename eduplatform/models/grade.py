class Grade:
    def __init__(self, _id, student_id, subject, value, date, teacher_id):
        self.id = _id
        self.student_id = student_id
        self.subject = subject
        self.value = value
        self.date = date
        self.teacher_id = teacher_id

    def update_grade(self, value):
        self.value = value

    def get_grade_info(self):
        return {
            "student_id": self.student_id,
            "subject": self.subject,
            "value": self.value,
            "date": self.date,
            "teacher_id": self.teacher_id
        }
