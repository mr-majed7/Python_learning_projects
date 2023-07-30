from turtle import Turtle

class Board(Turtle):
    
    def __init__(self):
        super().__init__()
        self.score = 0
        with open("data.txt") as data:
            self.high_score = int(data.read().strip())
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.write(f"Score: {self.score} High Score: {self.high_score}", align="center", font=("Courier", 20, "normal"))
    
    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align="center", font=("Courier", 20, "normal"))
    
    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()

    def reset(self):
        if self.score > int(self.high_score):
            self.high_score = self.score
            with open("data.txt", mode="w") as data:
                data.write(f"{self.high_score}")
        self.score = 0 
        self.update_scoreboard()   

    def game_over(self):
        self.goto(0, 0)
        self.write(f"GAME OVER", align="center", font=("Courier", 20, "normal"))
        