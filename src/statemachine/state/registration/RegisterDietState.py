from src.statemachine.State import State
import RegisterInterestsState


class RegisterDietState(State):
    def __init__(self, bot, dp):
        super().__init__(bot, dp)

    def processUpdate(self, message):
        # send_to_db('diet'=message.text)
        pass

    def getNextState(self, message):
        return RegisterInterestsState

    def sendMessage(self, message):
        await message.answer("Вы соблюдаете диету?")
