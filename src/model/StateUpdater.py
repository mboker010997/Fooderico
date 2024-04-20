from src import bot
from src.statemachine.state import *
from src import statemachine

state_cache_holder = dict()


class StateUpdater:
    @staticmethod
    def get_state(chat_id):
        context = state_cache_holder.get(chat_id, None)
        if context is None:
            user = bot.DBController().get_user_by_chat_id(chat_id)
            state_class = user.state_class
            if state_class is None:
                return InitialState()
            context = statemachine.Context(None, user)
            context.state = state_class(context)
            state_cache_holder[chat_id] = context
        return context.state

    @staticmethod
    def get_context(chat_id) -> statemachine.Context:
        context = state_cache_holder.get(chat_id, None)
        return context

    @staticmethod
    def get_sent_message(chat_id):
        context = state_cache_holder.get(chat_id, None)
        if context is None:
            return None
        return context.get_sent_message()

    @staticmethod
    def set_sent_message(chat_id, message):
        context = state_cache_holder.get(chat_id, None)
        if context is not None:
            context.set_sent_message(message)
