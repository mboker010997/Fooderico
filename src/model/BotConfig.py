from src.model.Localization import lang_dict, default_lang


class BotConfig:
    def __init__(self, lang_code):
        self.lang_code = lang_code
        if lang_code not in lang_dict.keys():
            self.lang_code = default_lang

    def getMessage(self, text):
        return lang_dict[self.lang_code]["tele-meet-bot"]["messages"].get(
            text, ""
        )
