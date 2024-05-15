from src.statemachine import State
from src import bot
from aiogram import types
from src.model import Update, Tags as tags
from src.statemachine.state import menu


class ComplaintState(State):
    def __init__(self, context, photo_id, complaint_text):
        super().__init__(context)
        self.photo_id = photo_id
        self.complaint_text = complaint_text
        self.menuBtn = context.get_message("menuBtn")
        self.text = context.get_message("chat_complaint_reason")

    async def process_update(self, update: Update):
        if not update.get_message():
            return
        text = update.get_message().text
        if text != self.menuBtn:
            await self.send_complaint(text, update)
            await update.bot.send_message(
                chat_id=update.get_chat_id(),
                text=self.context.get_message("chat_complaint_send"),
            )
        self.context.set_state(menu.MenuState(self.context))
        self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()

        buttons = [
            [types.KeyboardButton(text=self.menuBtn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        await message.answer(self.text, reply_markup=keyboard)

    async def send_complaint(self, text, update: Update):
        send_text = (f"#Жалоба\n"
                     f" <b>Причина: </b> {text}\n\n{self.complaint_text}")
        all_admins = bot.DBController().get_all_admins()
        for admin_chat_id in all_admins:
            if self.photo_id:
                await update.bot.send_photo(
                    chat_id=int(admin_chat_id),
                    photo=self.photo_id,
                    caption=send_text,
                    parse_mode='HTML',
                )
            else:
                await update.bot.send_message(
                    chat_id=int(admin_chat_id),
                    text=send_text,
                    parse_mode='HTML',
                )
