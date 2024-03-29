import yaml

lang_dict = dict()
langs = ['ru']
default_lang = 'ru'


class Localization:
    @staticmethod
    def loadInfo():
        for lang_code in langs:
            filename = f"/src/resources/{lang_code}.yml"
            with open(filename, "r") as stream:
                data_loaded = yaml.safe_load(stream)
                lang_dict[lang_code] = data_loaded
