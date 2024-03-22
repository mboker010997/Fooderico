import yaml

lang_dict = dict()


class Localization:
    @staticmethod
    def loadInfo(lang_codes):
        for lang_code in lang_codes:
            filename = f"/Users/mboker0109/MIPT/Inprak/jira/tele-meet-bot/src/resources/{lang_code}.yml"
            with open(filename, "r") as stream:
                data_loaded = yaml.safe_load(stream)
                lang_dict[lang_code] = data_loaded
