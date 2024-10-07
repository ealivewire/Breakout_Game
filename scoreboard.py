# Import necessary library(ies):
from turtle import Turtle

# Initiate scoreboard variable:
scoreboard = ""

# Define constants for certain GUI-related components:
ALIGNMENT = "center"
FONT = ("Courier", 60, "normal")

# Define variable (dictionary) for defining how many points should be awarded for a brick hit, based on the brick's color:
POINTS_BY_COLOR = {"yellow": 1, "green": 3, "orange": 5, "red": 7}


# Define class to represent a scoreboard object:
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")  # Set color of turtle (scoreboard).
        self.penup()  # Prevent turtle (scoreboard) from "writing" on the application window.  Scoreboard shall write via "update_scoreboard" function below.
        self.hideturtle()  # Hide the turtle (scoreboard).  Further updates will show scores.
        self.update_scoreboard([0,0])  # Set (and write) initial (zero) score for each player.

    # DEFINE FUNCTIONS ASSOCIATED WITH THE SCOREBOARD CLASS (LISTED IN ALPHABETICAL ORDER BY FUNCTION NAME):
    def update_scoreboard(self, total_scores_by_player):
        """Function to update the scoreboard with the current scores by player"""
        # Clear the contents of the scoreboard:
        self.clear()

        # Go to Player 1's position on the scoreboard:
        self.goto(-150, 232)

        # Update the scoreboard with Player 1's current score:
        self.write("{:03.0f}".format(total_scores_by_player[0]), False, ALIGNMENT, FONT)    # Player 1

        # Go to Player 2's position on the scoreboard:
        self.goto(180, 232)

        # Update the scoreboard with Player 2's current score:
        self.write("{:03.0f}".format(total_scores_by_player[1]), False, ALIGNMENT, FONT)    # Player 2