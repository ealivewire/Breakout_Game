# PROFESSIONAL PROJECT: Breakout Game

# NOTES:
# 1. Source of game rules/construct requirements:
#    https://en.wikipedia.org/wiki/Breakout_(video_game)
#
# 2. Ball speed increases at specific intervals:
#    - After 4 hits
#    - After 12 hits
#    - After making initial contact with the orange row.
#    - After making initial contact with the red row
#
# 3. Once ball breaks through and hits top wall for first time, paddle shrinks to half its size.

# The highest score achievable for one player is 896; this is done by eliminating two screens of bricks worth 448 points per screen. Once the second screen of bricks is destroyed, the ball in play harmlessly bounces off empty walls until the player restarts the game, as no additional screens are provided. However, a secret way to score beyond the 896 maximum is to play the game in two-player mode. If "Player One" completes the first screen on their third and last ball, then immediately and deliberately allows the ball to "drain", Player One's second screen is transferred to "Player Two" as a third screen, allowing Player Two to score a maximum of 1,344 points if they are adept enough to keep the third ball in play that long. Once the third screen is eliminated, the game is over

# Import necessary library(ies):
from turtle import Screen
from tkinter import messagebox
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
from ui import address_clearance_of_level_1, address_clearance_of_level_2, config_screen, check_for_brick_hit, check_for_contact_top_wall, create_and_config_bricks, create_and_config_walls, implement_screen_listening, pause_game, show_or_hide_bricks, switch_player

# Define variable for the GUI (application) window (so that it can be used globally), and make it a Turtle instance:
screen = Screen()

# Define variable to track if a game is in progress:
is_game_on = True

# Define list variable for tracking how many turns each player has left on the current screen:
turns_remaining = [3,3]

# Define list variable for tracking each player's brick objects:
bricks = [[],[]]

# Define list variable for tracking how many bricks each player has hit in his/her current game level:
bricks_hit = [0,0]

# Define list variable for tracking each player's total score in the current game:
total_scores = [0,0]

# Define list variable for tracking each player's ball speed in the current game:
ball_speed = [3,3]

# Define list variable for tracking each player's paddle length in the current game:
paddle_length = [10, 10]

# Define variable for tracking whether the current game is in 1-player or 2-player mode:
player_mode = 1

# Define list variable for tracking how many levels each player has successfully cleared in the current game:
levels_cleared = [0,0]

# Define lists for tracking key milestones each of up to two players has reached for the 1st time in the current game:
initial_contact_orange = [False, False]
initial_contact_red = [False, False]
initial_contact_top_wall = [False, False]

# Define variable to indicate which of up to two players is the starting player:
player_index = 0

award_player_2_third_screen = False

# DEFINE FUNCTIONS TO BE USED FOR THIS APPLICATION (LISTED IN ALPHABETICAL ORDER BY FUNCTION NAME):


def address_player_cleared_level_2():
    """Function to take necessary actions when player has cleared Level 2"""
    global player_index, is_game_on

    # WITHOUT ACCOMMODATING EXTRA BOARD FOR PLAYER 2, THIS SECTION WORKS.
    turns_remaining[player_index] = 0

    address_clearance_of_level_2(screen, ball, paddle, player_index, levels_cleared)

    if check_for_end_of_game() == "End of Game":
        is_game_on = False
        exit()

    else:
        # if player_mode == 2 and not (total_scores[0] == 896):
        if player_mode == 2:
            player_index = switch_player(abs(player_index - 1), screen, ball, ball_speed, paddle, paddle_length, bricks)


def check_for_end_of_game():
    """Function which checks if the game has ended and performs relevant player notifications"""
    # If current player has run out of turns, inform said player that his/her game has ended:
    if turns_remaining[player_index] == 0:  # Current player has run out of turns
        messagebox.showinfo(f"Player {player_index + 1}",
                            f"Player {player_index + 1}: Your game is over.")

    # If single player (1-player mode) or both players (2-player mode) have run out of turns,
    # the game has ended.  Perform relevant player notifications:
    if turns_remaining == [0, 0]:   # Both players have run out of turns:
        if player_mode == 2:
            if total_scores[player_index] > total_scores[abs(player_index - 1)]:
                messagebox.showinfo(f"GAME OVER",
                                f"Player {player_index + 1} is the winner.")
            elif total_scores[abs(player_index - 1)] > total_scores[player_index]:
                messagebox.showinfo(f"GAME OVER",
                                f"Player {abs(player_index - 1) + 1} is the winner!")
            elif total_scores[player_index] == total_scores[abs(player_index - 1)]:
                messagebox.showinfo(f"GAME OVER",
                                f"Game has ended with a tie score.")

        # Ask if player(s) want to play another game:
        play_again = messagebox.askyesno("Question", "Would you like to play another game?")
        if not play_again:  # New game has been declined
            # Return game-declining result to the calling function:
            return "End of Game"
        else:   # New game is desired
            # Set up the user interface in preparation for the new game:
            create_and_config_user_interface()
            # create_and_config_user_interface(ball_speed, turns_remaining, screen, bricks, bricks_hit, initial_contact_orange, initial_contact_red, initial_contact_top_wall, total_scores, levels_cleared, paddle_length)

            # Launch a new game:
            play_game()

    else:
        # Return result to calling function to indicate that current game (if not ended)
        # should continue OR if a new game should commence:
        return "Continue"


def check_if_ball_out_of_bounds():
    """Function to check if ball has gone out of bounds.  If yes, perform subsequent actions based on status of game"""
    global player_index, is_game_on, award_player_2_third_screen

    if ball.check_for_ball_out_of_bounds(screen):  # Ball has gone out of bounds.
        if player_index == 0 and total_scores[0] == 448 and turns_remaining[0] == 1:
            award_player_2_third_screen = True
            if player_mode == 2:
                messagebox.showinfo(f"Player 2",
                                    f"Note to Player 2:\n\nPlayer 1 had only 1 turn remaining at the start of the second screen.\n\nPlayer 1 did not hit any additional bricks before running out of turns.\n\nTherefore, if you clear both of your screens with turns remaining, you will receive a bonus (third) screen for the chance to score above 896 points.")
            #***FIGURE OUT WHAT ELSE TO DO HERE***

        # Reduce 'turns_remaining' tracker by 1:
        turns_remaining[player_index] -= 1

        # Check if player has run out of turns.  If both players have run out of turns, declare win/draw ande
        # ask player if s/he wished to play another game.  If yes, reset the game:
        if check_for_end_of_game() == "End of Game":
            is_game_on = False
            exit()

        else:
            # if player_mode == 2 and not (total_scores[0] == 896):
            if player_mode == 2 and turns_remaining[abs(player_index - 1)] > 0:
                player_index = switch_player(abs(player_index - 1), screen, ball, ball_speed, paddle, paddle_length, bricks)


def create_and_config_user_interface():
    """Function for creating and configuring the user interface, including the application window (screen), walls, paddle, game ball, and scoreboard"""
    global paddle, scoreboard, ball, turns_remaining, screen, bricks, bricks_hit, initial_contact_orange, initial_contact_red, initial_contact_top_wall, total_scores, levels_cleared, paddle_length

    bricks = [[], []]
    bricks_hit = [0, 0]
    total_scores = [0, 0]
    levels_cleared = [0, 0]

    initial_contact_orange = [False, False]
    initial_contact_red = [False, False]
    initial_contact_top_wall = [False, False]

    try:
        screen.clear()
        screen = None
        screen = Screen()
    except:
        pass

    # Populate 'turns_remaining' list for each of up to two players:
    turns_remaining = [3, 3]

    # Turn screen tracer off until interface has been fully configured:
    screen.tracer(0)

    # Configure the application window:
    config_screen(screen)

    # Create and configure each of the walls:
    create_and_config_walls()

    # Create and configure each of the bricks:
    for i in range(0, 1):
        create_and_config_bricks(bricks, i, levels_cleared)

    # Create and configure the paddle:
    try:
        del paddle
    except:
        pass
    paddle = Paddle((0, -300))
    paddle_length = [10, 10]

    # Create and configure the game ball:
    try:
        ball.clear()
    except:
        pass
    ball = Ball()
    for i in range(0,2):
        ball_speed[i] = 3

    # Create and configure the scoreboard:
    try:
        scoreboard.clear()
    except:
        pass
    scoreboard = Scoreboard()

    # Make sure that the screen "listens" for overall inputs (e.g., key presses):
    # screen.listen()

    # Specify window inputs for screen to "listen" for:
    implement_screen_listening(screen, paddle)

    # Turn screen tracer back on:
    screen.tracer(1)

    # Make sure that the screen "listens" for overall inputs (e.g., key presses):
    screen.listen()


def play_game():
    """Function which runs the game"""
    global is_game_on, turns_remaining, bricks_hit, initial_contact_orange, initial_contact_red, initial_contact_top_wall, player_index, player_mode, screen, paddle_length, award_player_2_third_screen

    # Create and configure the user interface:
    create_and_config_user_interface()
    # create_and_config_user_interface(ball_speed, turns_remaining, screen, bricks, bricks_hit, initial_contact_orange, initial_contact_red, initial_contact_top_wall, total_scores, levels_cleared, paddle_length)

    messagebox.showinfo("WELCOME TO MY BREAKOUT GAME!",
                        "GUIDELINES:\n\n- Maximum number of points per player = 896.\n\n- Each player is afforded three (3) turns via two (2) levels.\n\n"
                        "- Number of points scored per brick (by brick color):\nYELLOW = 1, GREEN = 3, ORANGE = 5, RED = 7.\n\n- If Player 1 scores 448 points on the third/final ball but then goes out of bounds without hitting any additional bricks, Player 2 will inherit a third level, thereby making "
                        "Player 2's maximum number of points = 1,364.\n\n- To pause the current game temporarily, hit the ESC key.\n\nENJOY!")

    if messagebox.askyesno("Player mode",f"Would you like to add a 2nd player to this game?"):
        player_mode = 2
    else:
        player_mode = 1
        turns_remaining[1] = 0

    player_index = switch_player(0, screen, ball, ball_speed, paddle, paddle_length, bricks)

    while is_game_on:
        # Move the ball:
        ball.move(screen)

        # Detect if ball has hit the left or right wall:
        ball.check_for_contact_side_wall()

        # Detect if ball has hit the top wall.  If it has on 1st contact, shrink the paddle in half and update 'initial_contact_top_wall' tracker:
        initial_contact_top_wall = check_for_contact_top_wall(player_index, ball, paddle, paddle_length, initial_contact_top_wall)

        # Check if a brick has been hit. If such a hit has been scored, perform necessary updates:
        for brick in bricks[player_index]:
            check_for_brick_hit(brick, player_index, screen, bricks, bricks_hit, ball, ball_speed, total_scores, scoreboard, initial_contact_orange, initial_contact_red)

        # Detect if ball has made contact with paddle:
        ball.check_for_contact_paddle(paddle)

        # If player has reached a final total of either 896 points (cleared 1st two levels) or 1,364
        # points (Player 2 cleared both screens + bonus one), end game:
        if total_scores[player_index] == 1364:
            # At this point, game is over and no switching back to the other player is allowed, since only Player 2 can reach 1,364 points and
            # Player 1's game is already over.  Following function is called, however, to perform final functionality including asking if a
            # new game is desired:
            turns_remaining[player_index] = 0
            if check_for_end_of_game() == "End of Game":
                is_game_on = False
                exit()

        # Check if player has cleared Level 2 (scored 896 points).  If yes, perform relevant actions based on game status:
        elif total_scores[player_index] == 896:
            address_player_cleared_level_2()

        # Check if player has cleared Level 1 (scored 448 points).  If yes, perform relevant actions based on game status:
        elif total_scores[player_index] == 448 and bricks_hit[player_index] > 0:
            initial_contact_orange, initial_contact_red, initial_contact_top_wall = address_clearance_of_level_1(screen, bricks, bricks_hit, ball, paddle, player_index, levels_cleared, initial_contact_orange, initial_contact_red, initial_contact_top_wall)

        else:
            # Detect if ball has gone out of bounds.  If player has run ouf of turns, player's game is over.  If game is over, ask player if
            # she/wishes to play another game.  If yes, reset the game:
            check_if_ball_out_of_bounds()


# Play the game:
play_game()


# Keep application window open until user closes it:
screen.exitonclick()

if __name__ == '__main__':
    play_game()