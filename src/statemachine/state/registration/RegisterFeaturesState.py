from src.statemachine.State import State
import RegisterDietState


class RegisterFeaturesState(State):
    def __init__(self, bot, dp):
        super().__init__(bot, dp)

    def processUpdate(self, message):
        # send_to_db('features'=message.text)
        pass

    def getNextState(self, message):
        return RegisterDietState

    def sendMessage(self, message):
        await message.answer("Какие у вас есть особенности?")
