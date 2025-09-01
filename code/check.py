from config.config import settings
from config.logger import get_logger

log = get_logger()


def check_api_key() -> None:
    if not settings.OPEN_AI_API_KEY:
        msg = "APIキーが未設定です"
        log.debug(msg)
        raise RuntimeError(msg)
    else:
        log.info("APIキーが設定されています。")
