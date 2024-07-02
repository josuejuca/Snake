import tkinter as tk
import random

# Configurações do jogo
WIDTH = 600
HEIGHT = 400
DELAY = 100
DOT_SIZE = 20
SCORE_SIZE = 10
SCORE_X = 50
SCORE_Y = 20
SNAKE_COLOR = "green"
FOOD_COLOR = "red"

# Constantes de direção
DIRECTIONS = {
    "Right": (1, 0),
    "Left": (-1, 0),
    "Up": (0, -1),
    "Down": (0, 1)
}

# Inicialização da janela
window = tk.Tk()
window.title("Jogo da Cobra")
window.resizable(False, False)

# Criação do canvas
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Classe da Cobra
class Snake:
    def __init__(self):
        self.segments = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.score = 0
        self.food = self.create_food()

    def create_food(self):
        x = random.randint(1, (WIDTH - DOT_SIZE) // DOT_SIZE) * DOT_SIZE
        y = random.randint(1, (HEIGHT - DOT_SIZE) // DOT_SIZE) * DOT_SIZE
        return x, y

    def move(self):
        head = self.segments[0]
        x, y = head
        dx, dy = DIRECTIONS[self.direction]

        new_head = (x + dx * DOT_SIZE, y + dy * DOT_SIZE)
        self.segments.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.create_food()
        else:
            self.segments.pop()

    def change_direction(self, direction):
        opposite_directions = {"Right": "Left", "Left": "Right", "Up": "Down", "Down": "Up"}
        if direction != opposite_directions[self.direction]:
            self.direction = direction

    def check_collision(self):
        head = self.segments[0]
        x, y = head

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return True

        return head in self.segments[1:]

    def draw(self):
        canvas.delete("all")

        for segment in self.segments:
            x, y = segment
            canvas.create_rectangle(x, y, x + DOT_SIZE, y + DOT_SIZE, fill=SNAKE_COLOR)

        x, y = self.food
        canvas.create_oval(x, y, x + DOT_SIZE, y + DOT_SIZE, fill=FOOD_COLOR)

        canvas.create_text(SCORE_X, SCORE_Y, text=f"Pontos: {self.score}", fill="white", font=("Arial", SCORE_SIZE))

# Classe do Jogo
class Game:
    def __init__(self):
        self.snake = Snake()
        self.setup_bindings()
        self.start_game()

    def setup_bindings(self):
        window.bind("<KeyPress>", self.on_key_press)
        window.focus_set()

    def on_key_press(self, event):
        if event.keysym in DIRECTIONS:
            self.snake.change_direction(event.keysym)

    def game_loop(self):
        if not self.snake.check_collision():
            self.snake.move()
            self.snake.draw()
            window.after(DELAY, self.game_loop)
        else:
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Você perdeu!", fill="white", font=("Arial", 20))

    def start_game(self):
        self.game_loop()

# Inicialização do jogo
game = Game()

# Execução da janela
window.mainloop()
