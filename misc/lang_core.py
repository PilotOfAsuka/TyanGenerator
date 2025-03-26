import json

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

    def get(self, key, lang=None):

        return self.translations.get(lang, {}).get(key, f"[{key}]")

# Пример translations.json.json:
# {
#     "ru": {"hello": "Привет", "bye": "Пока"},
#     "en": {"hello": "Hello", "bye": "Bye"}
# }

# Использование:
lang = LangEngine(default_lang="en")

