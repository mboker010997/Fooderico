from src.statemachine.state import InitialState

stateHolder = dict()  # todo(mboker0109) remove this in FOOD-38


class StateUpdater:
    @staticmethod
    def setState(chat_id, state):
        # todo(mboker0109): write sql query in FOOD-38
        stateHolder[chat_id] = state

    @staticmethod
    def getState(chat_id):
        # todo(mboker0109): write sql query in FOOD-38
        return stateHolder.get(chat_id, InitialState())
