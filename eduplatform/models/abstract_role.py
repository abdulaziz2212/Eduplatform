from abc import ABC, abstractmethod
from datetime import datetime

class AbstractRole(ABC):
    def __init__(self, _id, full_name, email, password_hash):
        self._id = _id
        self._full_name = full_name
        self._email = email
        self._password_hash = password_hash
        self._created_at = datetime.now().isoformat()

    @abstractmethod
    def get_profile(self):
        pass

    @abstractmethod
    def update_profile(self, **kwargs):
        pass