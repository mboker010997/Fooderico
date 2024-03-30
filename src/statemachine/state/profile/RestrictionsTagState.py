from src.statemachine import State
from src.statemachine.state import profile
from src.model.Update import Update
from src.model import Tags as tags


class RestrictionsTagState(State):
    def __init__(self, context):
        super().__init__(context)
        self.options = tags.restrictionsTags
        self.hasPoll = True

    def processUpdate(self, update: Update):
        poll_answer = update.getPollAnswer()
        if poll_answer and int(poll_answer.poll_id) == int(self.context.user.active_poll_id):
            if not self.context.user.restrictions_tags:
                self.context.user.restrictions_tags = set()
            for option_id in poll_answer.option_ids:
                self.context.user.restrictions_tags.add(self.options[option_id])
            self.context.user.active_poll_id = update.getPollAnswer().poll_id
            self.context.setState(profile.DietsTagState(self.context))
            self.context.saveToDb()
        self.hasPoll = False

    async def sendMessage(self, update: Update):
        options = list(map(lambda x: self.context.getMessage(x), tags.restrictionsTags))
        if self.hasPoll:
            poll_info = await update.bot.send_poll(chat_id=update.getChatId(),
                                                   question=self.context.getMessage("restrictions_tag_text"),
                                                   options=options,
                                                   is_anonymous=False,
                                                   allows_multiple_answers=True)
            self.context.user.active_poll_id = poll_info.poll.id
            self.context.saveToDb()

