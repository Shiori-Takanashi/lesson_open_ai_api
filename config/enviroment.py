# config/enviroment.py
import os

from dotenv import load_dotenv

# .env をロード
load_dotenv()


class Settings:
    # 環境変数から取得
    OPEN_AI_API_KEY: str = os.getenv("OPENAI_API_KEY")


settings = Settings()
