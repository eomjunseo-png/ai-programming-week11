import pytest

from load_scores import load_scores


def test_load_scores_preserves_order_and_accepts_score_boundaries(tmp_path):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text(
        "name,score\n"
        "Mina,0\n"
        "Joon,100\n"
        "Sora,65\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(scores_file)

    assert kept == [("Mina", 0), ("Joon", 100), ("Sora", 65)]
    assert skipped == []


def test_load_scores_records_and_excludes_invalid_rows_and_duplicate_names(tmp_path):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text(
        "name,score\n"
        "Mina,80\n"
        "Joon,\n"
        "Sora,not-a-number\n"
        "Tae,-1\n"
        "Yuna,101\n"
        "Mina,90\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(scores_file)

    assert kept == [("Mina", 80)]
    assert skipped == [
        (3, "Joon,", "점수가 비어 있음"),
        (4, "Sora,not-a-number", "점수가 정수가 아님"),
        (5, "Tae,-1", "점수가 0~100 밖"),
        (6, "Yuna,101", "점수가 0~100 밖"),
        (7, "Mina,90", "중복 이름"),
    ]


def test_load_scores_returns_empty_lists_for_header_only_file(tmp_path):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text("name,score\n", encoding="utf-8")

    assert load_scores(scores_file) == ([], [])


def test_load_scores_propagates_invalid_header_error(tmp_path):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text("student,points\nMina,80\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_scores(scores_file)


def test_load_scores_propagates_file_not_found(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(missing_file)
