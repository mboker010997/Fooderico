from src.statemachine import State
from src import bot
from src.statemachine.state import menu
from aiogram import types
from enum import Enum
from src.model import Update, Tags as tags


# from src.admin import crud as admin


class Status(Enum):
    MAIN = "Главная панель"
    ADD_ADMIN = "Добавление админа"
    USER_INFO = "Информация о пользователе"


class AdminState(State):
    def __init__(self, context):
        super().__init__(context)
        self.text = "Панель админки"
        self.metricsBtn = context.get_message("admin_metricsBtn")
        self.add_adminBtn = context.get_message("admin_add_adminBtn")
        self.user_infoBtn = context.get_message("admin_user_infoBtn")
        self.returnBtn = context.get_message("admin_returnBtn")
        self.menuBtn = context.get_message("menuBtn")
        self.feedbackBtn = context.get_message("admin_feedbackBtn")
        self.status = Status.MAIN

    async def process_update(self, update: Update):
        if not update.get_message():
            return
        text = update.get_message().text
        if text == self.returnBtn:
            self.text = text
            self.status = Status.MAIN
        elif self.status == Status.ADD_ADMIN:
            if not text.isdigit():
                self.text = self.context.get_message("admin_wrong_id")
            else:
                chat_id = int(text)
                user = bot.DBController().get_user_by_chat_id(chat_id)
                self.status = Status.MAIN
                if not user.id:
                    self.text = self.context.get_message("admin_no_user")
                else:
                    print("admin_add_admin_completed")
                    if bot.DBController().add_admin(chat_id):
                        self.text = self.context.get_message("admin_add_admin_error")
                    else:
                        self.text = self.context.get_message("admin_add_admin_completed")
                        await update.bot.send_message(
                            chat_id=chat_id,
                            text=self.context.get_message("admin_add_admin_message"),
                        )
        elif self.status == Status.USER_INFO:
            if not text.isdigit():
                self.text = self.context.get_message("admin_wrong_id")
            else:
                chat_id = int(text)
                user = bot.DBController().get_user_by_chat_id(chat_id)
                self.status = Status.MAIN
                if not user.id:
                    self.text = self.context.get_message("admin_no_user")
                else:
                    self.text = await self.get_user_info_text(user)
        elif text == self.menuBtn:
            self.context.set_state(menu.MenuState(self.context))
            self.status = Status.MAIN
        elif text == self.metricsBtn:
            users_count = bot.DBController().metric_number_of_users()
            active_users_count = bot.DBController().metric_number_of_active_users()
            most_common_city = bot.DBController().metric_most_common_city()
            match_count = bot.DBController().metric_number_of_match()
            all_admins = bot.DBController().get_all_admins()
            self.text = (f"#Метрики\n"
                         f"  <b>Всего пользователей:</b> {users_count}\n"
                         f"  <b>Активных пользователей:</b> {active_users_count}\n"
                         f"  <b>Наиболее распространенные города:</b> {most_common_city}\n"
                         f"  <b>Текущее количество матчей:</b> {match_count}\n"
                         f"  <b>Админы:</b> {all_admins}\n")
            self.status = Status.MAIN
        elif text == self.add_adminBtn:
            self.status = Status.ADD_ADMIN
            self.text = self.context.get_message("admin_user_get_id")
        elif text == self.user_infoBtn:
            self.status = Status.USER_INFO
            self.text = self.context.get_message("admin_user_get_id")
        elif text == self.feedbackBtn:
            feedback_number = bot.DBController().get_feedback_number(self.context.user.chat_id)
            feedback_size = bot.DBController().get_feedback_size()
            assert feedback_number <= feedback_size

            if feedback_number == feedback_size:
                text = self.context.get_message("admin_feedback_everything_has_been_viewed")
                self.text = "Панель админки"
                await update.bot.send_message(chat_id=self.context.user.chat_id, text=text)
            else:
                res = bot.DBController().get_feedback(feedback_number)
                bot.DBController().set_feedback_number(self.context.user.chat_id, feedback_number + len(res))
                text = self.context.get_message("admin_feedback_everything_has_been_viewed")
                text = ""
                for feedback_item in res:
                    text += f"chat_id = {feedback_item[0]}\n{feedback_item[1]}\n\n"
                await update.bot.send_message(chat_id=self.context.user.chat_id, text=text)
                self.text = "Панель админки"

            self.status = Status.MAIN

        self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()
        if self.status == Status.MAIN:
            buttons = [
                [types.KeyboardButton(text=self.user_infoBtn)],
                [types.KeyboardButton(text=self.add_adminBtn)],
                [types.KeyboardButton(text=self.metricsBtn)],
                [types.KeyboardButton(text=self.feedbackBtn)],
                [types.KeyboardButton(text=self.menuBtn)],
            ]
        else:
            buttons = [
                [types.KeyboardButton(text=self.returnBtn)],
            ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        return await message.answer(self.text, reply_markup=keyboard, parse_mode='HTML')

    async def get_user_info_text(self, user):
        name = user.profile_name
        age = user.age
        city = user.city
        info = user.about
        preferences = tags.get_readable_tags_description(
            user.preferences_tags, self.context.bot_config
        )
        restrictions = tags.get_readable_tags_description(
            user.restrictions_tags, self.context.bot_config
        )
        diets = tags.get_readable_tags_description(
            user.dietary, self.context.bot_config
        )
        interests = tags.get_readable_tags_description(
            user.interests_tags, self.context.bot_config
        )
        # photo_ids = user.photo_file_ids

        text = (f"<b>Анкета:</b>\n"
                f"  <b>Имя:</b> {name}\n"
                f"  <b>Возраст:</b> {age}\n"
                f"  <b>Город:</b> {city}\n"
                f"  <b>Пищевые предпочтения:</b> {preferences}\n"
                f"  <b>Ограничения:</b> {restrictions}\n"
                f"  <b>Диета:</b> {diets}\n"
                f"  <b>Интересы:</b> {interests}\n"
                f"  <b>О себе:</b> {info}")
        return text
