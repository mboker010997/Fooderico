from src.statemachine.State import State
import RegisterWelcomeMessageState


class RegisterInterestsState(State):
    def __init__(self, bot, dp):
        super().__init__(bot, dp)

    def processUpdate(self, message):
        # send_to_db('interests'=message.text)
        pass

    def getNextState(self, message):
        return RegisterWelcomeMessageState

    def sendMessage(self, message):
        await message.answer("Основные интересы:")
