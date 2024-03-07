from state.InitialState import InitialState


class StateCacheHolder:
    def __init__(self):
        self.stateDict = dict()

    def setState(self, chatId, state):
        self.stateDict[chatId] = state

    def getState(self, chatId):
        return self.stateDict.get(chatId)