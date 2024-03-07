from src.statemachine.State import State
import RegisterAgeState


class RegisterState(State):
    def __init__(self, bot, dp):
        super().__init__(bot, dp)

    def processUpdate(self, message):
        pass

    def getNextState(self, message):
        return RegisterAgeState

    def sendMessage(self, message):
        await message.answer("Сейчас просим ответить на несколько небольших вопросов. Это поможет подобрать "
                             "оптимальный список собеседников.")
