# code/run_git_log.py
from __future__ import annotations

import subprocess
from pathlib import Path

# --- 設定 ---
OUTDIR_NAME = ".gitlog"                 # ルート直下に作成
OUTFILE_STEM = "gitlog"                 # gitlogNN.txt
DEFAULT_PRETTY = "%H %cI %d %s"         # ← ハッシュを先頭に
ALL_BRANCHES = True
SINCE: str | None = None
LIMIT: int | None = None


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

# --- 採番・出力 ---
def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def next_index(dirpath: Path) -> int:
    max_n = -1
    for f in dirpath.glob(f"{OUTFILE_STEM}*.txt"):
        stem = f.stem  # e.g., gitlog03
        if stem.startswith(OUTFILE_STEM):
            tail = stem[len(OUTFILE_STEM):]
            if tail.isdigit() and len(tail) == 2:
                n = int(tail)
                if n > max_n:
                    max_n = n
    return max_n + 1  # 既存なし→0

def write_text(text: str, outdir: Path) -> Path:
    ensure_dir(outdir)
    idx = next_index(outdir)
    outfile = outdir / f"{OUTFILE_STEM}{idx:02d}.txt"
    outfile.write_text(text, encoding="utf-8", newline="\n")
    return outfile

# プレビューから先頭ハッシュを落とす
def preview_without_hash_first(line: str) -> str:
    s = line.rstrip("\r\n")
    parts = s.split(maxsplit=1)  # 左端だけ分割
    return parts[1] if len(parts) == 2 else s

# --- git 実行 ---
def build_git_log_cmd(
    all_branches: bool = ALL_BRANCHES,
    pretty: str = DEFAULT_PRETTY,
    since: str | None = SINCE,
    limit: int | None = LIMIT,
) -> list[str]:
    cmd: list[str] = [
        "git", "--no-pager",
        "log", "--no-color",
        f"--pretty={pretty}",
    ]
    if all_branches:
        cmd.append("--all")
    if since:
        cmd.extend(["--since", since])
    if limit:
        cmd.extend(["-n", str(limit)])
    return cmd

def run_git(cmd: list[str], cwd: Path) -> str:
    cp = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=True,
    )
    return cp.stdout

# --- メイン ---
def main() -> None:
    root = find_project_root(Path(__file__).resolve())
    outdir = root / OUTDIR_NAME

    cmd = build_git_log_cmd()  # 設定値に従う
    try:
        text = run_git(cmd, cwd=root)
    except subprocess.CalledProcessError as e:
        print(f"[git failed] returncode={e.returncode}")
        if e.stderr:
            print(e.stderr.strip()[:2000])
        return

    out = write_text(text, outdir)

    # プレビュー（ハッシュは表示しない）
    first = text.splitlines()[0] if text else ""
    preview = preview_without_hash_first(first)
    print(f"書込: {out.name}\n先頭: {preview[:100]} ...")

if __name__ == "__main__":
    main()
