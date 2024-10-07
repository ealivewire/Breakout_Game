# Import necessary library(ies):
from turtle import Turtle
from winsound import Beep, PlaySound, SND_ASYNC
from paddle import paddle_max_distance_from_ball
from random import choice


# Define class to represent a ball object:
class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")  # Set color of turtle (ball).
        self.shape("circle")  # Set shape of turtle (ball).
        self.penup()  # Prevent turtle (ball) from "writing" on the application window.
        self.goto(0, 0)  # Move ball to its "base" position.
        self.x_move = choice([-10, 10]) # Direction that ball should go in at next launch (random choice between leftward and rightward) relative to the x-axis.
        self.y_move = 10  # Direction that ball should go in at next launch, relative to the y-axis.
        # self.x_move = choice([-1, 1]) # Direction that ball should go in at next launch (random choice between leftward and rightward) relative to the x-axis.
        # self.y_move = 1  # Direction that ball should go in at next launch, relative to the y-axis.

    # DEFINE FUNCTIONS ASSOCIATED WITH THE BALL CLASS (LISTED IN ALPHABETICAL ORDER BY FUNCTION NAME):
    def bounce_x(self):
        """Function to define the direction that the ball should bounce along the x-axis"""
        self.x_move *= -1

    def bounce_y(self):
        """Function to define the direction that the ball should bounce along the y-axis"""
        self.y_move *= -1

    def check_for_ball_out_of_bounds(self, screen):
        """Function to execute GUI behavior when ball goes out of bounds (bottom end of application window)"""
        if self.ycor() < -400:  # Ball has breached bottom end of application window.
            # Turn screen tracer off until updates have been fully completed:
            screen.tracer(0)

            # Play a sound to alert current player that the ball has gone out of bounds:
            PlaySound("out-of-bounds.wav", SND_ASYNC)

            # Re-position ball to its "base" position:
            self.reset_position()

            # Set the direction that ball should go in at next launch (random choice between leftward and rightward)
            # relative to the x-axis:
            self.x_move = choice([-10, 10])

            # Set the direction that ball should go in at next launch, relative to the y-axis:
            self.y_move = abs(self.y_move)

            # Turn screen tracer back on:
            screen.tracer(1)

            # Return the result of this function to inform the calling function that the ball has gone out of bounds:
            return True

        # Return the result of this function to inform the calling function that the ball has NOT gone out of bounds:
        return False

    def check_for_contact_paddle(self, paddle):
        """Function to determine if the ball has made contact with the paddle"""
        # Calculate key distance metrics which will then determine if the ball has contacted the paddle, thus meriting a bounce:
        center_of_paddle_x = paddle.xcor()
        center_of_paddle_y = paddle.ycor()
        half_width_of_paddle_x = paddle.shapesize()[1] * 30 * 0.5
        half_height_of_paddle_y = paddle.shapesize()[0] * 30 * 0.5
        left_edge_of_paddle_x = center_of_paddle_x - half_width_of_paddle_x
        right_edge_of_paddle_x = center_of_paddle_x + half_width_of_paddle_x
        top_edge_of_paddle_y = center_of_paddle_y + half_height_of_paddle_y
        bottom_edge_of_paddle_y = center_of_paddle_y - half_height_of_paddle_y
        center_of_ball_x = self.xcor()
        center_of_ball_y = self.ycor()
        half_height_of_ball_y = self.shapesize()[0] * 30 * 0.5
        bottom_edge_of_ball_y = center_of_ball_y - half_height_of_ball_y
        ball_within_left_edge_of_paddle_x = left_edge_of_paddle_x < center_of_ball_x
        ball_within_right_edge_of_paddle_x = center_of_ball_x < right_edge_of_paddle_x
        ball_within_edge_of_paddle_y = bottom_edge_of_paddle_y < bottom_edge_of_ball_y < top_edge_of_paddle_y

        # If ball is deemed to have contacted the paddle, bounce the ball off the paddle:
        if ball_within_left_edge_of_paddle_x and ball_within_right_edge_of_paddle_x and ball_within_edge_of_paddle_y:

            # Play a sound to alert the current player of contact made:
            Beep(1000, 10)  # Set Duration To 10 ms == 0.01 second

            # Bounce the ball relative to the y-axis:
            self.bounce_y()

    def check_for_contact_side_wall(self):
        """Function to determine if the ball has made contact with either the left-hand or right-hand wall"""
        if self.xcor() > 265 or self.xcor() < -270: # Ball has made contact with either the left-hand or right-hand wall.
            # Play a sound to alert the current player of contact made:
            Beep(500, 10)   # Set Duration To 10 ms == 0.01 second

            # Bounce the ball relative to the x-axis:
            self.bounce_x()

    def check_for_contact_top_wall(self):
        """Function to determine if the ball has made contact with the top wall of the application window"""
        if self.ycor() > 340:   # Ball has made contact with the top wall.
            # Play a sound to alert the current player of contact made:
            Beep(500, 10)  # Set Duration To 10 ms == 0.01 second

            # Bounce the ball relative to the y-axis:
            self.bounce_y()

            # Return the result of this function to inform the calling function that the ball has contacted the top wall:
            return True

    def move(self, screen):
        """Function to move the ball, based on the ball's position and the x-y directions in effect"""
        # Perform a screen update:
        screen.update()

        # Determine the new position of the ball by adding a new x and y coordinate to its existing position:
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move

        # Move the ball to the new x and y coordinates:
        self.goto(new_x, new_y)

    def reset_position(self):
        """Function to reset the ball's position and direct its next bounce along the x-axis"""
        # Return the ball to its "base" position:
        self.goto(0, 0)

        # Bounce the ball relative to the x-axis:
        self.bounce_x()

    def speed_up(self, ball_speed, player_index):
        """Function to increase the ball's speed for the current player"""
        # Increase the speed of the ball:
        self.speed(ball_speed[player_index] + 1)

        # Record the new speed as the current player's in-effect ball speed:
        ball_speed[player_index] += 1