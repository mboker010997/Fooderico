from src.statemachine.State import State
from src.statemachine.state.profile.GeoState import GeoState
from src.bot.Update import Update


class InterestsTagState(State):
    def __init__(self):
        super().__init__()

    def processUpdate(self, update: Update):
        # expected poll answer
        pass

    def getNextState(self, update: Update):
        return GeoState()

    async def sendMessage(self, update: Update):
        await update.bot.send_poll(chat_id=update.getChatId(),
                                   question='Какие у вас интересы?',
                                   options=['A)', 'B)', 'C'],
                                   is_anonymous=False,
                                   allows_multiple_answers=True
                                   )

