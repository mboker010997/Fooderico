from enum import Enum


class Geolocation:
    def __init__(self, latitude=None, longitude=None):
        self.R = 6371
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = None


class Status(Enum):
    INIT = "Инициализация"
    CONFIRMATION = "Подтверждение города"
