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
        self.sentMessage = None
        self.nextState = None
        self.other_chat_id = None

    def setState(self, state):
        self.state = state
        # self.user.id = int(self.user.chat_id)
        self.user.state_class = state.__class__
        # model.StateUpdater.setState(self.user.chat_id, state)

    def setSentMessage(self, message):
        self.sentMessage = message

    def getSentMessage(self):
        sentMessage = self.sentMessage
        self.sentMessage = None
        return sentMessage

    def setNextState(self, state):
        self.nextState = state

    def getNextState(self):
        nextState = self.nextState
        self.nextState = None
        return nextState

    def getMessage(self, text):
        return self.bot_config.getMessage(text)

    def saveToDb(self):
        bot.DBController().setUser(self.user)
