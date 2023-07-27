from turtle import Turtle, Screen
import time
from snake import Snake

screeen = Screen()
screeen.setup(width=600, height=600)
screeen.bgcolor("black")
screeen.title("Snake Game")
screeen.tracer(0)


game_is_on = True

snake = Snake()

while game_is_on:
    screeen.update()
    time.sleep(0.1)
    snake.move()













screeen.exitonclick()