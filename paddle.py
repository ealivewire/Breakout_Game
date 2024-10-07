# Import necessary library(ies):
from turtle import Turtle

# Define variable (dictionary) for the max distance between the paddle and a ball before it is considered a hit, based on length of paddle:
paddle_max_distance_from_ball = {
    10:{"max": 83},
    5:{"max": 42},
    2.5:{"max": 20.8},
    }  # 10: Max was 83 before troubleshooting of paddle erratic behavior

# Define variable (dictionary) for the x-coordinates (left and right) should be, based on length of paddle:
paddle_shapesize = {
    10:{"left": -179, "right": 178},
    5:{"left": -220, "right": 219},
    2.5:{"left": -240, "right": 240},
    }


# Define class to represent a paddle object:
class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")  # Set shape of turtle (paddle).
        self.color("purple")  # Set color of turtle (paddle).
        self.shapesize(0.5,10)  # Size of paddle at object instantiation.
        self.penup()  # Prevent turtle (paddle) from "writing" on the application window.
        self.goto(position) # Move paddle to the position passed along at object instantiation.

    # DEFINE FUNCTIONS ASSOCIATED WITH THE PADDLE CLASS (LISTED IN ALPHABETICAL ORDER BY FUNCTION NAME):
    def go_left(self):
        """Function to send the paddle toward the left wall in the application window"""
        # Define the x-coordinate at the left of the application window that will serve as the limit
        # for how far left the paddle will be allowed to go, based on length of paddle:
        xcor_limit = (paddle_shapesize[self.shapesize()[1]]["left"])

        # If paddle has not reached the left-hand limit, allow leftward movement of paddle:
        if self.xcor() >= xcor_limit:  # Left end of paddle has not reached the left-hand wall.
            new_x = self.xcor() - 20
            self.goto(new_x, self.ycor())

    def go_right(self):
        """Function to send the paddle toward the right wall in the application window"""
        # Define the x-coordinate at the right of the application window that will serve as the limit
        # for how far right the paddle will be allowed to go, based on length of paddle:
        xcor_limit = (paddle_shapesize[self.shapesize()[1]]["right"])

        # If paddle has not reached the right-hand limit, allow rightward movement of paddle:
        if self.xcor() <= xcor_limit:  # Right end of paddle has not reached the right-hand wall.
            new_x = self.xcor() + 20
            self.goto(new_x, self.ycor())

    def reset(self, paddle_length):
        """Function for resetting the paddle's size and position"""
        # Reset the paddle length:
        self.shapesize(0.5, paddle_length)

        # Reset the paddle position:
        self.setposition(0,-300)

