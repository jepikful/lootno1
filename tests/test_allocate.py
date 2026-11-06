import pytest

from lootno1 import Member, allocate_proportional


def test_splits_evenly():
    members = [Member("ana"), Member("bo")]
    assert allocate_proportional(10, members) == {"ana": 5, "bo": 5}


def test_respects_weights():
    members = [Member("ana", 2), Member("bo", 1)]
    assert allocate_proportional(9, members) == {"ana": 6, "bo": 3}


def test_single_member_gets_everything():
    assert allocate_proportional(7, [Member("ana")]) == {"ana": 7}


def test_rejects_empty_members():
    with pytest.raises(ValueError):
        allocate_proportional(5, [])


def test_rejects_negative_total():
    with pytest.raises(ValueError):
        allocate_proportional(-1, [Member("ana")])


def test_rejects_zero_total_weight():
    with pytest.raises(ValueError):
        allocate_proportional(5, [Member("ana", 0)])


def test_rejects_negative_weight():
    with pytest.raises(ValueError):
        Member("ana", -1)
