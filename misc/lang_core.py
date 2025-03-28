import json
from tools.user_state_handler import users_data

class LangEngine:
    def __init__(self, default_lang="ru", path="misc/translations.json"):
        self.default_lang = default_lang
        self.translations = self.load_translations(path)

    def load_translations(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get(self, key, message):

        return self.translations.get(users_data.get_user_language(message), {}).get(key, f"[{key}]")


# Использование:
lang = LangEngine(default_lang="en")

