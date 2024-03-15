import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from src.statemachine.Handler import Handler
from src.bot.DBController import DBController
from src.statemachine.state.profile.AboutState import AboutState
from src.bot.User import User

class TelegramBot:
    def __init__(self):
        load_dotenv()
        self.bot = Bot(os.getenv("TOKEN"))
        # self.bot = Bot("6645685311:AAEv2S99I2KCXcJa8ZtEZHpLxVKO3_fL-6I") # Debug
        self.dp = Dispatcher()
        self.handler = Handler(self.bot, self.dp)
        logging.basicConfig(level=logging.INFO)

    async def start_polling(self):
        await self.dp.start_polling(self.bot)


if __name__ == '__main__':
    try:
        dbcontroller = DBController()
        bot = TelegramBot()
        
        ################## Test getState
        st = DBController().getState(1)()
        print(isinstance(st, AboutState))
        #################
        
        ################# Test updateUserInformation
        update_fields = {
            "city": "MM",
            "last_name": "Alex",
            "age": 19,
        }
        
        DBController().updateUserInformation(1, update_fields)
        #################
        
        ################# Test updateState
        DBController().updateState(2, "AgeState")   
        ################
        
        ################ Test getAllInformation
        d = DBController().getUserDict(1)
        print(d)
        ################
        
        ################ Test getUser
        d = DBController().getUser(1)
        print(d)
        print(d.city, d.age)
        ################
        
        ################ Test setUser
        d.age = 5
        d = DBController().setUser(d)
        ################
        
        asyncio.run(bot.start_polling())
    except Exception as _ex:
        print(_ex)
    finally:
        if dbcontroller.connection:
            dbcontroller.connection.commit()
            dbcontroller.connection.close()
