from pathlib import Path

def find_project_root(start: Path | None = None) -> Path:
    """
    .git が存在するディレクトリを遡って探す。
    引数 start がファイルならその親から探索を始める。
    """
    if start is None:
        start = Path(__file__).resolve(strict=True)

    # ファイルなら親ディレクトリへ
    if start.is_file():
        start = start.parent

    # 上位に向かって探索
    for path in [start, *start.parents]:
        if (path / ".git").is_dir():
            return path

    raise FileNotFoundError("プロジェクトルート (.git) が見つかりませんでした")
