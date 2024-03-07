from src.statemachine.State import State
import RegisterCityState


class RegisterNameState(State):
    def __init__(self, bot, dp):
        super().__init__(bot, dp)

    def processUpdate(self, message):
        # send_to_db('name'=message.text)
        pass

    def getNextState(self, message):
        return RegisterCityState

    def sendMessage(self, message):
        await message.answer("Как вас зовут?")
