from datetime import datetime

class Notification:
    def __init__(self, _id, message, recipient_id):
        self.id = _id
        self.message = message
        self.recipient_id = recipient_id
        self.created_at = datetime.now().isoformat()
        self.is_read = False

    def send(self):
        # Would normally push to a user's notification list
        return True

    def mark_as_read(self):
        self.is_read = True
