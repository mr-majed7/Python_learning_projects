from turtle import Screen, Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.update()

    def update(self):
        self.clear()
        self.goto(-100,240)
        self.write(f"{self.l_score}", align="center", font=("Courier", 40, "normal"))
        self.goto(100,240)
        self.write(f"{self.r_score}", align="center", font=("Courier", 40, "normal"))

    def l_point(self):
        self.l_score += 1
        self.clear()
        self.update()
    
    def r_point(self):
        self.r_score += 1
        self.clear()
        self.update()