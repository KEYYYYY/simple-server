from .base import Model


class Todo(Model):
    def __init__(self, title, user_id, id=-1):
        self.title = title
        self.user_id = user_id
        self.id = id
