# lootno1

按权重把战利品分配给队伍成员的小工具。

这个仓库同时用作 [dsh-superagent](https://github.com/deepseek-ai/dsh-superagent-prototype)
的试验场：issue 与 pull request 由 agent 处理，用来观察它在真实工作流里的表现。

## 用法

```python
from lootno1 import Member, allocate_proportional

members = [Member("ana", 3), Member("bo", 1), Member("cy", 1)]
allocate_proportional(10, members)
```

`Member` 的 `weight` 表示该成员在分配中的相对权重，默认为 1。
`allocate_proportional(total_items, members)` 返回 `{成员名: 分到的件数}`。

## 测试

```sh
uv run --with pytest python -m pytest tests/ -q
```

若当前解释器已装 pytest，也可直接 `python3 -m pytest tests/ -q`。

## 结构

| 路径 | 内容 |
| --- | --- |
| `lootno1/allocate.py` | 分配逻辑 |
| `tests/test_allocate.py` | 测试 |
