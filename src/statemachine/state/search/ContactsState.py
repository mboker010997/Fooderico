from src.statemachine import State
from src.statemachine.state import menu
from src.model.UserRelation import UserRelation
from src import bot
from src.model import Update
from aiogram import types
from src.algo import similarity


class ContactsState(State):
    def __init__(self, context):
        super().__init__(context)
        self.menu_text = self.context.getMessage("menu_text")
        self.nextStateDict = {
            self.menu_text: menu.MenuState,
        }
        self.CHANGE_TO_LIKE_COMMAND = "/change_to_like_"
        self.CHANGE_TO_DISLIKE_COMMAND = "/change_to_dislike_"
        self.REMOVE_RELATION_COMMAND = "/remove_"

    def processUpdate(self, update: Update):
        pass

    async def __switchContext(self, update: Update):
        self.context.setState(menu.MenuState(self.context))
        self.context.saveToDb()
        await self.context.state.sendMessage(update)

    async def sendMessage(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()
        my_chat_id = bot.DBController().getUser(self.context.user.id).chat_id

        query = (f"SELECT * FROM tele_meet_relations WHERE user_id = {self.context.user.id} "
                 f"AND relation != 'SKIPPED'")
        bot.DBController().cursor.execute(query)
        self.other_user_rows = bot.DBController().cursor.fetchall()
        counter = 0
        for other_user_row in self.other_user_rows:
            other_relation = other_user_row[3]
            other_user_id = other_user_row[2]
            other_user = bot.DBController().getUser(other_user_id)
            other_profile_name = other_user.profile_name

            text = ""
            command = ""
            if other_relation == "FOLLOW":
                text = "Вы лайкнули"
                command = self.CHANGE_TO_DISLIKE_COMMAND
            elif other_relation == "BLACKLIST":
                text = "Вы дизлайкнули"
                command = self.CHANGE_TO_LIKE_COMMAND
            if other_user.photo_file_ids:
                await message.answer_photo(photo=other_user.photo_file_ids[0],
                                           caption=f"{text}: {other_profile_name}\n"
                                                   f"{command}{counter}\n"
                                                   f"{self.REMOVE_RELATION_COMMAND}{counter}")
            else:
                await update.bot.send_message(chat_id=my_chat_id,
                                              text=f"{text}: {other_profile_name}\n"
                                                   f"{command}{counter}\n"
                                                   f"{self.REMOVE_RELATION_COMMAND}{counter}")
            counter += 1
        await self.__switchContext(update)