from src.model.Geolocation import Geolocation, Status
from src.statemachine.State import State
from aiogram import types
from src.statemachine.state import profile
from src.model import Update
import requests


class GeoState(State):
    def __init__(self, context):
        super().__init__(context)
        self.text = "Передайте геолокацию или укажите город"
        self.all_cities = ['Dolgoprudny', 'Paris', 'Moscow']
        self.counter = -1
        self.status = Status.INIT

    def processUpdate(self, update: Update):
        message = update.getMessage()
        self.status = Status.INIT
        if message.location:
            geolocation = Geolocation(message.location.latitude, message.location.longitude)
            self.context.user.geolocation = geolocation

            city = self.getCity(geolocation)
            if city:
                self.context.user.city = city
                self.context.setState(profile.AboutState(self.context))
            else:
                self.text = "Город не определен. Пожалуйста, введите название города"
        elif message.text == "Передать геолокацию":
            self.text = "Ошибка геолокации. Попробуйте еще раз"
        elif message.text == "Да, это мой город":
            city = self.all_cities[self.counter]
            self.context.user.city = city
            latitude, longitude = self.getCoordinats(city)
            if latitude:
                geolocation = Geolocation(latitude, longitude)
                self.context.user.geolocation = geolocation
                self.context.setState(profile.AboutState(self.context))
            else:
                self.text = "Координаты города не найдены. Попробуйте еще раз"
        elif message.text == "Нет, это не мой город":
            next_city = self.nextCity()
            if not next_city:
                self.text = "Весь список городов пройден. Попробуйте еще раз"
                return
            self.text = f"Города с таким названием нет, может вы имели в виду - {next_city}?"
            self.status = Status.SORTTHROUGH
        else:
            self.counter = -1
            city = message.text
            if city not in self.all_cities:
                self.sortCities(city)
                nearest = self.nextCity()
                self.text = f"Города с таким названием нет, может вы имели в виду - {nearest}?"
                self.status = Status.SORTTHROUGH
                return
            self.context.user.city = city
            latitude, longitude = self.getCoordinats(city)
            if latitude:
                geolocation = Geolocation(latitude, longitude)
                self.context.user.geolocation = geolocation
                self.context.setState(profile.AboutState(self.context))
            else:
                self.text = "Координаты города не найдены. Попробуйте еще раз"
        self.context.saveToDb()

    async def sendMessage(self, update: Update):
        chatId = update.getChatId()
        kb = [
            [types.KeyboardButton(
                text="Передать геолокацию",
                request_location=True,
            )],
        ]
        if self.status == Status.SORTTHROUGH:
            kb.append([types.KeyboardButton(
                text="Да, это мой город",
            )])
            kb.append([types.KeyboardButton(
                text="Нет, это не мой город",
            )])
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await update.bot.send_message(chat_id=chatId, text=self.text,
                                      reply_markup=keyboard)

    def getCity(self, geolocation):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.8, ru-RU, ru;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Brave\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "cookie": "_osm_totp_token=114327"
        }
        lat = geolocation.latitude
        lon = geolocation.longitude
        url = f"http://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        response = requests.get(url, headers=headers)
        data = response.json()
        try:
            city = data['address']['city']
        except Exception:
            city = None
        return city

    def getCoordinats(self, city):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.8, ru-RU, ru;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Brave\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "cookie": "_osm_totp_token=114327"
        }
        url = f"http://nominatim.openstreetmap.org/search?format=json&city={city}"
        response = requests.get(url, headers=headers)
        data = response.json()
        try:
            lat, lon = data[0]['lat'], data[0]['lon']
        except Exception:
            lat, lon = None, None
        return lat, lon

    def nextCity(self):
        if self.counter + 1 >= len(self.all_cities):
            next_city = None
        else:
            self.counter += 1
            next_city = self.all_cities[self.counter]
        return next_city

    def sortCities(self, city):
        def levenstein(word):
            targetWord = city
            n, m = len(word), len(targetWord)
            if n > m:
                word, targetWord = targetWord, word
                n, m = m, n
            current_row = range(n + 1)
            for i in range(1, m + 1):
                previous_row, current_row = current_row, [i] + [0] * n
                for j in range(1, n + 1):
                    add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                    if word[j - 1] != targetWord[i - 1]:
                        change += 1
                    current_row[j] = min(add, delete, change)
            return current_row[n]

        self.all_cities = sorted(self.all_cities, key=levenstein)
