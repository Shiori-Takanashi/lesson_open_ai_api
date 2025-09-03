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

def validate_dirname(child_dirname: str) -> str:
    invalid_chars = ["/"]

    for invalid_char in invalid_chars:
        if invalid_char in child_dirname:
            raise ValueError(f"{child_dirname} is invalid.")
        else:
            pass

    return child_dirname



def ensure_outdir_from_dirname(child_dirname: str) -> None:
    if not child_dirname:
        raise ValueError(f"child_dirname is '' .")

    outdirpath: Path | None = None

    rootpath = find_project_root()
    valid_child_dirname = validate_dirname(child_dirname)
    out_dirpath = rootpath / child_dirname
    out_dirpath.mkdir(exist_ok=True)

    return out_dirpath

def get_outdir_from_dirname() -> Path:
    out_dirpath = ensure_outdir_form_dirname()
    return out_dirpath
