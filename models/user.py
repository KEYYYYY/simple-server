from .base import Model


class User(Model):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def validate(cls, username, password):
        user = User.get_by(username=username, password=password)
        if user:
            return True
        return False
