from src import model
from src.model.User import User
from src.bot.DBController import DBController


class Context:
    def __init__(self):
        self.user = User()
        self.state = None

    def setState(self, state):
        self.state = state
        self.user.state_class = state.__class__
        model.StateUpdater.setState(self.user.chat_id, state)

    def saveToDb(self):
        DBController().setUser(user)
