# Import necessary library(ies):
from tkinter import messagebox
from brick import Brick
from wall import Wall
from winsound import PlaySound, SND_ASYNC
from scoreboard import Scoreboard, POINTS_BY_COLOR
from turtle import Screen
from ball import Ball
from paddle import Paddle

# Define variable to represents what color each row's bricks should be:
brick_colors = ["yellow","yellow","green","green","orange","orange", "red", "red"]

# Define variable (dictionary) for what sounds play (by color) for bricks hit:
brick_sounds = {"yellow": "yellow", "green": "green.wav", "orange": "orange.wav", "red": "red.wav"}


def address_clearance_of_level_1(screen, bricks, bricks_hit, ball, paddle, player_index, levels_cleared, initial_contact_orange, initial_contact_red, initial_contact_top_wall):
    """Function to check if a player has successfully cleared the game's first level.  If level was cleared, perform necessary UI-related updates"""
    # Increment level-clearance tracker by 1 for the current player:
    levels_cleared[player_index] += 1

    # Inform current player of successful level clearance:
    messagebox.showinfo(f"LEVEL SUCCESSFULLY CLEARED",
                        f"Player {player_index + 1}: CONGRATULATIONS!\n\nYou have cleared Level {levels_cleared[player_index]}.\n\nYou will now proceed to Level {levels_cleared[player_index]+1}.")

    # Turn screen tracer off until updates have been fully completed:
    screen.tracer(0)

    # Introduce a new set of bricks on the application window for the current player who cleared the level:
    create_and_config_bricks(bricks, player_index, levels_cleared)

    # Reset the bricks-hit tracker to 0 for the current player.
    # This is done to facilitate tracking of milestones reached by the current player in the next game level:
    bricks_hit[player_index] = 0

    # Re-position ball to its "base" position:
    ball.setposition(0, 0)
    ball.y_move = abs(ball.y_move)

    # Re-position paddle to its "base" position:
    paddle.setposition(0, -300)

    # Reset milestone trackers for the current player.
    # This is done to facilitate tracking of milestones reached by the current player in the next game level:
    initial_contact_orange[player_index] = False
    initial_contact_red[player_index] = False
    initial_contact_top_wall[player_index] = False

    # Turn screen tracer back on:
    screen.tracer(1)

    return initial_contact_orange, initial_contact_red, initial_contact_top_wall


def address_clearance_of_level_2(screen, ball, paddle, player_index, levels_cleared):
    """Function to check if a player has successfully cleared the game's second level (or in the case of Player 3 only, the inherited "third" level).  If level was cleared, perform necessary updates"""
    # Increment level-clearance tracker by 1 for the current player:
    levels_cleared[player_index] += 1

    # Inform current player of successful level clearance:
    messagebox.showinfo(f"LEVEL SUCCESSFULLY CLEARED",
                        f"Player {player_index + 1}: CONGRATULATIONS!\n\nYou have cleared Level {levels_cleared[player_index]}.")

    # Turn screen tracer off until updates have been fully completed:
    screen.tracer(0)

    # Re-position ball to its "base" position:
    ball.setposition(0, 0)
    ball.y_move = abs(ball.y_move)

    # Re-position paddle to its "base" position:
    paddle.setposition(0, -300)

    # Turn screen tracer back on:
    screen.tracer(1)

    # If this is a 2-player game and the other player has turns remaining, switch play to the other player.
    # However, do not switch to Player 1 if s/he has scored 896 (game limit for Player 1):
    # if turns_remaining[abs(player_index - 1)] > 0 and player_mode == 2 and not (total_scores[0] == 896):
    #     switch_player(abs(player_index - 1))


def check_for_brick_hit(brick, player_index, screen, bricks, bricks_hit, ball, ball_speed, total_scores, scoreboard, initial_contact_orange, initial_contact_red):
    """Function to check if a brick has been hit.  If such a hit has been scored, perform necessary updates"""
    # global bricks_hit, initial_contact_orange, initial_contact_red, player_index

    # If a brick has been hit, perform necessary updates:
    if ball.distance(brick) < 20:  # Brick has been hit.
        # Increment counter of hit bricks by 1:
        bricks_hit[player_index] += 1

        # Increase point for the current player:
        total_scores[player_index] += POINTS_BY_COLOR[brick.color()[0]]

        # Turn screen tracer off until updates have been fully completed:
        screen.tracer(0)

        # Update the scoreboard:
        scoreboard.update_scoreboard(total_scores)

        # Emit a beep:
        PlaySound(brick_sounds[brick.color()[0]], SND_ASYNC)

        # If an orange brick has been hit for the first time, increase ball speed and update 'initial_contact_orange' tracker:
        if initial_contact_orange[player_index] == False and brick.color()[0] == "orange":
            ball.speed_up(ball_speed, player_index)
            initial_contact_orange[player_index] = True
            print("INITIAL HIT - ORANGE")

        # If a red brick has been hit for the first time, increase ball speed and update 'initial_contact_red' tracker:
        if initial_contact_red[player_index] == False and brick.color()[0] == "red":
            ball.speed_up(ball_speed, player_index)
            initial_contact_red[player_index] = True
            print("INITIAL HIT - RED")

        # Remove hit brick from user interface as well as the 'bricks' list:
        brick.reset()
        bricks[player_index].remove(brick)

        # If number of bricks hit has crossed either the 4-hit or 12-hit threshold, increase ball speed:
        if bricks_hit[player_index] == 4 or bricks_hit[player_index] == 12:
            # print(f"Player {player_index + 1}: HIT {bricks_hit[player_index]}")
            ball.speed_up(ball_speed, player_index)

        # print(f"Length of bricks list (current player): {len(bricks[player_index])}")
        # print(f"Length of bricks list (other player): {len(bricks[abs(player_index - 1)])}")
        # print(f"Bricks hit (current player): {bricks_hit[player_index]}")
        # print(f"Bricks hit (other player): {bricks_hit[abs(player_index - 1)]}")
        # print(f"Total scores: {total_scores}")

        # Turn screen tracer back on:
        screen.tracer(1)

        # Bounce ball:
        # print(f"Ball speed: {ball_speed}")
        ball.bounce_y()


def check_for_contact_top_wall(player_index, ball, paddle, paddle_length, initial_contact_top_wall):
    if ball.check_for_contact_top_wall():  # Ball has hit top wall.
        if not initial_contact_top_wall[player_index]:  # 1st contact with top wall has been made.
            print(f"Player {player_index + 1}: HIT TOP WALL")
            # Shrink paddle:
            paddle_length[player_index] = paddle_length[player_index] * 0.5
            paddle.shapesize(0.5, paddle_length[player_index])

            # Update tracker
            initial_contact_top_wall[player_index] = True

    return initial_contact_top_wall



def config_screen(screen):
    """Function for configuring the application window (screen)"""
    # Configure the application window (screen):
    screen.setup(width=600, height=800)
    screen.bgcolor("black")
    screen.cv._rootwindow.resizable(False, False)
    screen.title("My Breakout Game")


def create_and_config_bricks(bricks, player_index, levels_cleared):
    """Function for creating and configuring each of the bricks on the user interface"""
    # Create and configure each of the bricks:
    x, y = -268, 130
    for i in range(0, 8):  # Number of rows
        for j in range(0, 14):  # Number of bricks per row
            # Create a new brick object, position it on the screen, and add it to the 'bricks' list:
            if levels_cleared == [0,0]:
                bricks[player_index].append(Brick((x, y), brick_colors[i]))
                bricks[player_index + 1].append(Brick((x, y), brick_colors[i]))

            else:
                bricks[player_index].append(Brick((x, y), brick_colors[i]))

            # Increment x right-ward by one brick column:
            x += 40.5

        # Reset x position back to left of screen and increment y by one row upwards:
        x = -268
        y += 15

    if player_index == 0:
        for brick in bricks[player_index + 1]:
            brick.hideturtle()


def create_and_config_user_interface(ball_speed, turns_remaining, screen, initial_contact_orange, initial_contact_red, initial_contact_top_wall, bricks, bricks_hit, total_scores, levels_cleared, paddle_length):
    """Function for creating and configuring the user interface, including the application window (screen), walls, paddle, game ball, and scoreboard"""
    # global paddle, scoreboard, ball, turns_remaining, screen, bricks, bricks_hit, initial_contact_orange, initial_contact_red, initial_contact_top_wall, total_scores, levels_cleared, paddle_length

    # global paddle, scoreboard, ball

    bricks = [[], []]
    bricks_hit = [0, 0]
    total_scores = [0, 0]
    levels_cleared = [0, 0]

    initial_contact_orange = [False, False]
    initial_contact_red = [False, False]
    initial_contact_top_wall = [False, False]

    screen.tracer(0)

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

    return ball, paddle


def create_and_config_walls():
    """Function for creating and configuring each of the walls on the user interface"""
    # Create and configure each of the walls for the user interface:
    wall_left = Wall((-294, 300), "left")
    wall_right = Wall((286, 300), "right")
    wall_top = Wall((0, 400), "top")
    wall_score_left = Wall((-250, 335), "score_left")
    wall_score_right = Wall((80, 335), "score_right")


def implement_screen_listening(screen, paddle):
    """Function toSpecify window inputs for screen to "listen" for"""
    screen.onkey(paddle.go_left, "Left")
    screen.onkey(paddle.go_right, "Right")
    screen.onkey(pause_game, "Escape")


def pause_game():
    """Function which pauses the game.  Player receives a messagebox to click on OK when game resumption is desired"""
    # Upon pressing the ESC key, display the message box and wait for player confirmation to resume game:
    messagebox.showinfo("GAME PAUSED",
                        "Click on OK to resume game.")


def show_or_hide_bricks(bricks, player_index):
    """Function for showing one player's game board (bricks) and hiding the other's.  This occurs in 2-player mode"""

    # Hide the game board (bricks) for the player that is relinquishing game control:
    for brick in bricks[abs(player_index - 1)]:
        brick.hideturtle()

    # Show the game board (bricks) for the player that is assuming game control:
    for brick in bricks[player_index]:
        brick.showturtle()


def switch_player(player_index_to_switch_to, screen, ball, ball_speed, paddle, paddle_length, bricks):
    """Function to show the game board to that belonging to the player to whom game control is being switched"""
    # Turn screen tracer off until updates have been fully completed:
    screen.tracer(0)

    # Hide the game board (bricks) belonging to the player relinquishing game control, and show the game board (bricks) belonging to the
    # player who is assuming game control.  This occurs in 2-player mode:
    show_or_hide_bricks(bricks, player_index_to_switch_to)

    # Reset the paddle size and position to reflect the current game board for the player assuming game control;:
    paddle.reset(paddle_length[player_index_to_switch_to])

    # Reset the ball speed to reflect the current game board for the player assuming game control:
    ball.speed(ball_speed[player_index_to_switch_to])

    # Turn screen tracer back on:
    screen.tracer(1)

    # Inform the player assuming game control that it is his/her turn to play:
    messagebox.showinfo(f"Player {player_index_to_switch_to + 1}", f"Player {player_index_to_switch_to + 1}: TIME TO PLAY!")

    return player_index_to_switch_to
