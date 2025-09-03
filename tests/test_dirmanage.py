from pathlib import Path

import pytest

from utils.dirmanage import DirManager


def test_rootdir_is_none() -> None:
    dmanager = DirManager()
    assert dmanager.rootdir is None


def test_parentdir_is_none() -> None:
    dmanager = DirManager()
    assert dmanager.parentdir is None


def test_childdir_is_none() -> None:
    dmanager = DirManager()
    assert dmanager.childdir is None

# def test_find_project_root_with_git(tmp_path: Path) -> None:
#     # 仮のプロジェクト構造を作成
#     root = tmp_path / "myproj"
#     root.mkdir()
#     (root / ".git").mkdir()
#     subdir = root / "src"
#     subdir.mkdir()

#     # start位置を指定できる設計が望ましい
#     dmanager = DirManager()
#     project_root = dmanager.find_project_root()

#     assert project_root == root
