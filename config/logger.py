# prac_open_ai/logger.py
import logging
import sys
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent / "logs"


def make_logfile_path() -> Path:
    """実行スクリプトのファイル名からログファイルパスを生成する。"""
    LOG_DIR.mkdir(exist_ok=True)

    # sys.argv[0] に実行ファイル名が入る
    caller_file = Path(sys.argv[0]).stem or "app"
    return LOG_DIR / f"{caller_file}.log"


def get_logger(name: str = __name__) -> logging.Logger:
    """ターミナルとファイルへログを出すロガーを返す。"""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logfile = make_logfile_path()

    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)

    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(fh)
    return logger
