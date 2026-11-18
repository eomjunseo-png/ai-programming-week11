import pytest

from bug3_logic import count_pass, find_max


def test_find_max_returns_largest_score():
    assert find_max([70, 85, 60, 95]) == 95


def test_find_max_handles_first_and_only_score():
    assert find_max([95, 85, 70, 60]) == 95
    assert find_max([42]) == 42


def test_find_max_raises_for_empty_scores():
    with pytest.raises(IndexError):
        find_max([])


def test_count_pass_includes_scores_at_cutoff():
    assert count_pass([60, 60, 59]) == 2


def test_count_pass_uses_custom_cutoff():
    assert count_pass([69, 70, 71], cutoff=70) == 2


def test_count_pass_returns_zero_for_empty_scores():
    assert count_pass([]) == 0
