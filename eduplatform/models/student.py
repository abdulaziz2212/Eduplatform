from models.user import User
import datetime
class Student(User):
    def __init__(self, _id, full_name, email, password_hash, grade):
        super().__init__(_id, full_name, email, password_hash, "Student")
        self.grade = grade
        self.subjects = {}
        self.assignments = {}
        self.grades = {}

    def submit_assignment(self, assignment_id, content, assignment_obj):
        now = datetime.now().isoformat()
        is_late = now > assignment_obj.deadline
        if is_late == False and len(content)<=500:
            self.assignments[assignment_id] = {
                "content": content,
                "submitted_at": now,
                "late": is_late
            }
        
    def view_grades(self, subject=None):
        if subject:
            return self.grades.get(subject, [])
        return self.grades

    def calculate_average_grade(self):
        total = count = 0
        for subject_grades in self.grades.values():
            total += sum(subject_grades)
            count += len(subject_grades)
        return total / count if count > 0 else 0