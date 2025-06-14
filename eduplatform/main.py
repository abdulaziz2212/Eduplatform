from models.student import Student
from models.teacher import Teacher
from models.parent import Parent
from models.admin import Admin
from data.auth import hash_password, check_password
from datetime import datetime
import csv

users = []
assignments = [] 

user_map = {
    "Admin": Admin,
    "Teacher": Teacher,
    "Student": Student,
    "Parent": Parent
}


def load_users_from_csv(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_class = user_map.get(row["role"])
            if not user_class:
                continue
            uid = int(row["id"])
            full_name = row["full_name"]
            email = row["email"]
            password = row["password"]
            password_hash = password if len(password) == 64 else hash_password(password)
            role = row["role"]
            if role == "Student":
                grade = row.get("grade", "9-A")
                users.append(Student(uid, full_name, email, password_hash, grade))
            elif role == "Parent":
                users.append(Parent(uid, full_name, email, password_hash))
            else:
                users.append(user_class(uid, full_name, email, password_hash))

load_users_from_csv("sample_users_extended.csv")


admin = Admin(1, "Admin User", "admin@edu.com", hash_password("admin123"))
teacher = Teacher(2, "Mr. Smith", "smith@edu.com", hash_password("teach123"))
student = Student(3, "Jane Doe", "jane@edu.com", hash_password("stud123"), "9-A")
parent = Parent(4, "Mrs. Doe", "parent@edu.com", hash_password("parent123"))

parent.children.append(student)

users.extend([admin, teacher, student, parent])

if not users:
    admin = Admin(1, "Admin User", "admin@edu.com", hash_password("admin123"))
    teacher = Teacher(2, "Mr. Smith", "smith@edu.com", hash_password("teach123"))
    student = Student(3, "Jane Doe", "jane@edu.com", hash_password("stud123"), "9-A")
    parent = Parent(4, "Mrs. Doe", "parent@edu.com", hash_password("parent123"))
    parent.children.append(student)  # For testing
    users.extend([admin, teacher, student, parent])

# User login simulation
def login():
    email = input("Enter your email: \n").strip()
    password = input("Enter your password: \n").strip()
    for user in users:
        if user._email == email and check_password(password, user._password_hash):
            return user
    print("Invalid credentials.")
    return None

# Student panel
def student_panel(student):
    while True:
        print("\n--- Student Panel ---")
        print("1. View Profile")
        print("2. View Grades")
        print("3. Calculate Average Grade")
        print("4. Submit Assignment")
        print("5. View Notifications")
        print("0. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            print(student.get_profile())
        elif choice == "2":
            print(student.view_grades())
        elif choice == "3":
            print("Average Grade:", student.calculate_average_grade())
        elif choice == "4":
            aid = input("Assignment ID: ")
            content = input("Your answer: ")
            student.submit_assignment(aid, content)
            print("Assignment submitted!")
        elif choice == "5":
            print("Notifications:", student.view_notifications())
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

# Teacher panel
def teacher_panel(teacher):
    while True:
        print("\n--- Teacher Panel ---")
        print("1. View Profile")
        print("2. View Student Progress")
        print("0. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            print(teacher.get_profile())
        elif choice == "2":
            sid = input("Enter student ID: ")
            found = next((u for u in users if u._id == int(sid) and isinstance(u, Student)), None)
            if found:
                print("Grades:", teacher.view_student_progress(found))
            else:
                print("Student not found.")
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

# Parent panel
def parent_panel(parent):
    while True:
        print("\n--- Parent Panel ---")
        print("1. View Profile")
        print("2. View Child Grades")
        print("3. View Child Assignments")
        print("4. View Child Notifications")
        print("0. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            print(parent.get_profile())
        elif choice in ["2", "3", "4"]:
            if not parent.children:
                print("No linked children.")
                continue
            child = parent.children[0]
            if choice == "2":
                print(parent.view_child_grades(child))
            elif choice == "3":
                print(parent.view_child_assignments(child))
            elif choice == "4":
                print(parent.receive_child_notification(child))
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

# Admin panel
def admin_panel(admin):
    while True:
        print("\n--- Admin Panel ---")
        print("1. View Profile")
        print("2. Generate Report")
        print("0. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            print(admin.get_profile())
        elif choice == "2":
            report = admin.generate_report(users)
            for r in report:
                print(r)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    print("Welcome to EduPlatform!\n")
    user = login()
    if user:
        if getattr(user, "role", None) == "Student":
            student_panel(user)
        elif getattr(user, "role", None) == "Teacher":
            teacher_panel(user)
        elif getattr(user, "role", None) == "Parent":
            parent_panel(user)
        elif getattr(user, "role", None) == "Admin":
            admin_panel(user)
    print("Goodbye!")