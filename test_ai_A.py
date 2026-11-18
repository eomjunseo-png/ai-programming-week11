import pytest

from load_scores import load_scores


def test_load_scores_keeps_valid_rows_and_score_boundaries(tmp_path):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text(
        "\ufeffname,score\n"
        "  Mina  ,0\n"
        "Mina,100\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(scores_file)

    assert kept == [("Mina", 0), ("Mina", 100)]
    assert skipped == []


def test_load_scores_records_invalid_rows_and_ignores_blank_lines(tmp_path):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text(
        "name,score\n"
        "OnlyOneColumn\n"
        "Bob,\n"
        ",80\n"
        "Cara,not-a-number\n"
        "Dan,-1\n"
        "Eve,101\n"
        "\n"
        " ,90\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(scores_file)

    assert kept == []
    assert skipped == [
        (2, "OnlyOneColumn", "열 개수가 2가 아님"),
        (3, "Bob,", "점수가 비어 있음"),
        (4, ",80", "이름이 비어 있음"),
        (5, "Cara,not-a-number", "점수가 정수가 아님"),
        (6, "Dan,-1", "점수가 0~100 밖"),
        (7, "Eve,101", "점수가 0~100 밖"),
        (9, " ,90", "이름이 비어 있음"),
    ]


def test_load_scores_returns_empty_lists_for_header_only_file(tmp_path):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text("name,score\n", encoding="utf-8")

    assert load_scores(scores_file) == ([], [])


def test_load_scores_propagates_file_not_found(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(missing_file)
