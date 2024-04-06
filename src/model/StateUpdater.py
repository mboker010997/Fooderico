from src import bot
from src.statemachine.state import *
from src import statemachine

stateCacheHolder = dict()


class StateUpdater:
    @staticmethod
    def getState(chat_id):
        context = stateCacheHolder.get(chat_id, None)
        if context is None:
            user = bot.DBController().getUserByChatId(chat_id)
            stateClass = user.state_class
            if stateClass is None:
                return InitialState()
            context = statemachine.Context(None, user)
            context.state = stateClass(context)
            stateCacheHolder[chat_id] = context
        return context.state

    @staticmethod
    def getSentMessage(chat_id):
        context = stateCacheHolder.get(chat_id, None)
        if context is None:
            return None
        return context.getSentMessage()

    @staticmethod
    def setSentMessage(chat_id, message):
        context = stateCacheHolder.get(chat_id, None)
        if context is not None:
            context.setSentMessage(message)
