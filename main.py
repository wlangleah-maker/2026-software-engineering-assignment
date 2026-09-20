from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox

from game_logic import GameModel
from levels import GRID_COLS, GRID_ROWS, LEVELS, MAX_MISTAKES

WINDOW_W = 820
WINDOW_H = 720
BOARD_X = 160
BOARD_Y = 155
CELL = 100
BOARD_W = GRID_COLS * CELL
BOARD_H = GRID_ROWS * CELL

BG = "#f3f6fb"
PANEL = "#ffffff"
GRID = "#cad5e2"
PRIMARY = "#2f6fed"
PRIMARY_DARK = "#174ea6"
TEXT = "#203047"
MUTED = "#64748b"
DANGER = "#e5484d"
SUCCESS = "#20a464"
ARROW = "#315f9d"

VECTORS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}


class ArrowGame(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("一箭又一箭")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.level_index = 0
        self.model: GameModel | None = None
        self.animating = False
        self.hit_boxes: dict[int, str] = {}
        self.screen: tk.Frame | None = None
        self.show_start()

    def clear_screen(self) -> tk.Frame:
        if self.screen is not None:
            self.screen.destroy()
        self.screen = tk.Frame(self, bg=BG, width=WINDOW_W, height=WINDOW_H)
        self.screen.pack(fill="both", expand=True)
        return self.screen

    def make_button(self, parent: tk.Widget, text: str, command, width: int = 15) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            font=("Microsoft YaHei UI", 12, "bold"),
            fg="white",
            bg=PRIMARY,
            activebackground=PRIMARY_DARK,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8,
        )

    def show_start(self) -> None:
        frame = self.clear_screen()
        card = tk.Frame(frame, bg=PANEL, highlightbackground="#dfe7f1", highlightthickness=1)
        card.place(x=125, y=90, width=570, height=530)

        tk.Label(card, text="一箭又一箭", font=("Microsoft YaHei UI", 34, "bold"), fg=TEXT, bg=PANEL).pack(pady=(55, 8))
        tk.Label(card, text="观察方向 · 找准顺序 · 清空棋盘", font=("Microsoft YaHei UI", 14), fg=MUTED, bg=PANEL).pack()

        rules = (
            "游戏规则\n\n"
            "1. 点击棋盘中的箭头。\n"
            "2. 前方没有其他箭头时，它会飞出棋盘。\n"
            "3. 前方被阻挡时会晃动，并消耗一次失误机会。\n"
            "4. 清空全部箭头即可进入下一关。"
        )
        tk.Label(card, text=rules, justify="left", font=("Microsoft YaHei UI", 12), fg=TEXT, bg=PANEL).pack(pady=35)
        self.make_button(card, "开始游戏", self.start_game, 18).pack()
        tk.Label(card, text="Python · Tkinter · AIGC 协作开发", font=("Microsoft YaHei UI", 9), fg="#94a3b8", bg=PANEL).pack(side="bottom", pady=24)

    def start_game(self) -> None:
        self.level_index = 0
        self.load_level()

    def load_level(self) -> None:
        level = LEVELS[self.level_index]
        self.model = GameModel(level["arrows"], MAX_MISTAKES)
        self.animating = False
        self.build_game_screen()
        self.redraw()

    def build_game_screen(self) -> None:
        frame = self.clear_screen()
        top = tk.Frame(frame, bg=BG)
        top.pack(fill="x", padx=55, pady=(25, 8))

        level = LEVELS[self.level_index]
        self.level_label = tk.Label(top, text=f"第 {self.level_index + 1} 关  ·  {level['name']}", font=("Microsoft YaHei UI", 18, "bold"), fg=TEXT, bg=BG)
        self.level_label.pack(side="left")
        self.make_button(top, "重新开始", self.restart_level, 10).pack(side="right")
        tk.Button(top, text="返回首页", command=self.show_start, font=("Microsoft YaHei UI", 11), fg=MUTED, bg=BG, relief="flat", cursor="hand2").pack(side="right", padx=15)

        status = tk.Frame(frame, bg=BG)
        status.pack(fill="x", padx=60)
        self.remaining_label = tk.Label(status, font=("Microsoft YaHei UI", 12, "bold"), fg=TEXT, bg=BG)
        self.remaining_label.pack(side="left")
        self.message_label = tk.Label(status, text="选择一个没有被阻挡的箭头", font=("Microsoft YaHei UI", 11), fg=MUTED, bg=BG)
        self.message_label.pack(side="left", expand=True)
        self.mistakes_label = tk.Label(status, font=("Microsoft YaHei UI", 12, "bold"), fg=DANGER, bg=BG)
        self.mistakes_label.pack(side="right")

        self.canvas = tk.Canvas(frame, width=WINDOW_W, height=570, bg=BG, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

    def restart_level(self) -> None:
        if self.model is None:
            return
        self.model.reset()
        self.animating = False
        self.message_label.config(text="本关已重新开始", fg=MUTED)
        self.redraw()

    def board_center(self, row: int, col: int) -> tuple[float, float]:
        return BOARD_X + col * CELL + CELL / 2, BOARD_Y + row * CELL + CELL / 2

    def draw_arrow(self, x: float, y: float, direction: str, color: str, offset_x: float = 0, offset_y: float = 0) -> list[int]:
        dx, dy = VECTORS[direction]
        px, py = -dy, dx
        x += offset_x
        y += offset_y
        tail_x, tail_y = x - dx * 25, y - dy * 25
        tip_x, tip_y = x + dx * 28, y + dy * 28
        neck_x, neck_y = x + dx * 9, y + dy * 9
        items = [
            self.canvas.create_line(tail_x, tail_y, neck_x, neck_y, fill=color, width=9, capstyle=tk.ROUND),
            self.canvas.create_polygon(
                tip_x, tip_y,
                neck_x + px * 17, neck_y + py * 17,
                neck_x - px * 17, neck_y - py * 17,
                fill=color,
                outline=color,
            ),
        ]
        return items

    def redraw(self, animated_id: str | None = None, offset=(0, 0), animated_color: str | None = None) -> None:
        if self.model is None:
            return
        self.canvas.delete("all")
        self.hit_boxes.clear()

        self.canvas.create_rectangle(BOARD_X - 12, BOARD_Y - 12, BOARD_X + BOARD_W + 12, BOARD_Y + BOARD_H + 12, fill="#dce6f2", outline="")
        self.canvas.create_rectangle(BOARD_X, BOARD_Y, BOARD_X + BOARD_W, BOARD_Y + BOARD_H, fill=PANEL, outline="#aebed0", width=2)
        for row in range(GRID_ROWS + 1):
            y = BOARD_Y + row * CELL
            self.canvas.create_line(BOARD_X, y, BOARD_X + BOARD_W, y, fill=GRID)
        for col in range(GRID_COLS + 1):
            x = BOARD_X + col * CELL
            self.canvas.create_line(x, BOARD_Y, x, BOARD_Y + BOARD_H, fill=GRID)

        for arrow in self.model.arrows.values():
            x, y = self.board_center(arrow.row, arrow.col)
            color = animated_color if arrow.id == animated_id and animated_color else ARROW
            dx, dy = offset if arrow.id == animated_id else (0, 0)
            self.draw_arrow(x, y, arrow.direction, color, dx, dy)
            box = self.canvas.create_rectangle(x - 38, y - 38, x + 38, y + 38, fill="", outline="")
            self.hit_boxes[box] = arrow.id

        self.remaining_label.config(text=f"剩余箭头：{self.model.remaining}")
        hearts = "● " * self.model.mistakes_left + "○ " * (self.model.max_mistakes - self.model.mistakes_left)
        self.mistakes_label.config(text=f"失误机会：{hearts.strip()}")

    def locate_arrow(self, x: float, y: float) -> str | None:
        if self.model is None:
            return None
        for arrow in self.model.arrows.values():
            cx, cy = self.board_center(arrow.row, arrow.col)
            if abs(x - cx) <= 40 and abs(y - cy) <= 40:
                return arrow.id
        return None

    def on_click(self, event) -> None:
        if self.animating or self.model is None or self.model.failed or self.model.won:
            return
        arrow_id = self.locate_arrow(event.x, event.y)
        if arrow_id is None:
            return
        if self.model.is_blocked(arrow_id):
            self.model.click(arrow_id)
            self.message_label.config(text="前方有阻挡！失误机会 -1", fg=DANGER)
            self.animate_collision(arrow_id)
        else:
            self.message_label.config(text="路径畅通，箭头飞出！", fg=SUCCESS)
            self.animate_exit(arrow_id)

    def animate_collision(self, arrow_id: str) -> None:
        if self.model is None or arrow_id not in self.model.arrows:
            return
        self.animating = True
        arrow = self.model.arrows[arrow_id]
        dx, dy = VECTORS[arrow.direction]
        frames = 18

        def step(i: int) -> None:
            if self.model is None:
                return
            if i >= frames:
                self.animating = False
                self.redraw()
                if self.model.failed:
                    self.after(120, self.show_failure)
                return
            progress = i / frames
            amount = math.sin(progress * math.pi * 6) * 8 * (1 - progress)
            self.redraw(arrow_id, (dx * amount, dy * amount), DANGER)
            self.after(22, lambda: step(i + 1))

        step(0)

    def animate_exit(self, arrow_id: str) -> None:
        if self.model is None or arrow_id not in self.model.arrows:
            return
        self.animating = True
        arrow = self.model.arrows[arrow_id]
        dx, dy = VECTORS[arrow.direction]
        frames = 22

        def step(i: int) -> None:
            if self.model is None:
                return
            if i >= frames:
                result = self.model.click(arrow_id)
                self.animating = False
                self.redraw()
                if result == "won":
                    self.after(180, self.show_success)
                return
            progress = i / frames
            distance = progress * 650
            self.redraw(arrow_id, (dx * distance, dy * distance), SUCCESS)
            self.after(16, lambda: step(i + 1))

        step(0)

    def show_modal(self, title: str, detail: str, color: str, button_text: str, command) -> None:
        overlay = tk.Frame(self.screen, bg="#dce5f1")
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        card = tk.Frame(overlay, bg=PANEL, highlightbackground="#cbd7e5", highlightthickness=1)
        card.place(x=185, y=175, width=450, height=340)
        tk.Label(card, text=title, font=("Microsoft YaHei UI", 30, "bold"), fg=color, bg=PANEL).pack(pady=(55, 15))
        tk.Label(card, text=detail, font=("Microsoft YaHei UI", 13), fg=TEXT, bg=PANEL, justify="center").pack(pady=12)
        self.make_button(card, button_text, command, 16).pack(pady=25)

    def show_failure(self) -> None:
        self.show_modal("挑战失败", "失误机会已经用完。\n调整顺序，再试一次吧！", DANGER, "重新开始", self.load_level)

    def show_success(self) -> None:
        if self.level_index + 1 < len(LEVELS):
            def next_level() -> None:
                self.level_index += 1
                self.load_level()
            self.show_modal("本关通过", f"成功清空第 {self.level_index + 1} 关的全部箭头！", SUCCESS, "进入下一关", next_level)
        else:
            self.show_modal("全部通关", "恭喜你完成全部 3 个关卡！", SUCCESS, "返回首页", self.show_start)


if __name__ == "__main__":
    try:
        ArrowGame().mainloop()
    except tk.TclError as exc:
        messagebox.showerror("启动失败", f"无法创建图形界面：{exc}")
