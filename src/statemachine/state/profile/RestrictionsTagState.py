from src.statemachine import State
from src.statemachine.state import profile
from src.model.Update import Update


class RestrictionsTagState(State):  # todo(mboker0109): add RestrictionTag enum and support all tags in FOOD-30
    def __init__(self, context):
        super().__init__(context)
        self.options = ['A)', 'B)', 'C']

    def processUpdate(self, update: Update):
        # expected poll answer
        poll_answer = update.getPollAnswer()
        if not self.context.user.restrictions_tags:
            self.context.user.restrictions_tags = set()
        if poll_answer:
            for option_id in poll_answer.option_ids:
                self.context.user.restrictions_tags.add(self.options[option_id])
            self.context.setState(profile.InterestsTagState(self.context))
            self.context.saveToDb()

    async def sendMessage(self, update: Update):
        message = update.getMessage()
        await message.answer_poll(question='Какие у вас ограничения?',
                                  options=self.options,
                                  allows_multiple_answers=True,
                                  is_anonymous=False)
