from src.statemachine import State
from src.statemachine.state import menu
from src import bot
from src.model import Update
from aiogram import types


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
        if not update.getMessage():
            return
        message = update.getMessage()
        my_chat_id = bot.DBController().getUser(self.context.user.id).chat_id

        query = (f"SELECT * FROM tele_meet_relations "
                 f"WHERE user_id = {self.context.user.id} "
                 f"ORDER BY id DESC "
                 f"LIMIT 1")

        bot.DBController().cursor.execute(query)
        self.other_user_rows = bot.DBController().cursor.fetchall()
        counter = 0
        for other_user_row in self.other_user_rows:
            other_relation = other_user_row[3]
            other_user_id = other_user_row[2]
            other_user = bot.DBController().getUser(other_user_id)
            other_profile_name = other_user.profile_name

            buttons = []
            text = ""

            if other_relation == "FOLLOW":
                text = self.context.getMessage("contacts_you_have_liked")
                buttons = [[
                        types.InlineKeyboardButton(
                            text=self.context.getMessage(
                                "contacts_change_to_dislike"
                            ),
                            callback_data=f"change_to_dislike_{counter}",
                        )],
                    [types.InlineKeyboardButton(
                            text=self.context.getMessage(
                                "contacts_change_to_skip"
                            ),
                            callback_data=f"change_to_skip_{counter}",
                        )],
                    [types.InlineKeyboardButton(
                            text=self.context.getMessage("contacts_remove"),
                            callback_data=f"remove_{counter}"
                        )],
                ]

            elif other_relation == "BLACKLIST":
                text = self.context.getMessage("contacts_you_have_disliked")
                buttons = [[
                        types.InlineKeyboardButton(
                            text=self.context.getMessage(
                                "contacts_change_to_like"
                            ),
                            callback_data=f"change_to_like_{counter}",
                        )],
                    [types.InlineKeyboardButton(
                            text=self.context.getMessage(
                                "contacts_change_to_skip"
                            ),
                            callback_data=f"change_to_skip_{counter}",
                        )],
                    [types.InlineKeyboardButton(
                            text=self.context.getMessage("contacts_remove"),
                            callback_data=f"remove_{counter}"
                        )],
                ]

            elif other_relation == "SKIPPED":
                text = self.context.getMessage("contacts_you_have_skiped")
                buttons = [[
                        types.InlineKeyboardButton(
                            text=self.context.getMessage(
                                "contacts_change_to_like"
                            ),
                            callback_data=f"change_to_like_{counter}",
                        )],
                    [types.InlineKeyboardButton(
                            text=self.context.getMessage(
                                "contacts_change_to_dislike"
                            ),
                            callback_data=f"change_to_dislike_{counter}",
                        )],
                    [types.InlineKeyboardButton(
                            text=self.context.getMessage("contacts_remove"),
                            callback_data=f"remove_{counter}"
                        )],
                ]

            keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

            if other_user.photo_file_ids:
                await message.answer_photo(
                    photo=other_user.photo_file_ids[0],
                    caption=f"{text}: {other_profile_name}",
                    reply_markup=keyboard,
                )
            else:
                await update.bot.send_message(
                    chat_id=my_chat_id,
                    text=f"{text}: {other_profile_name}",
                    reply_markup=keyboard,
                )

            counter += 1
        await self.__switchContext(update)
