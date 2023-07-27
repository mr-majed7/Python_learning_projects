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
    for seg_num in range(len(segements) - 1, 0, -1):
        new_x = segements[seg_num - 1].xcor()
        new_y = segements[seg_num - 1].ycor()
        segements[seg_num].goto(new_x, new_y)
    segements[0].forward(20)
    segements[0].left(90)
        













screeen.exitonclick()