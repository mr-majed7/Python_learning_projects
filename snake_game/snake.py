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
        self.head = self.segements[0]
    
    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)
    
    def move(self):
        for seg_num in range(len(self.segements) - 1, 0, -1):
            new_x = self.segements[seg_num - 1].xcor()
            new_y = self.segements[seg_num - 1].ycor()
            self.segements[seg_num].goto(new_x, new_y)
        self.head.forward(20)
    
    def add_segment(self,position):
            new_segment = Turtle("square")
            new_segment.color("white")
            new_segment.penup()
            new_segment.goto(position)
            self.segements.append(new_segment)

    def extend(self):
        self.add_segment(self.segements[-1].position())

    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)
    
    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)
    
    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
    
    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def reset(self):
        for seg in self.segements:
            seg.goto(1000, 1000)
        self.segements.clear()
        self.create_snake()
        self.head = self.segements[0]