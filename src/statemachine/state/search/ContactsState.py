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


    def processUpdate(self, update: Update):
        pass

    async def __switchContext(self, update: Update):
        self.context.setState(menu.MenuState(self.context))
        self.context.saveToDb()
        await self.context.state.sendMessage(update)

    async def sendMessage(self, update: Update):
        my_chat_id = bot.DBController().getUser(self.context.user.id).chat_id

        query = (f"SELECT * FROM tele_meet_relations WHERE user_id = {self.context.user.id} "
                 f"AND relation != 'SKIPPED'")
        bot.DBController().cursor.execute(query)
        other_user_rows = bot.DBController().cursor.fetchall()
        for other_user_row in other_user_rows:
            other_relation = other_user_row[3]
            other_user_id = other_user_row[2]
            if other_relation == "FOLLOW":
                other_profile_name = bot.DBController().getUser(int(other_user_id)).profile_name
                await update.bot.send_message(chat_id=my_chat_id,
                                              text="Вы лайкнули: {}".format(other_profile_name))
                # query = (f"SELECT * FROM tele_meet_users WHERE user_id = {int(other_user_id)} ")
                # bot.DBController().cursor.execute(query)
                # other_user_rows = bot.DBController().cursor.fetchall()
                # for other_user_row in other_user_rows:
                #     photo_ids = other_user_row[14]
                #     for photo_id in photo_ids:
                #         await update.bot.send_photo(chat_id=my_chat_id, photo=photo_id)

            if other_relation == "BLACKLIST":
                other_profile_name = bot.DBController().getUser(int(other_user_id)).profile_name
                await update.bot.send_message(chat_id=my_chat_id,
                                              text="Вы дизлайкнули: {}".format(other_profile_name))
        await self.__switchContext(update)

