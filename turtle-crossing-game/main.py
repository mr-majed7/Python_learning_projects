import time
from turtle import Screen
from player import Player
from car import Car
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
screen.bgcolor("white")
screen.title("Turtle Crossing Game")
screen.listen()

player = Player()
car = Car()
scoreboard = Scoreboard()
screen.onkey(player.move, "Up")

game_is_on = True


while game_is_on:
    time.sleep(0.1)
    screen.update()
    car.create_car()
    car.move()
    if player.ycor() > 280:
        player.reset_position()
        car.car_level_up()
        scoreboard.update_scoreboard()

    for cars in car.all_cars:
        if cars.distance(player) < 20:
            game_is_on = False
            scoreboard.game_over()
        
    


screen.exitonclick()