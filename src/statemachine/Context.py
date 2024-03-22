from src import model
from src.model.User import User
from src.model.BotConfig import BotConfig
from src.bot.DBController import DBController


class Context:
    def __init__(self, lang_code):
        self.user = User()
        self.bot_config = BotConfig(lang_code)
        self.state = None

    def setState(self, state):
        self.state = state
        self.user.state_class = state.__class__
        model.StateUpdater.setState(self.user.chat_id, state)

    def getMessage(self, text):
        return self.bot_config.getMessage(text)

    def saveToDb(self):
        DBController().setUser(user)
