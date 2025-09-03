from pathlib import Path


class DirManager:
    """
    childdirはproject_root/out/childdirという構成。
    """

    def __init__(self) -> None:
        self.rootdir: Path | None = None
        self.parentdir: Path | None = None
        self.childdir: Path | None = None

    def find_project_root(self) -> Path:
        """
        呼び出された場所を起点として、上位に向かって.gitがあるproject_rootを探索。
        """
        start = Path(__file__).resolve()

        # ファイルなら親ディレクトリへ
        if start.is_file():
            start = start.parent

        # 上位に向かって探索
        for path in [start, *start.parents]:
            if (path / ".git").is_dir():
                path = path.resolve()
                self.rootdir = path
                root = path
                return root

        raise FileNotFoundError("プロジェクトルートが見つかりませんでした")

    def setup_parentdir(self) -> None:
        self.parentdir = self.rootdir / "out"
        try:
            self.parentdir.mkdir(exist_ok=True)
        except Exception as e:
            raise RuntimeError("Error in making out-DIR.") from e

    def validate_dirname(self, dirname: str) -> str:
        INVALID_CHARS = ["/", r"\0", "..", " "]

        if not isinstance(dirname, str):
            obj_type = str(type(dirname))
            raise ValueError(f"dirname is {obj_type}")

        if not dirname:
            raise ValueError("empty name is invalid.")

        for invalid_char in INVALID_CHARS:
            if invalid_char in dirname:
                raise ValueError(
                    f"{dirname} is invalid. Include {invalid_char}."
                )

        return dirname

    def ensure_parentdir_from_dirname(self, dirname: str) -> None:
        root = self.find_project_root()
        valid_dirname = self.validate_dirname(dirname)
        childdir = root / valid_dirname

        try:
            childdir.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            raise RuntimeError(f"Error in making {childdir.name}.") from e

        self.childdir = childdir

#  % git commit -m "Ignore: outディレクトリは除外"
# [main 6656f11] Ignore: outディレクトリは除外
#  2 files changed, 2 insertions(+)
#  rename utils/{get_path.py => dirmanage.py} (100%)
