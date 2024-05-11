from src.statemachine import State
from src.statemachine.state import constructor
from src.model import Update
from aiogram import types
from src import bot
import pandas as pd
import random as rnd
import numpy as np

tmp_products = [
    'Рыба',
    'Яйцо',
    'Сельдерей',
    'Соя',
    'Карп',
    'Треска',
    'Мед',
    'Грибы',
    'Яблоко',
    'Абрикос',
    'Персик',
    'Банан',
    'Ананас',
    'Киви',  
    'Вишня, черешня'
    'Консервант Бензоат натрия',
    'Консервант SO2 (вино)',
    'Моллюски',
    'Люпин',  
    'Коровье молоко',
    'Орехи',
    'Ракообразные',
    'Креветка',
    'Арахис',
    'Горчица',
    'Злаки',
    'Гречка',
    'Пшеница'
]


def choose_dish(table, good_products):
    dishes = table["Блюдо"].to_numpy()
    weights = np.zeros(len(dishes)) + 1
    for product in good_products:
        if product not in tmp_products:
            continue
        weights += table[product].to_numpy()
    return rnd.choices(dishes, weights)[0]


def generator(user_id, table, dish_type, food_time):
    bot.DBController().cursor.execute(f"SELECT product FROM tele_meet_products WHERE type = -1")
    bad_products = bot.DBController().cursor.fetchone() or []
    bot.DBController().cursor.execute(f"SELECT product FROM tele_meet_products WHERE type = 1")
    good_products = bot.DBController().cursor.fetchone() or []
    table = table.loc[(table["Тип блюда"] == dish_type) & (table[food_time] == 1)]
    for bad_product in bad_products:
        if bad_product not in tmp_products:
            continue
        table = table.loc[table[bad_product] != -1]
    return "Не найдено" if table.empty else choose_dish(table, good_products)


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
        dataframe = pd.read_excel(f"/src/resources/final.xlsx")
        text = "Генерация меню\n"
        text += "Завтрак\n"
        text += "Основное - " + generator(self.context.user.id, dataframe, "Основное", "Завтрак") + '\n'
        text += "Напиток - " + generator(self.context.user.id, dataframe, "Напиток", "Завтрак") + '\n'
        text += "Обед\n"
        text += "Суп - " + generator(self.context.user.id, dataframe, "Суп", "Обед") + '\n'
        text += "Основное - " + generator(self.context.user.id, dataframe, "Основное", "Обед") + '\n'
        text += "Салат - " + generator(self.context.user.id, dataframe, "Салат", "Обед") + '\n'
        text += "Напиток - " + generator(self.context.user.id, dataframe, "Напиток", "Обед") + '\n'
        text += "Ужин\n"
        text += "Основное - " + generator(self.context.user.id, dataframe, "Основное", "Ужин") + '\n'
        text += "Салат - " + generator(self.context.user.id, dataframe, "Салат", "Ужин") + '\n'
        text += "Напиток - " + generator(self.context.user.id, dataframe, "Напиток", "Ужин") + '\n'
        buttons = [
            [types.KeyboardButton(text=self.constructorMenuBtn)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        return await message.answer(text, reply_markup=keyboard)
