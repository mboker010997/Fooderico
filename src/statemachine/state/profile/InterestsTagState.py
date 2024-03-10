from src.statemachine.State import State
from aiogram import types
from src.statemachine.state.profile.GeoState import GeoState


class InterestsTagState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, message: types.PollAnswer):
        answer_ids = message.option_ids  # list of answers
        pass

    def getNextState(self, message):
        return GeoState()

    async def sendMessage(self, message, bot, dp):
        await message.answer_poll(question='Какие у вас интересы?',
                                  options=['A)', 'B)', 'C'],
                                  type='regular',
                                  allows_multiple_answers=True)
