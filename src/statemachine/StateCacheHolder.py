from src.statemachine.state.InitialState import InitialState


class StateCacheHolder:
    def __init__(self):
        self.state_dict = dict()

    def set_state(self, chat_id, state):
        self.state_dict[chat_id] = state

    def get_state(self, chat_id):
        return self.state_dict.get(chat_id, InitialState())
