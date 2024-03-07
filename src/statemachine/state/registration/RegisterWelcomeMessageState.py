from src.statemachine.State import State


class RegisterWelcomeMessageState(State):
    def __init__(self, bot, dp):
        super().__init__(bot, dp)

    def processUpdate(self, message):
        # send_to_db('welcome_message'=message.text)
        pass

    def getNextState(self, message):
        pass

    def sendMessage(self, message):
        await message.answer("Напишите приветственное сообщение и еще немножко о своих других интересах. Это поможет "
                             "быстрее найти контакт.")
