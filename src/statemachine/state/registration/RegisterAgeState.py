from src.statemachine.State import State
import RegisterNameState


class RegisterAgeState(State):
    def __init__(self, bot, dp):
        super().__init__(bot, dp)

    def processUpdate(self, message):
        # send_to_db('age'=message.text)
        pass

    def getNextState(self, message):
        return RegisterNameState

    def sendMessage(self, message):
        await message.answer("Сколько вам полных лет?")
