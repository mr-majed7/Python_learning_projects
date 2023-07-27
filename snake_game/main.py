from turtle import Turtle, Screen
import time

screeen = Screen()
screeen.setup(width=600, height=600)
screeen.bgcolor("black")
screeen.title("Snake Game")
screeen.tracer(0)

starting_positions = [(0, 0), (-20, 0), (-40, 0)]
segements = []

for position in starting_positions:
    new_segment = Turtle("square")
    new_segment.color("white")
    new_segment.penup()
    new_segment.goto(position)
    segements.append(new_segment)

game_is_on = True

while game_is_on:
    screeen.update()
    time.sleep(0.1)
    for seg in segements:
        seg.forward(20)
        













screeen.exitonclick()