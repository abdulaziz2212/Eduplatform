from models.user import User

class Admin(User):
    def __init__(self, _id, full_name, email, password_hash):
        super().__init__(_id, full_name, email, password_hash, "Admin")
        self.permissions = ["add_user", "remove_user", "generate_report"]

    def add_user(self, user_list, user):
        user_list.append(user)

    def remove_user(self, user_list, user_id):
        user_list[:] = [u for u in user_list if u._id != user_id]

    def generate_report(self, users):
        return [u.get_profile() for u in users]