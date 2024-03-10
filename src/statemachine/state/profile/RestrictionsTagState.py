from src.statemachine.State import State
from aiogram import types
from src.statemachine.state.profile.InterestsTagState import InterestsTagState


class RestrictionsTagState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, message: types.PollAnswer):
        answer_ids = message.option_ids  # list of answers
        pass

    def getNextState(self, message):
        return InterestsTagState()

    async def sendMessage(self, message, bot, dp):
        await message.answer_poll(question='Какие у вас ограничения?',
                                  options=['A)', 'B)', 'C'],
                                  type='regular',
                                  allows_multiple_answers=True)
