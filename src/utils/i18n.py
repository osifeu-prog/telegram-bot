import json, os

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "locales")
DEFAULT_LANGUAGE = "en"
_languages = {}

def get_string(key: str, language: str = None) -> str:
    if not language:
        language = DEFAULT_LANGUAGE
    if language not in _languages:
        path = os.path.join(LOCALE_DIR, f"{language}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                _languages[language] = json.load(f)
        except FileNotFoundError:
            if language != DEFAULT_LANGUAGE:
                return get_string(key, DEFAULT_LANGUAGE)
            return key
    return _languages[language].get(key, key)
