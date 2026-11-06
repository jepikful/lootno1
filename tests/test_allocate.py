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


def test_fills_all_items_when_weights_do_not_divide_evenly():
    # 3:1 分 10 件：取整后是 7 + 2，余 1 件按小数部分补回（两人小数部分相同，
    # 按输入顺序补给 ana）。
    members = [Member("ana", 3), Member("bo", 1)]
    allocation = allocate_proportional(10, members)
    assert allocation == {"ana": 8, "bo": 2}
    assert sum(allocation.values()) == 10


def test_leftover_goes_to_the_largest_fraction_first():
    # 1:2:3 分 8 件：取整为 1/2/4，余 1 件；bo 的小数部分最大，补给 bo。
    members = [Member("ana", 1), Member("bo", 2), Member("cy", 3)]
    assert allocate_proportional(8, members) == {"ana": 1, "bo": 3, "cy": 4}


def test_leftover_can_fill_several_members():
    # 1:1:1 分 11 件：取整为 3/3/3，余 2 件；三人小数部分相同，按输入顺序补。
    members = [Member("ana"), Member("bo"), Member("cy")]
    assert allocate_proportional(11, members) == {"ana": 4, "bo": 4, "cy": 3}


def test_ties_follow_input_order_not_name_order():
    # 两人权重相同、只分 1 件时，补给输入顺序里靠前的人。
    members = [Member("zeta"), Member("alpha")]
    assert allocate_proportional(1, members) == {"zeta": 1, "alpha": 0}


@pytest.mark.parametrize("total_items", [0, 1, 2, 3, 5, 7, 10, 11, 37, 100])
def test_allocates_exactly_total_items_for_any_total(total_items):
    members = [Member("ana", 3), Member("bo", 1), Member("cy", 5)]
    allocation = allocate_proportional(total_items, members)
    assert sum(allocation.values()) == total_items


@pytest.mark.parametrize("total_items", [0, 1, 4, 7, 10, 23])
def test_each_member_stays_between_floor_and_ceil_of_exact_share(total_items):
    members = [Member("ana", 3), Member("bo", 1), Member("cy", 5)]
    total_weight = sum(member.weight for member in members)
    allocation = allocate_proportional(total_items, members)
    for member in members:
        weighted = total_items * member.weight
        assert weighted // total_weight <= allocation[member.name]
        assert allocation[member.name] <= -(-weighted // total_weight)
