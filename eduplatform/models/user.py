from models.abstract_role import AbstractRole

class User(AbstractRole):
    def __init__(self, _id, full_name, email, password_hash, role):
        super().__init__(_id, full_name, email, password_hash)
        self.role = role
        self._notifications = []

    def add_notification(self, message):
        self._notifications.append(message)

    def view_notifications(self):
        return self._notifications

    def delete_notification(self, index):
        if 0 <= index < len(self._notifications):
            del self._notifications[index]

    def get_profile(self):
        return {
            "id": self._id,
            "name": self._full_name,
            "email": self._email,
            "role": self.role,
            "created_at": self._created_at
        }

    def update_profile(self, **kwargs):
        self._full_name = kwargs.get("full_name", self._full_name)
        self._email = kwargs.get("email", self._email)
