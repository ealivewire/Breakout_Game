# Import necessary library(ies):
from turtle import Turtle


# Define class to represent a wall object:
class Wall(Turtle):
    def __init__(self, position, which_wall):
        super().__init__()
        self.shape("square")  # Set shape of turtle (wall).
        self.color("white")  # Set color of turtle (wall).
        if which_wall == "top": # Set size of top wall.
            self.shapesize(4,400)
        elif which_wall == "left" or which_wall == "right":   # Set size of side (left or right) wall.
            self.shapesize(300,0.5)
        elif which_wall == "score_left" or which_wall == "score_right":   # Set size of scoreboard wall (left or right).
            self.shapesize(2.5,0.5)
        self.penup()  # Prevent turtle (wall) from "writing" on the application window.
        self.goto(position)  # Move wall to the position passed along at object instantiation.




