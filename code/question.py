# import asyncio
# import aiohttp
# from openai import OpenAI
# from prac_open_ai.config import settings
# from prac_open_ai.logger import get_logger

# log = get_logger(__name__)


# def run_openai() -> None:
#     # APIキーが正しいか確認
#     check_api_key()

#     # クライアント作成
#     client = OpenAI(api_key=settings.API_KEY)

#     # Chat Completions の呼び出し
#     response = client.chat.completions.create(
#         model="gpt-5-nano",
#         messages=[
#             {"role": "system", "content": "あなたは冷静なアシスタントです。"},
#             {"role": "user", "content": "ランダムに世界史の登場人物を一人だけ出力せよ。一般的な日本語表記で出力せよ。"}, #
#         ],
#     )

#     # 返答をログに出力
#     answer = response.choices[0].message.content
#     log.info(f"{answer}")
