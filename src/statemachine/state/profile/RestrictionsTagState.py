from src.statemachine.State import State
from src.statemachine.state.profile.InterestsTagState import InterestsTagState
from src.bot.Update import Update


class RestrictionsTagState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, update: Update):
        # expected poll answer
        poll_answer = update.getPollAnswer()
        if poll_answer is None:
            self.nextState = self
        else:
            self.nextState = InterestsTagState()
        pass

    def getNextState(self, update: Update):
        return self.nextState

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer_poll(question='Какие у вас ограничения?',
                                  options=['A)', 'B)', 'C'],
                                  allows_multiple_answers=True,
                                  is_anonymous=False)
