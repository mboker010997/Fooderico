from src import model
from src.model.User import User
from src.model.BotConfig import BotConfig
from src import bot


class Context:
    def __init__(self, lang_code=None, user=User(), state=None):
        self.user = user
        if lang_code is None:
            lang_code = user.language_code
        self.bot_config = BotConfig(lang_code)
        self.state = state

    def setState(self, state):
        self.state = state
        # self.user.id = int(self.user.chat_id)
        self.user.state_class = state.__class__
        # model.StateUpdater.setState(self.user.chat_id, state)

    def getMessage(self, text):
        return self.bot_config.getMessage(text)

    def saveToDb(self):
        bot.DBController().setUser(self.user)
