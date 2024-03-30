from src.statemachine import State
from src.statemachine.state import profile
from src.model import Update
from src.model import Tags as tags


class InterestsTagState(State):
    def __init__(self, context):
        super().__init__(context)
        self.options = tags.interestsTags
        self.hasPoll = True

    def processUpdate(self, update: Update):
        poll_answer = update.getPollAnswer()
        if poll_answer and int(poll_answer.poll_id) == (int(self.context.user.active_poll_id)):
            if not self.context.user.interests_tags:
                self.context.user.interests_tags = set()
            for option_id in poll_answer.option_ids:
                self.context.user.interests_tags.add(self.options[option_id])
            self.context.user.active_poll_id = None
            self.context.setState(profile.GeoState(self.context))
            self.context.saveToDb()
        self.hasPoll = False

    async def sendMessage(self, update: Update):
        options = list(map(lambda x: self.context.getMessage(x), tags.interestsTags))
        if self.hasPoll:
            poll_info = await update.bot.send_poll(chat_id=update.getChatId(),
                                                   question=self.context.getMessage("interests_tag_text"),
                                                   options=options,
                                                   is_anonymous=False,
                                                   allows_multiple_answers=True)
            self.context.user.active_poll_id = poll_info.poll.id
            self.context.saveToDb()
