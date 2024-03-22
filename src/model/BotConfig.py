from src.model.Localization import lang_dict


class BotConfig:
    def __init__(self, lang_code):
        self.lang_code = lang_code

    def getMessage(self, text):
        return lang_dict[self.lang_code]["tele-meet-bot"]["messages"].get(text, "")
