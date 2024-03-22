from src.statemachine.state import InitialState
from src.bot.DBController import DBController


class StateUpdater:
    @staticmethod
    def setState(chat_id, state):
        DBController().updateState(chat_id, state)

    @staticmethod
    def getState(chat_id):
        state = DBController().getState(chat_id)
        if state is None:
            state = InitialState()
        return state
