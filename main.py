from __future__ import annotations

import math
import random
import tkinter as tk
from tkinter import messagebox

from game_logic import GameModel
from levels import GRID_COLS, GRID_ROWS, LEVELS, MAX_MISTAKES

WINDOW_W, WINDOW_H = 900, 790
BOARD_X, BOARD_Y = 200, 32
CELL = 100
BOARD_W, BOARD_H = GRID_COLS * CELL, GRID_ROWS * CELL

BG = "#fff4fb"
PANEL = "#fffafd"
GRID = "#ead9ec"
PRIMARY = "#8b6de8"
PRIMARY_DARK = "#6750c5"
PINK = "#f08fbd"
CYAN = "#64c9d4"
TEXT = "#4b4163"
MUTED = "#887d9d"
DANGER = "#ec6680"
SUCCESS = "#54b99a"
ARROW_COLORS = ["#8069df", "#eb7fb0", "#57bcca", "#f1a35d"]
VECTORS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


class ArrowGame(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("一箭又一箭 · 星愿篇")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.minsize(WINDOW_W, WINDOW_H)
        self.resizable(True, True)
        self.configure(bg=BG)
        self.level_index = 0
        self.model: GameModel | None = None
        self.animating = False
        self.screen: tk.Frame | None = None
        self.level_scores: list[int] = []
        self.level_stars: list[int] = []
        self.show_start()

    def clear_screen(self) -> tk.Frame:
        if self.screen is not None:
            self.screen.destroy()
        self.screen = tk.Frame(self, bg=BG)
        self.screen.pack(fill="both", expand=True)
        return self.screen

    def decorate(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(-90, -70, 260, 210, fill="#fbd7e9", outline="")
        canvas.create_oval(690, -80, 1030, 230, fill="#dcd7ff", outline="")
        canvas.create_oval(700, 590, 1040, 900, fill="#d9f5f2", outline="")
        for x, y, size, color in [(85, 300, 5, PINK), (760, 300, 7, PRIMARY), (110, 650, 6, CYAN), (810, 570, 5, PINK), (725, 90, 5, "#f4b95f")]:
            self.draw_star(canvas, x, y, size, color)

    @staticmethod
    def draw_star(canvas: tk.Canvas, x: float, y: float, r: float, color: str) -> None:
        pts = []
        for i in range(10):
            angle = -math.pi / 2 + i * math.pi / 5
            radius = r if i % 2 == 0 else r * .42
            pts.extend((x + math.cos(angle) * radius, y + math.sin(angle) * radius))
        canvas.create_polygon(*pts, fill=color, outline="")

    def make_button(self, parent, text, command, width=15, secondary=False):
        bg = "#efe9fb" if secondary else PRIMARY
        fg = TEXT if secondary else "white"
        return tk.Button(parent, text=text, command=command, width=width,
                         font=("Microsoft YaHei UI", 11, "bold"), fg=fg, bg=bg,
                         activebackground=PRIMARY_DARK if not secondary else "#e4daf8",
                         activeforeground="white" if not secondary else TEXT,
                         relief="flat", cursor="hand2", padx=12, pady=8)

    def show_start(self) -> None:
        frame = self.clear_screen()
        bg_canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
        bg_canvas.pack(fill="both", expand=True)
        self.decorate(bg_canvas)
        bg_canvas.create_oval(340, 70, 560, 290, fill="#fff8fc", outline="#f4c8dc", width=3)
        bg_canvas.create_arc(382, 116, 518, 252, start=20, extent=140, style=tk.ARC, outline=PINK, width=5)
        bg_canvas.create_oval(410, 147, 425, 166, fill=TEXT, outline="")
        bg_canvas.create_oval(475, 147, 490, 166, fill=TEXT, outline="")
        bg_canvas.create_arc(438, 165, 462, 190, start=200, extent=140, style=tk.ARC, outline=PINK, width=3)
        bg_canvas.create_polygon(360, 105, 395, 58, 420, 115, fill="#fff8fc", outline="#f4c8dc", width=3)
        bg_canvas.create_polygon(480, 115, 505, 58, 540, 105, fill="#fff8fc", outline="#f4c8dc", width=3)

        card = tk.Frame(frame, bg=PANEL, highlightbackground="#f0d8e7", highlightthickness=2)
        card.place(relx=.5, y=315, anchor="n", width=610, height=390)
        tk.Label(card, text="一箭又一箭", font=("Microsoft YaHei UI", 35, "bold"), fg=PRIMARY, bg=PANEL).pack(pady=(35, 0))
        tk.Label(card, text="✦ 星 愿 篇 ✦", font=("Microsoft YaHei UI", 14, "bold"), fg=PINK, bg=PANEL).pack(pady=4)
        tk.Label(card, text="观察箭头的方向与阻挡关系，按正确顺序让它们飞向星空。",
                 font=("Microsoft YaHei UI", 12), fg=MUTED, bg=PANEL).pack(pady=18)
        tk.Label(card, text="5 个关卡  ·  每关星级评价  ·  最终通关纪念画面",
                 font=("Microsoft YaHei UI", 11, "bold"), fg=CYAN, bg=PANEL).pack(pady=6)
        self.make_button(card, "开始冒险  ✦", self.start_game, 19).pack(pady=22)
        tk.Label(card, text="提示：前方没有其他箭头时才能安全飞出",
                 font=("Microsoft YaHei UI", 9), fg="#a499b4", bg=PANEL).pack()

    def start_game(self) -> None:
        self.level_index = 0
        self.level_scores = []
        self.level_stars = []
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
        top.pack(fill="x", padx=45, pady=(18, 4))
        level = LEVELS[self.level_index]
        title_box = tk.Frame(top, bg=BG)
        title_box.pack(side="left")
        self.level_label = tk.Label(title_box, text=f"STAGE {self.level_index + 1} / {len(LEVELS)}  ·  {level['name']}",
                                    font=("Microsoft YaHei UI", 18, "bold"), fg=PRIMARY, bg=BG)
        self.level_label.pack(anchor="w")
        tk.Label(title_box, text=level["subtitle"], font=("Microsoft YaHei UI", 9), fg=MUTED, bg=BG).pack(anchor="w")
        self.make_button(top, "重新开始", self.restart_level, 10).pack(side="right")
        self.make_button(top, "返回首页", self.show_start, 10, True).pack(side="right", padx=10)

        status = tk.Frame(frame, bg="#fffafd", highlightbackground="#efdaea", highlightthickness=1)
        status.pack(fill="x", padx=48, pady=(8, 0), ipady=8)
        self.remaining_label = tk.Label(status, font=("Microsoft YaHei UI", 11, "bold"), fg=TEXT, bg="#fffafd")
        self.remaining_label.pack(side="left", padx=18)
        self.message_label = tk.Label(status, text="找出没有被阻挡的箭头吧 ✦", font=("Microsoft YaHei UI", 10), fg=MUTED, bg="#fffafd")
        self.message_label.pack(side="left", expand=True)
        self.mistakes_label = tk.Label(status, font=("Microsoft YaHei UI", 12, "bold"), fg=DANGER, bg="#fffafd")
        self.mistakes_label.pack(side="right", padx=18)

        self.canvas = tk.Canvas(frame, width=WINDOW_W, height=610, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_click)

    def restart_level(self) -> None:
        if self.model:
            self.model.reset()
            self.animating = False
            self.message_label.config(text="时间回溯，本关重新开始 ✦", fg=MUTED)
            self.redraw()

    def board_center(self, row, col):
        return BOARD_X + col * CELL + CELL / 2, BOARD_Y + row * CELL + CELL / 2

    def draw_arrow(self, x, y, direction, color, ox=0, oy=0):
        dx, dy = VECTORS[direction]
        px, py = -dy, dx
        x, y = x + ox, y + oy
        tail_x, tail_y = x - dx * 25, y - dy * 25
        tip_x, tip_y = x + dx * 28, y + dy * 28
        neck_x, neck_y = x + dx * 9, y + dy * 9
        self.canvas.create_oval(x - 34, y - 34, x + 34, y + 34, fill="#fffafd", outline="#eadcf0", width=2)
        self.canvas.create_line(tail_x, tail_y, neck_x, neck_y, fill=color, width=9, capstyle=tk.ROUND)
        self.canvas.create_polygon(tip_x, tip_y, neck_x + px*17, neck_y + py*17,
                                   neck_x - px*17, neck_y - py*17, fill=color, outline=color)
        self.canvas.create_oval(tail_x-4, tail_y-4, tail_x+4, tail_y+4, fill="#fff", outline="")

    def redraw(self, animated_id=None, offset=(0, 0), animated_color=None) -> None:
        if not self.model:
            return
        self.canvas.delete("all")
        self.canvas.create_oval(15, 40, 145, 100, fill="#fff", outline="")
        self.canvas.create_oval(80, 25, 210, 105, fill="#fff", outline="")
        self.canvas.create_oval(690, 470, 840, 545, fill="#e8f8f7", outline="")
        for sx, sy in [(95, 175), (770, 115), (115, 500), (785, 380)]:
            self.draw_star(self.canvas, sx, sy, 7, "#efafd0")

        self.canvas.create_rectangle(BOARD_X-16, BOARD_Y-16, BOARD_X+BOARD_W+16, BOARD_Y+BOARD_H+16,
                                     fill="#e8dff7", outline="")
        self.canvas.create_rectangle(BOARD_X-8, BOARD_Y-8, BOARD_X+BOARD_W+8, BOARD_Y+BOARD_H+8,
                                     fill="#fffafd", outline="#d5bce9", width=3)
        self.canvas.create_rectangle(BOARD_X, BOARD_Y, BOARD_X+BOARD_W, BOARD_Y+BOARD_H,
                                     fill="#fffbfe", outline="#d8c7e4", width=2)
        for r in range(GRID_ROWS + 1):
            y = BOARD_Y + r * CELL
            self.canvas.create_line(BOARD_X, y, BOARD_X+BOARD_W, y, fill=GRID)
        for c in range(GRID_COLS + 1):
            x = BOARD_X + c * CELL
            self.canvas.create_line(x, BOARD_Y, x, BOARD_Y+BOARD_H, fill=GRID)

        for arrow in self.model.arrows.values():
            x, y = self.board_center(arrow.row, arrow.col)
            base = ARROW_COLORS[(arrow.row + arrow.col) % len(ARROW_COLORS)]
            color = animated_color if arrow.id == animated_id and animated_color else base
            dx, dy = offset if arrow.id == animated_id else (0, 0)
            self.draw_arrow(x, y, arrow.direction, color, dx, dy)

        self.remaining_label.config(text=f"✦ 剩余 {self.model.remaining} 支")
        hearts = "♥ " * self.model.mistakes_left + "♡ " * (self.model.max_mistakes-self.model.mistakes_left)
        self.mistakes_label.config(text=f"失误机会  {hearts.strip()}")

    def locate_arrow(self, x, y):
        if not self.model:
            return None
        for arrow in self.model.arrows.values():
            cx, cy = self.board_center(arrow.row, arrow.col)
            if abs(x-cx) <= 40 and abs(y-cy) <= 40:
                return arrow.id
        return None

    def on_click(self, event) -> None:
        if self.animating or not self.model or self.model.failed or self.model.won:
            return
        arrow_id = self.locate_arrow(event.x, event.y)
        if not arrow_id:
            return
        if self.model.is_blocked(arrow_id):
            self.model.click(arrow_id)
            self.message_label.config(text="被挡住了！失误机会 -1", fg=DANGER)
            self.animate_collision(arrow_id)
        else:
            self.message_label.config(text="路径畅通，向星空出发！", fg=SUCCESS)
            self.animate_exit(arrow_id)

    def animate_collision(self, arrow_id) -> None:
        if not self.model or arrow_id not in self.model.arrows:
            return
        self.animating = True
        arrow = self.model.arrows[arrow_id]
        dx, dy = VECTORS[arrow.direction]
        def step(i):
            if i >= 18:
                self.animating = False
                self.redraw()
                if self.model and self.model.failed:
                    self.after(120, self.show_failure)
                return
            p = i/18
            amount = math.sin(p*math.pi*6)*8*(1-p)
            self.redraw(arrow_id, (dx*amount, dy*amount), DANGER)
            self.after(22, lambda: step(i+1))
        step(0)

    def animate_exit(self, arrow_id) -> None:
        if not self.model or arrow_id not in self.model.arrows:
            return
        self.animating = True
        arrow = self.model.arrows[arrow_id]
        dx, dy = VECTORS[arrow.direction]
        def step(i):
            if i >= 22:
                result = self.model.click(arrow_id)
                self.animating = False
                self.redraw()
                if result == "won":
                    self.after(180, self.show_level_result)
                return
            p = i/22
            self.redraw(arrow_id, (dx*p*650, dy*p*650), SUCCESS)
            self.after(16, lambda: step(i+1))
        step(0)

    def modal_base(self):
        overlay = tk.Frame(self.screen, bg="#eadff0")
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        card = tk.Frame(overlay, bg=PANEL, highlightbackground="#e0c7e8", highlightthickness=2)
        card.place(relx=.5, rely=.5, anchor="center", width=520, height=460)
        return overlay, card

    def show_failure(self) -> None:
        _, card = self.modal_base()
        tk.Label(card, text="☁", font=("Segoe UI Symbol", 55), fg="#b9aecb", bg=PANEL).pack(pady=(35, 0))
        tk.Label(card, text="挑战失败", font=("Microsoft YaHei UI", 29, "bold"), fg=DANGER, bg=PANEL).pack()
        tk.Label(card, text=f"第 {self.level_index+1} 关的失误机会已经用完\n别灰心，重新观察箭头的阻挡关系吧！",
                 font=("Microsoft YaHei UI", 12), fg=TEXT, bg=PANEL, justify="center").pack(pady=22)
        self.make_button(card, "重新挑战", self.load_level, 16).pack(pady=6)
        self.make_button(card, "返回首页", self.show_start, 16, True).pack(pady=6)

    def show_level_result(self) -> None:
        mistakes = MAX_MISTAKES - self.model.mistakes_left
        stars = max(1, 3-mistakes)
        score = 100 - mistakes*20
        self.level_stars.append(stars)
        self.level_scores.append(score)
        if self.level_index == len(LEVELS)-1:
            self.show_final_clear()
            return
        _, card = self.modal_base()
        tk.Label(card, text="关卡完成！", font=("Microsoft YaHei UI", 29, "bold"), fg=SUCCESS, bg=PANEL).pack(pady=(48, 10))
        tk.Label(card, text="★ "*stars + "☆ "*(3-stars), font=("Segoe UI Symbol", 34), fg="#f3ad45", bg=PANEL).pack()
        tk.Label(card, text=f"本关评分  {score} 分", font=("Microsoft YaHei UI", 17, "bold"), fg=PRIMARY, bg=PANEL).pack(pady=8)
        comment = ["完美通关，闪耀如星！", "表现不错，再接再厉！", "成功过关，下次会更好！"][3-stars]
        tk.Label(card, text=comment, font=("Microsoft YaHei UI", 11), fg=MUTED, bg=PANEL).pack(pady=5)
        def next_level():
            self.level_index += 1
            self.load_level()
        self.make_button(card, "进入下一关  →", next_level, 18).pack(pady=30)

    def show_final_clear(self) -> None:
        frame = self.clear_screen()
        canvas = tk.Canvas(frame, bg="#f8f1ff", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.decorate(canvas)
        random.seed(7)
        for _ in range(55):
            x, y = random.randint(40, 860), random.randint(30, 740)
            self.draw_star(canvas, x, y, random.randint(3, 8), random.choice([PINK, CYAN, "#f3b34f", PRIMARY]))
        total_score = sum(self.level_scores)
        total_stars = sum(self.level_stars)
        canvas.create_oval(290, 55, 610, 375, fill="#fffafd", outline="#dcc7f2", width=4)
        canvas.create_text(450, 130, text="✦", font=("Segoe UI Symbol", 55), fill="#f1ad43")
        canvas.create_text(450, 215, text="银河终章 完成", font=("Microsoft YaHei UI", 31, "bold"), fill=PRIMARY)
        canvas.create_text(450, 270, text="所有箭头都已飞向星空！", font=("Microsoft YaHei UI", 14), fill=TEXT)
        canvas.create_text(450, 325, text="★ "*total_stars + "☆ "*(15-total_stars), font=("Segoe UI Symbol", 16), fill="#f0a83d", width=290)
        card = tk.Frame(frame, bg=PANEL, highlightbackground="#ead5ef", highlightthickness=2)
        card.place(relx=.5, y=410, anchor="n", width=540, height=280)
        tk.Label(card, text="最终通关纪念", font=("Microsoft YaHei UI", 20, "bold"), fg=PINK, bg=PANEL).pack(pady=(25, 10))
        tk.Label(card, text=f"总评分  {total_score} / {len(LEVELS)*100}", font=("Microsoft YaHei UI", 25, "bold"), fg=PRIMARY, bg=PANEL).pack()
        tk.Label(card, text=f"收集星星  {total_stars} / {len(LEVELS)*3}", font=("Microsoft YaHei UI", 14), fg=TEXT, bg=PANEL).pack(pady=8)
        tk.Label(card, text="恭喜完成全部五个关卡，愿每支箭都抵达心中的方向。",
                 font=("Microsoft YaHei UI", 10), fg=MUTED, bg=PANEL).pack(pady=8)
        self.make_button(card, "再次挑战", self.start_game, 16).pack(pady=10)


if __name__ == "__main__":
    try:
        ArrowGame().mainloop()
    except tk.TclError as exc:
        messagebox.showerror("启动失败", f"无法创建图形界面：{exc}")
