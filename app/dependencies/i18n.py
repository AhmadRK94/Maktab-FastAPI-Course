import gettext
from fastapi import Request, Depends

SUPPORTED_LANGUAGES = ["en", "fa"]
DEFAULT_LANGUAGE = "en"


def detect_language(request: Request) -> str:
    # 1. Query param has priority
    lang = request.query_params.get("lang")
    if lang and lang in SUPPORTED_LANGUAGES:
        return lang

    return DEFAULT_LANGUAGE


def get_translator(lang: str = Depends(detect_language)):
    print(lang)
    localedir = "locales"
    translator = gettext.translation(
        "messages",
        localedir=localedir,
        languages=[lang],
        fallback=True,
    )
    _ = translator.gettext
    return _
