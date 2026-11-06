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

    先按权重取整分配，剩下的物品按各成员的小数部分从大到小依次补 1 件；
    小数部分相同时按 ``members`` 的输入顺序优先。因此无论权重能否整除
    ``total_items``，分出的件数之和总等于 ``total_items``。

    返回 ``{成员名: 分到的件数}``。
    """
    if total_items < 0:
        raise ValueError("物品总数不能为负")
    if not members:
        raise ValueError("至少需要一名成员")

    total_weight = sum(member.weight for member in members)
    if total_weight <= 0:
        raise ValueError("权重之和必须为正")

    # 用整数余数表示小数部分：分母都是 total_weight，余数大即小数部分大。
    shares = [
        total_items * member.weight // total_weight for member in members
    ]
    remainders = [
        total_items * member.weight % total_weight for member in members
    ]

    leftover = total_items - sum(shares)
    # 余数大的先补；余数相同时 ``i`` 保证沿用输入顺序。
    order = sorted(range(len(members)), key=lambda i: (-remainders[i], i))
    for i in order[:leftover]:
        shares[i] += 1

    return {member.name: shares[i] for i, member in enumerate(members)}
