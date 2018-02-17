from .base import Model


class User(Model):

    def __init__(self, username, password, id=-1):
        self.username = username
        self.password = password
        self.id = id

    @classmethod
    def validate(cls, username, password):
        user = User.get_by(username=username, password=password)
        if user:
            return user
        else:
            return None
