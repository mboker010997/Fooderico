from src.model.Geolocation import Geolocation, Status
from src.statemachine.State import State
from aiogram import types
from src.statemachine.state import profile
from src.model import Update

from geopy.distance import geodesic
import requests


class GeoState(State):
    def __init__(self, context):
        super().__init__(context)
        self.text = "Передайте геолокацию или укажите город"
        self.query_city = None
        self.counter = -1
        self.status = Status.INIT

    def processUpdate(self, update: Update):
        if not update.getMessage():
            return
        message = update.getMessage()

        if (
            self.context.user.geolocation is not None
            and message.text == self.context.getMessage("geo_skipBtn")
        ):
            self.setStateInContext()
            self.context.saveToDb()
            return

        self.status = Status.INIT
        if message.location:
            geolocation = Geolocation(
                message.location.latitude, message.location.longitude
            )
            self.context.user.geolocation = geolocation
            city = self.getCityByGeolocation(geolocation)
            if city:
                self.context.user.city = city
                self.setStateInContext()
            else:
                city = self.findNearestCity(geolocation)
                if city:
                    self.query_city = city
                    self.text = f"{city} - это ваш город?"
                    self.status = Status.CONFIRMATION
                else:
                    self.text = "Город не определен. Пожалуйста, введите название вашего города"
        elif message.text == "Передать геолокацию":
            self.text = "Ошибка геолокации. Попробуйте еще раз"
        elif message.text == "Да, это мой город":
            city = self.query_city
            self.context.user.city = city
            self.setStateInContext()
        elif message.text == "Нет, это не мой город":
            self.text = "Город не определен. Пожалуйста, введите название вашего города"
        else:
            city = message.text
            self.context.user.city = city
            latitude, longitude, name = self.getCoordinats(city)
            if latitude:
                geolocation = Geolocation(latitude, longitude)
                self.context.user.city = name
                self.context.user.geolocation = geolocation
                self.context.setState(profile.AboutState(self.context))
                self.setStateInContext()
            else:
                self.text = "Координаты города не найдены. Попробуйте еще раз"
        self.context.saveToDb()

    def setStateInContext(self):
        nextState = self.context.getNextState()
        if nextState is None:
            nextState = profile.AboutState
        self.context.setState(nextState(self.context))

    async def sendMessage(self, update: Update):
        chatId = update.getChatId()

        if self.context.user.geolocation is not None:
            kb = [
                [
                    types.KeyboardButton(
                        text="Передать геолокацию",
                        request_location=True,
                    )
                ],
                [
                    types.KeyboardButton(
                        text=self.context.getMessage("geo_skipBtn")
                    )
                ],
            ]
        else:
            kb = [
                [
                    types.KeyboardButton(
                        text="Передать геолокацию",
                        request_location=True,
                    )
                ],
            ]

        if self.status == Status.CONFIRMATION:
            kb.append(
                [
                    types.KeyboardButton(
                        text="Да, это мой город",
                    )
                ]
            )
            kb.append(
                [
                    types.KeyboardButton(
                        text="Нет, это не мой город",
                    )
                ]
            )
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True, one_time_keyboard=True
        )
        await update.bot.send_message(
            chat_id=chatId, text=self.text, reply_markup=keyboard
        )

    @staticmethod
    def getCityByGeolocation(geolocation):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.8, ru-RU, ru;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "cookie": "_osm_totp_token=114327",
        }
        lat = geolocation.latitude
        lon = geolocation.longitude
        url = f"http://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            city = data['address']['city']
        except Exception:
            city = None
        return city

    @staticmethod
    def getCoordinats(city):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.8, ru-RU, ru;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "cookie": "_osm_totp_token=114327",
        }
        url = f"http://nominatim.openstreetmap.org/search?format=json&city={city}"
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            lat, lon = data[0]['lat'], data[0]['lon']
            name = data[0]['display_name'].split(',')[0]
        except Exception:
            lat, lon, name = None, None, None
        return lat, lon, name

    @staticmethod
    def searchNearbyFeatures(latitude, longitude, radius):
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        (
          node(around:{radius},{latitude},{longitude})[place="city"];
        );
        out body;
        """
        params = {"data": query}
        response = requests.get(overpass_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["elements"]
        else:
            return []

    @staticmethod
    def findNearestCity(geolocation):
        lat = geolocation.latitude
        lon = geolocation.longitude
        for radius in range(50000, 150001, 50000):
            nearest_cities = GeoState.searchNearbyFeatures(lat, lon, radius)
            if len(nearest_cities) == 0:
                continue
            best_city = nearest_cities[0]
            best_city_dist = geodesic(
                (lat, lon),
                (best_city["lat"], best_city["lon"]),
                ellipsoid="WGS-84",
            ).m
            for city in nearest_cities:
                current = geodesic(
                    (lat, lon), (city["lat"], city["lon"]), ellipsoid="WGS-84"
                ).m
                if best_city_dist > current:
                    best_city = city
                    best_city_dist = current
            return best_city["tags"]["name"]
        return None
