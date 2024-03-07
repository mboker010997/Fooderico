from src.statemachine.State import State
import RegisterFeaturesState


class RegisterCityState(State):
    def __init__(self, bot, dp):
        super().__init__(bot, dp)

    def processUpdate(self, message):
        # send_to_db('city'=message.text)
        pass

    def getNextState(self, message):
        return RegisterFeaturesState

    def sendMessage(self, message):
        await message.answer("Из какого вы города? Можно поделиться локацией или написать город/район/метро")
