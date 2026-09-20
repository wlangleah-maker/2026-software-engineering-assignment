from game_logic import Arrow

GRID_ROWS = 5
GRID_COLS = 5
MAX_MISTAKES = 3

LEVELS = [
    {
        "name": "樱色启程",
        "subtitle": "从棋盘边缘开始熟悉四种方向",
        "arrows": [
            Arrow("L1-A", 0, 2, "up"),
            Arrow("L1-B", 2, 0, "left"),
            Arrow("L1-C", 2, 4, "right"),
            Arrow("L1-D", 4, 2, "down"),
        ],
    },
    {
        "name": "云端序曲",
        "subtitle": "先移除外侧箭头，再处理被阻挡者",
        "arrows": [
            Arrow("L2-A", 0, 2, "up"),
            Arrow("L2-B", 1, 2, "left"),
            Arrow("L2-C", 1, 0, "left"),
            Arrow("L2-D", 3, 1, "down"),
            Arrow("L2-E", 4, 1, "down"),
            Arrow("L2-F", 2, 4, "right"),
        ],
    },
    {
        "name": "星光交错",
        "subtitle": "观察同行同列间的多重阻挡",
        "arrows": [
            Arrow("L3-A", 0, 1, "up"),
            Arrow("L3-B", 1, 1, "left"),
            Arrow("L3-C", 1, 0, "left"),
            Arrow("L3-D", 2, 0, "left"),
            Arrow("L3-E", 2, 2, "right"),
            Arrow("L3-F", 2, 4, "right"),
            Arrow("L3-G", 4, 3, "down"),
            Arrow("L3-H", 3, 3, "up"),
            Arrow("L3-I", 0, 3, "right"),
        ],
    },
    {
        "name": "月夜回廊",
        "subtitle": "拆解横纵交织的箭头链",
        "arrows": [
            Arrow("L4-A", 0, 2, "up"),
            Arrow("L4-B", 1, 2, "left"),
            Arrow("L4-C", 1, 0, "left"),
            Arrow("L4-D", 2, 1, "up"),
            Arrow("L4-E", 2, 3, "right"),
            Arrow("L4-F", 2, 4, "right"),
            Arrow("L4-G", 3, 0, "left"),
            Arrow("L4-H", 3, 3, "down"),
            Arrow("L4-I", 4, 3, "down"),
            Arrow("L4-J", 4, 1, "down"),
        ],
    },
    {
        "name": "银河终章",
        "subtitle": "最终挑战：冷静寻找最外层突破口",
        "arrows": [
            Arrow("L5-A", 0, 0, "up"),
            Arrow("L5-B", 0, 2, "left"),
            Arrow("L5-C", 0, 4, "right"),
            Arrow("L5-D", 1, 0, "left"),
            Arrow("L5-E", 1, 2, "up"),
            Arrow("L5-F", 1, 4, "right"),
            Arrow("L5-G", 2, 0, "left"),
            Arrow("L5-H", 2, 2, "right"),
            Arrow("L5-I", 2, 4, "right"),
            Arrow("L5-J", 3, 0, "left"),
            Arrow("L5-K", 3, 2, "down"),
            Arrow("L5-L", 3, 4, "right"),
            Arrow("L5-M", 4, 1, "down"),
            Arrow("L5-N", 4, 3, "down"),
        ],
    },
]
