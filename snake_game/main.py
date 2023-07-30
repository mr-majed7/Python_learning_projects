from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import Board

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)


game_is_on = True

snake = Snake()
food = Food()
score_board = Board()


def exit():
    global game_is_on
    game_is_on = False

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")
screen.onkey(exit, "q")



while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()
    
    if snake.head.distance(food) < 15:
        food.refresh()
        score_board.increase_score()
        snake.extend()

    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
            score_board.reset()
            snake.reset()
    
    for segment in snake.segements[1:]:
        if snake.head.distance(segment) < 10:
            score_board.reset()
            snake.reset()
 










screen.exitonclick()