# core/run_openai.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypedDict

from openai import OpenAI
from openai import APIConnectionError, RateLimitError, BadRequestError

from config.enviroment import settings
from config.logger import get_logger

log = get_logger(__name__)

# ---- 型定義（Chat Completions で一般的な messages 形） ----
class Message(TypedDict):
    role: str         # "system" | "user" | "assistant" など
    content: str

# ---- 定数 ----
SOURCE_DIRNAME = "source"
DEFAULT_JSON   = "default_question.json"
MODEL_NAME     = "gpt-5-nano"   # 必要なら環境変数へ

# ---- ユーティリティ ----
def require_api_key() -> str:
    """API キーの存在を検査。なければ例外。"""
    key = settings.OPEN_AI_API_KEY
    if not key:
        msg = "OpenAI APIキーが未設定です。"
        log.error(msg)
        raise RuntimeError(msg)
    log.info("APIキーが設定されています。")
    return key

def project_root(start: Path | None = None) -> Path:
    """モジュール起点のプロジェクトルート（= このファイルの親の親）"""
    # 既存構成に合わせている。別の find 関数があるなら差し替えればよい。
    base = (start or Path(__file__)).resolve()
    return base.parent.parent

def get_json_path(filename: str = DEFAULT_JSON) -> Path:
    """source ディレクトリ配下の JSON ファイル Path を返す。存在検査を行う。"""
    src_dir = project_root() / SOURCE_DIRNAME
    if not src_dir.exists():
        msg = f"{src_dir} が存在しません。"
        log.error(msg)
        raise FileNotFoundError(msg)
    if not src_dir.is_dir():
        msg = f"{src_dir} はディレクトリではありません。"
        log.error(msg)
        raise NotADirectoryError(msg)

    json_path = src_dir / filename
    if not json_path.exists():
        msg = f"{json_path} が見つかりません。"
        log.error(msg)
        raise FileNotFoundError(msg)
    if not json_path.is_file():
        msg = f"{json_path} はファイルではありません。"
        log.error(msg)
        raise IsADirectoryError(msg)

    return json_path

def load_messages(json_path: Path) -> list[Message]:
    """JSON を読み込み、messages の最低限のスキーマを検証する。"""
    try:
        raw: Any = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        msg = f"JSONの構文エラー: {e}"
        log.error(msg)
        raise ValueError(msg) from e
    except Exception as e:
        msg = f"JSON読込エラー: {e}"
        log.error(msg)
        raise

    if not isinstance(raw, list):
        msg = "JSONの最上位は list である必要があります。"
        log.error(msg)
        raise TypeError(msg)

    msgs: list[Message] = []
    for i, item in enumerate(raw):
        if not (isinstance(item, dict) and "role" in item and "content" in item):
            msg = f"messages[{i}] の形式が不正です（role/content 必須）。"
            log.error(msg)
            raise TypeError(msg)
        role = item["role"]
        content = item["content"]
        if not (isinstance(role, str) and isinstance(content, str)):
            msg = f"messages[{i}] の型が不正です（role: str, content: str）。"
            log.error(msg)
            raise TypeError(msg)
        msgs.append({"role": role, "content": content})
    if not msgs:
        msg = "messages が空です。"
        log.error(msg)
        raise ValueError(msg)
    return msgs

def create_client(api_key: str) -> OpenAI:
    # 追加設定が必要ならここで集約
    return OpenAI(api_key=api_key)

def run_openai(filename: str = DEFAULT_JSON) -> str:
    """JSON を読み、Chat Completions を1回実行して返答本文を返す。"""
    api_key = require_api_key()
    json_path = get_json_path(filename)
    messages = load_messages(json_path)

    client = create_client(api_key)

    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,   # list[{"role": "...", "content": "..."}]
        )
    except RateLimitError as e:
        msg = f"Rate limit に達しました: {e}"
        log.error(msg)
        raise
    except BadRequestError as e:
        msg = f"リクエスト不正: {e}"
        log.error(msg)
        raise
    except APIConnectionError as e:
        msg = f"接続エラー: {e}"
        log.error(msg)
        raise
    except Exception as e:
        msg = f"OpenAI API 呼び出し中に例外: {e}"
        log.error(msg)
        raise

    try:
        answer = resp.choices[0].message.content or ""
    except Exception as e:
        msg = f"レスポンスの解析に失敗: {e}"
        log.error(msg)
        raise

    log.info("応答を取得しました。")
    # ここでは print せず、呼び出し側へ返す
    return answer

if __name__ == "__main__":
    # 実行例（ログにのみ出す。標準出力には流さない）
    try:
        ans = run_openai()
        log.info(f"モデル応答: {ans}")
    except Exception:
        # 具体的なログは各所で出している。ここでは異常終了を明示。
        raise
