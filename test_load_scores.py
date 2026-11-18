import runpy
import sys
from pathlib import Path

import pytest

from load_scores import load_scores


def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")

    assert len(kept) == 5


def test_빈_줄은_건너뛴다(tmp_path):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text(
        "name,score\n"
        "가나다,80\n"
        "\n"
        "라마바,90\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(scores_file)

    assert kept == [("가나다", 80), ("라마바", 90)]
    assert skipped == []


def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text('name,score\n"최,네번",77\n', encoding="utf-8")

    kept, skipped = load_scores(scores_file)

    assert kept == [("최,네번", 77)]
    assert skipped == []


def test_이름이_비어_있으면_건너뛴다(tmp_path):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text("name,score\n,80\n", encoding="utf-8")

    kept, skipped = load_scores(scores_file)

    assert kept == []
    assert skipped == [(2, ",80", "이름이 비어 있음")]


def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")

    assert kept == []
    assert skipped == []


def test_직접_실행하면_결과를_출력한다(tmp_path, monkeypatch, capsys):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text(
        "name,score\n"
        "민지,80\n"
        "철수,결석\n",
        encoding="utf-8",
    )
    script = Path(__file__).with_name("load_scores.py")
    monkeypatch.setattr(sys, "argv", [str(script), str(scores_file)])

    runpy.run_path(str(script), run_name="__main__")
    output = capsys.readouterr().out

    assert "읽은 줄 : 1개" in output
    assert "  민지 80" in output
    assert "건너뛴 줄 : 1개" in output
    assert "  3행  철수,결석   ← 점수가 정수가 아님" in output


@pytest.mark.parametrize(
    ("점수", "유효한가"),
    [
        (-1, False),
        (0, True),
        (1, True),
        (99, True),
        (100, True),
        (101, False),
    ],
)
def test_점수_경계값(tmp_path, 점수, 유효한가):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text(f"name,score\n학생,{점수}\n", encoding="utf-8")

    kept, skipped = load_scores(scores_file)

    assert (len(kept) == 1) == 유효한가
