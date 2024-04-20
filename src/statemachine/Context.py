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
        self.sent_message = None
        self.next_state = None
        self.other_chat_id = None

    def set_state(self, state):
        self.state = state
        self.user.state_class = state.__class__

    def set_sent_message(self, message):
        self.sent_message = message

    def get_sent_message(self):
        sent_message = self.sent_message
        self.sent_message = None
        return sent_message

    def set_next_state(self, state):
        self.next_state = state

    def get_next_state(self):
        next_state = self.next_state
        self.next_state = None
        return next_state

    def get_message(self, text):
        return self.bot_config.get_message(text)

    def save_to_db(self):
        bot.DBController().setUser(self.user)
