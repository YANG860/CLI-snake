from collections import deque
from inputimeout import inputimeout, TimeoutOccurred
from dataclasses import dataclass
from random import randint
import os

@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash(self.x) + hash(self.y)

class Snake:
    def __init__(self, head_posi: Position, rows: int, cols: int):
        self.body = deque([head_posi])
        self.last_move = "w"  # 初始方向
        self.rows = rows
        self.cols = cols

    def is_crashed(self):
        return len(self.body) > len(set(self.body))

    def move_head(self, move: str):
        """移动蛇头"""
        head_posi = self.body[0]

        match move:
            case "w":
                new_head = Position((head_posi.x - 1) % self.rows, head_posi.y)
            case "s":
                new_head = Position((head_posi.x + 1) % self.rows, head_posi.y)
            case "a":
                new_head = Position(head_posi.x, (head_posi.y - 1) % self.cols)
            case "d":
                new_head = Position(head_posi.x, (head_posi.y + 1) % self.cols)
            case _:
                new_head = head_posi

        self.body.appendleft(new_head)

    def remove_tail(self):
        self.body.pop()

class Main:
    def __init__(self, rows, cols, speed):
        self.rows = rows
        self.cols = cols
        self.speed = speed
        self.map = [["⬜" for _ in range(self.cols)] for _ in range(self.rows)]

    def gen_apple(self, snake: Snake):
        while True:
            apple_posi = Position(randint(0, self.rows - 1), randint(0, self.cols - 1))
            if apple_posi not in snake.body:
                self.apple = apple_posi
                break

    def render_snake(self, snake: Snake):
        for i, pos in enumerate(snake.body):
            self.map[pos.x][pos.y] = "❎" if i == 0 else "🟩"

    def render_apple(self):
        self.map[self.apple.x][self.apple.y] = "🟥"

    def show_map(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.map:
            print("".join(row))

    def clear_map(self):
        self.map = [["⬜" for _ in range(self.cols)] for _ in range(self.rows)]

    def next_move(self, snake: Snake):
        try:
            move = inputimeout("", self.speed)
            if move not in ["w", "s", "a", "d"]:
                move = snake.last_move
            else:
                # 检查新方向是否与 last_move 相反
                opposite_directions = {
                    "w": "s",
                    "s": "w",
                    "a": "d",
                    "d": "a",
                }
                if opposite_directions.get(snake.last_move) == move:
                    # 如果方向相反，则忽略此次输入，保持原方向
                    move = snake.last_move
                else:
                    # 否则更新方向
                    snake.last_move = move
        except TimeoutOccurred:
            move = snake.last_move

        snake.move_head(move)

        if self.apple in snake.body:
            self.gen_apple(snake)
        else:
            snake.remove_tail()

class Message:
    @staticmethod
    def start(game: Main):
        print("贪吃蛇")
        print("请对齐以下框架")
        game.show_map()
        input("按任意键继续")

    @staticmethod
    def end():
        print("游戏结束")

if __name__ == "__main__":
    ROWS = int(input("请输入行数: "))
    COLS = int(input("请输入列数: "))
    SPEED = float(input("请输入游戏速度（秒）: "))

    game = Main(ROWS, COLS, SPEED)
    Message.start(game)

    snake = Snake(Position(ROWS // 2, COLS // 2), ROWS, COLS)
    game.gen_apple(snake)

    while not snake.is_crashed():
        game.next_move(snake)
        game.clear_map()
        game.render_snake(snake)
        game.render_apple()
        game.show_map()

    Message.end()