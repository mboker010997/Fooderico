from src import model
from src.model.User import User


class Context:
    def __init__(self):
        self.user = User()
        self.state = None

    def setState(self, state):
        self.state = state
        self.user.state_class = state.__class__
        model.StateUpdater.setState(self.user.chat_id, state)

    def saveToDb(self):
        # todo(mboker0109): FOOD-38
        pass
