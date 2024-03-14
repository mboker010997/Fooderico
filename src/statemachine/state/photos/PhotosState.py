from src.statemachine.State import State
from src.statemachine.state.photos.PhotoListState import PhotoListState
from src.statemachine.state.photos.PhotoUploadState import PhotoUploadState
from aiogram import types


class PhotosState(State):
    def __init__(self, photo_file_ids): #photo_file_ids: List - from typing import List
        self.photo_file_ids = photo_file_ids

    def processUpdate(self, message: types.Message):
        if message.text == "Посмотреть фото":
            self.nextState = PhotoListState(self.photo_file_ids)
        elif message.text == "Загрузить фото":
            self.nextState = PhotoUploadState()
        elif message.text == "Удалить фото":
            photo_file_ids = []
            self.nextState = self
            # remove from db
        else:
            self.nextState = self

    def getNextState(self, message: types.Message):
        return self.nextState

    async def sendMessage(self, message: types.Message, bot, dp):
        kb = [
            [types.KeyboardButton(text="Посмотреть фото")],
            [types.KeyboardButton(text="Загрузить фото")],
            [types.KeyboardButton(text="Удалить фото")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
        await message.answer("Что хотите сделать в фотоальбоме?", reply_markup=keyboard)
