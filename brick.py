# Import necessary library(ies):
from turtle import Turtle


# Define class to represent a brick object:
class Brick(Turtle):
    def __init__(self, position, color):
        super().__init__()
        self.shape("square")  # Set shape of turtle (brick).
        self.color(color)  # Set color of turtle (brick).
        self.shapesize(0.5,1.75)  # Set size of brick.
        self.penup()  # Prevent turtle (brick) from "writing" on the application window.
        self.goto(position)  # Move brick to the position passed along at object instantiation.





