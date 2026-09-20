from game_logic import Arrow

GRID_ROWS = 5
GRID_COLS = 5
MAX_MISTAKES = 3

LEVELS = [
    {
        "name": "初识箭头",
        "arrows": [
            Arrow("L1-A", 0, 2, "up"),
            Arrow("L1-B", 2, 0, "left"),
            Arrow("L1-C", 2, 4, "right"),
            Arrow("L1-D", 4, 2, "down"),
        ],
    },
    {
        "name": "先外后内",
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
        "name": "交错迷阵",
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
]
