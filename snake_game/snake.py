from turtle import Turtle, Screen

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
UP = 90
DOWN = 270
RIGHT = 0
LEFT = 180


class Snake:

    def __init__(self):
        self.segements = []
        self.create_snake()
    
    def create_snake(self):
        for position in STARTING_POSITIONS:
            new_segment = Turtle("square")
            new_segment.color("white")
            new_segment.penup()
            new_segment.goto(position)
            self.segements.append(new_segment)
    
    def move(self):
        for seg_num in range(len(self.segements) - 1, 0, -1):
            new_x = self.segements[seg_num - 1].xcor()
            new_y = self.segements[seg_num - 1].ycor()
            self.segements[seg_num].goto(new_x, new_y)
        self.segements[0].forward(20)
    
    def up(self):
        if self.segements[0].heading() != DOWN:
            self.segements[0].setheading(UP)
    
    def down(self):
        if self.segements[0].heading() != UP:
            self.segements[0].setheading(DOWN)
    
    def right(self):
        if self.segements[0].heading() != LEFT:
            self.segements[0].setheading(RIGHT)
    
    def left(self):
        if self.segements[0].heading() != RIGHT:
            self.segements[0].setheading(LEFT)
