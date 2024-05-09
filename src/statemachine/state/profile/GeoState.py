import random

from src.model.Geolocation import Geolocation, Status
from src.statemachine.State import State
from aiogram import types
from src.statemachine.state import profile
from src.model import Update
from src.bot.config import nominatim_URL

from geopy.distance import geodesic
import requests
import logging


class GeoState(State):
    def __init__(self, context):
        super().__init__(context)
        self.text = "Передайте геолокацию или укажите город"
        self.query_city = None
        self.counter = -1
        self.status = Status.INIT

    async def process_update(self, update: Update):
        if not update.get_message():
            return
        message = update.get_message()

        if self.context.user.geolocation is not None and message.text == self.context.get_message("geo_skipBtn"):
            self.set_state_in_context()
            self.context.save_to_db()
            return

        self.status = Status.INIT
        if message.location:
            geolocation = Geolocation(message.location.latitude, message.location.longitude)
            self.context.user.geolocation = geolocation
            city = self.get_city_by_geolocation(geolocation)
            if city:
                self.context.user.city = city
                self.set_state_in_context()
            else:
                city = self.find_nearest_city(geolocation)
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
            self.set_state_in_context()
        elif message.text == "Нет, это не мой город":
            self.text = "Город не определен. Пожалуйста, введите название вашего города"
        else:
            city = message.text
            self.context.user.city = city
            latitude, longitude, name = self.get_coordinats(city)
            if latitude:
                geolocation = Geolocation(latitude, longitude)
                self.context.user.city = name
                self.context.user.geolocation = geolocation
                self.context.set_state(profile.AboutState(self.context))
                self.set_state_in_context()
            else:
                self.text = "Координаты города не найдены. Попробуйте еще раз"
        self.context.save_to_db()

    def set_state_in_context(self):
        next_state = self.context.get_next_state()
        if next_state is None:
            next_state = profile.AboutState
        self.context.set_state(next_state(self.context))

    async def send_message(self, update: Update):
        chat_id = update.get_chat_id()

        if self.context.user.geolocation is not None:
            buttons = [
                [types.KeyboardButton(text="Передать геолокацию", request_location=True)],
                [types.KeyboardButton(text=self.context.get_message("geo_skipBtn"))],
            ]
        else:
            buttons = [
                [types.KeyboardButton(text="Передать геолокацию", request_location=True)],
            ]

        if self.status == Status.CONFIRMATION:
            buttons.append([types.KeyboardButton(text="Да, это мой город")])
            buttons.append([types.KeyboardButton(text="Нет, это не мой город")])
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
        await update.bot.send_message(chat_id=chat_id, text=self.text, reply_markup=keyboard)

    @staticmethod
    def get_city_by_geolocation(geolocation):
        # different fake User Agents to use nominatim API without violated the usage policy of
        # nominatim.openstreetmap.org
        user_agent_list = [
            "Fooderico", "Telemeetbot", "Foodbot", "abcd", "Registration"
        ]
        headers = {
            "User-Agent": random.choice(user_agent_list),
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
        url = f"{nominatim_URL}/reverse?format=json&lat={lat}&lon={lon}"
        response = requests.get(url, headers=headers)
        try:
            data = response.json()
            city = data["address"]["city"]
        except IndexError or TypeError:
            city = None
        except Exception as exc:
            city = None
            logging.exception("get_city_by_geolocation (GeoState)")
            logging.exception(exc)
        return city

    @staticmethod
    def get_coordinats(city):
        # different fake User Agents to use nominatim API without violated the usage policy of
        # nominatim.openstreetmap.org
        user_agent_list = [
            "Fooderico", "Telemeetbot", "Foodbot", "abcd", "Registration"
        ]
        headers = {
            "User-Agent": random.choice(user_agent_list),
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
        url = f"{nominatim_URL}/search?format=json&city={city}"
        response = requests.get(url, headers=headers)
        print(response)
        try:
            data = response.json()
            lat, lon = data[0]["lat"], data[0]["lon"]
            name = data[0]["display_name"].split(",")[0]
        except IndexError or TypeError:
            lat, lon, name = None, None, None
        except Exception as exc:
            lat, lon, name = None, None, None
            logging.exception("get_coordinats (GeoState)")
            logging.exception(exc)
        return lat, lon, name

    @staticmethod
    def search_near_by_features(latitude, longitude, radius):
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
    def find_nearest_city(geolocation):
        lat = geolocation.latitude
        lon = geolocation.longitude
        for radius in range(50000, 150001, 50000):
            nearest_cities = GeoState.search_near_by_features(lat, lon, radius)
            if len(nearest_cities) == 0:
                continue
            best_city = nearest_cities[0]
            best_city_dist = geodesic(
                (lat, lon),
                (best_city["lat"], best_city["lon"]),
                ellipsoid="WGS-84",
            ).m
            for city in nearest_cities:
                current = geodesic((lat, lon), (city["lat"], city["lon"]), ellipsoid="WGS-84").m
                if best_city_dist > current:
                    best_city = city
                    best_city_dist = current
            return best_city["tags"]["name"]
        return None
