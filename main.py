from inputimeout import inputimeout, TimeoutOccurred
from dataclasses import dataclass
from random import randint
from os import system


@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash(self.x) + hash(self.y)


class Snake:
    "蛇的状态管理类"

    def __init__(self, head_posi: Position, rows, cols):
        self.body = [head_posi]
        self.last_move = "w"
        self.rows = rows
        self.cols = cols

    def is_crashed(self):
        return len(self.body) > len(set(self.body))

    def move_head(self, move: str):
        head_posi: Position = self.body[0]
        match move:
            case "w":
                self.body.insert(
                    0, Position((head_posi.x - 1) % self.rows, head_posi.y)
                )
            case "s":
                self.body.insert(
                    0, Position((head_posi.x + 1) % self.rows, head_posi.y)
                )
            case "a":
                self.body.insert(
                    0, Position(head_posi.x, (head_posi.y - 1) % self.cols)
                )
            case "d":
                self.body.insert(
                    0, Position(head_posi.x, (head_posi.y + 1) % self.cols)
                )

    def remove_tail(self):
        self.body.pop()


class Main:
    "全局状态管理类"

    def __init__(self, rows, cols, speed):
        self.rows = rows
        self.cols = cols
        self.speed = speed
        self.map = [["⬜" for i in range(self.cols)] for j in range(self.rows)]
        self.score = 0

    def gen_apple(self, snake: Snake):
        while 1:
            apple_posi = Position(randint(0, self.rows - 1), randint(0, self.cols - 1))
            if apple_posi in snake.body:
                continue
            else:
                self.apple = apple_posi
                break

    def render_snake(
        self,
        snake: Snake,
    ):
        for i in snake.body:
            if snake.body.index(i) == 0:
                self.map[i.x][i.y] = "❎"
            else:
                self.map[i.x][i.y] = "🟩"

    def render_apple(self):
        self.map[self.apple.x][self.apple.y] = "🟥"

    def show_map(self):
        for row in self.map:
            for element in row:
                print(element, end="")
            print("")

    def clear_map(self):
        self.map = [["⬜" for i in range(self.cols)] for j in range(self.rows)]

    def next_move(self, snake: Snake):
        opposite_move = {
            "w": "s",
            "s": "w",
            "a": "d",
            "d": "a",
        }
        try:
            move = inputimeout("", SPEED)
            if move in ["w", "s", "a", "d"] and move != opposite_move[snake.last_move]:
                snake.last_move = move
            else:
                move = snake.last_move
        except TimeoutOccurred:
            move = snake.last_move

        snake.move_head(move)
        if self.apple in snake.body:
            self.gen_apple(snake)
            self.score += 1
        else:
            snake.remove_tail()


class Message:
    @staticmethod
    def start(game: Main):
        print("贪吃蛇")
        print("请对齐以下框架")
        game.show_map()
        input("任意键继续")

    @staticmethod
    def end(score):
        print("游戏结束")
        print(f"成绩为:{score}分")


if __name__ == "__main__":

    ROWS = int(input())
    COLS = int(input())
    SPEED = float(input())

    game = Main(ROWS, COLS, SPEED)
    Message.start(game)
    snake = Snake(Position(ROWS // 2, COLS // 2), ROWS, COLS)
    game.gen_apple(snake)
    
    while not snake.is_crashed():
        game.clear_map()
        game.next_move(snake)
        game.render_apple()
        game.render_snake(snake)
        game.show_map()
        
    Message.end(game.score)
