from turtle import Turtle, Screen

screeen = Screen()
screeen.setup(width=600, height=600)
screeen.bgcolor("black")
screeen.title("Snake Game")

starting_positions = [(0, 0), (-20, 0), (-40, 0)]

for position in starting_positions:
    new_segment = Turtle("square")
    new_segment.color("white")
    new_segment.goto(position)













screeen.exitonclick()