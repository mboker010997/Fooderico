from src.statemachine import State
from src.statemachine.state import profile
from src.model.Update import Update


class RestrictionsTagState(State):  # todo(mboker0109): add RestrictionTag enum and support all tags in FOOD-30
    def __init__(self, context):
        super().__init__(context)
        self.options = ['A)', 'B)', 'C']
        self.hasPoll = True

    def processUpdate(self, update: Update):
        poll_answer = update.getPollAnswer()
        if poll_answer:
            if not self.context.user.restrictions_tags:
                self.context.user.restrictions_tags = set()
            for option_id in poll_answer.option_ids:
                self.context.user.restrictions_tags.add(self.options[option_id])
            self.context.user.active_poll_id = update.getPollAnswer().poll_id
            self.context.setState(profile.InterestsTagState(self.context))
            self.context.saveToDb()
        self.hasPoll = False

    async def sendMessage(self, update: Update):
        if self.hasPoll:
            await update.bot.send_poll(chat_id=update.getChatId(),
                                       question='Какие у вас ограничения?',
                                       options=self.options,
                                       is_anonymous=False,
                                       allows_multiple_answers=True)
