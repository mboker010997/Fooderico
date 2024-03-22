from src.statemachine import State
from src.statemachine.state import profile
from src.model import Update


class InterestsTagState(State):
    def __init__(self, context):
        super().__init__(context)
        self.options = ['A)', 'B)', 'C']

    def processUpdate(self, update: Update):
        # add prev_poll_id and check that answer_ids different?
        poll_answer = update.getPollAnswer()
        if not self.context.user.interests_tags:
            self.context.user.interests_tags = set()
        if poll_answer:
            for option_id in poll_answer.option_ids:
                self.context.user.interests_tags.add(self.options[option_id])
            self.context.setState(profile.GeoState(self.context))
            self.context.saveToDb()

    async def sendMessage(self, update: Update):
        await update.bot.send_poll(chat_id=update.getChatId(),
                                   question='Какие у вас интересы?',
                                   options=self.options,
                                   is_anonymous=False,
                                   allows_multiple_answers=True,
                                   )
