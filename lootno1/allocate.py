"""按权重把物品分配给队伍成员。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Member:
    """一名参与分配的成员。"""

    name: str
    weight: int = 1

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("成员名不能为空")
        if self.weight < 0:
            raise ValueError(f"权重不能为负：{self.name}")


def allocate_proportional(total_items: int, members: list) -> dict:
    """把 ``total_items`` 件物品按权重分给 ``members``。

    返回 ``{成员名: 分到的件数}``。
    """
    if total_items < 0:
        raise ValueError("物品总数不能为负")
    if not members:
        raise ValueError("至少需要一名成员")

    total_weight = sum(member.weight for member in members)
    if total_weight <= 0:
        raise ValueError("权重之和必须为正")

    return {
        member.name: total_items * member.weight // total_weight
        for member in members
    }
