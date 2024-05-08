from src.statemachine import State
from src.statemachine.state import constructor
from src.model import Update
from aiogram import types
from src import bot
from src import resources
import pandas as pd
import random as rnd
import numpy as np

def choose_dish(table, good_products):
    dishes = table["блюдо"].to_numpy()
    weights = np.zeros(len(dishes)) + 1
    for product in good_products:
        weights += table[product].to_numpy()
    return rnd.choices(dishes, weights)[0]


def generator(user_id, table, dish_type, food_time):
    bot.DBController().cursor.execute(f"SELECT product FROM tele_meet_products WHERE type = -1")
    bad_products = bot.DBController().cursor.fetchone() or []
    bot.DBController().cursor.execute(f"SELECT product FROM tele_meet_products WHERE type = 1")
    good_products = bot.DBController().cursor.fetchone() or []
    table = table.loc[(table["тип блюда"] == dish_type) & (table["прием пищи"] == food_time)]
    for bad_product in bad_products:
        table = table.loc[table[bad_product] != -1]
    return "" if table.empty else choose_dish(table, good_products)


class GeneratorState(State):
    def __init__(self, context):
        super().__init__(context)
        self.constructorMenuBtn = context.get_message("constructorMenuBtn")

        self.nextStateDict = {
            self.constructorMenuBtn: constructor.ConstructorMenuState,
        }

    async def process_update(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()
        if message.text:
            if message.text in self.nextStateDict.keys():
                self.context.set_state(self.nextStateDict.get(message.text)(self.context))
                self.context.save_to_db()

    async def send_message(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()
        text = "Генерация меню\n"
        text += "Завтрак\n"
        text += "Основное - " + generator(self.context.user.id, pd.read_excel(f"/src/resources/table_for_test.xlsx"), "основное", "завтрак") + '\n'
        buttons = [
            [types.KeyboardButton(text=self.constructorMenuBtn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        return await message.answer(text, reply_markup=keyboard)
