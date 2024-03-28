from src import bot
from src.statemachine.state import *
from src import statemachine

stateHolder = dict()  # todo(mboker0109) remove this in FOOD-38


class StateUpdater:
    @staticmethod
    def setState(chat_id, state):
        bot.DBController().updateState(chat_id, state)

    @staticmethod
    def getState(chat_id):
        user = bot.DBController().getUserByChatId(chat_id)
        stateClass = user.state_class
        if stateClass is None:
            state = InitialState()
        else:
            state = stateClass(statemachine.Context(None, user))
            state.context.state = state
        return state
