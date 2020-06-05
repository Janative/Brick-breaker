"""
File: brickbreaker.py
----------------
YOUR DESCRIPTION HERE
"""

import tkinter
import time
import random

# How big is the playing area?
CANVAS_WIDTH = 600  # Width of drawing canvas in pixels
CANVAS_HEIGHT = 800  # Height of drawing canvas in pixels

# Constants for the bricks
N_ROWS = 10  # How many rows of bricks are there?
N_COLS = 10  # How many columns of bricks are there?
SPACING = 5  # How much space is there between each brick?
BRICK_START_Y = 50  # The y coordinate of the top-most brick
BRICK_HEIGHT = 20  # How many pixels high is each brick
BRICK_WIDTH = (CANVAS_WIDTH - (N_COLS + 1) * SPACING) / N_COLS

# Constants for the ball and paddle
BALL_SIZE = 40
PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_WIDTH = 80


def main():

    #creating the canvas
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Brick Breaker')

    # Creating and looping the bricks
    for col in range(N_COLS):
        for row in range(N_ROWS):
            create_brick(canvas, row, col)

    # Introducing counter and bricks remaining
    counter = 0
    bricks_remaining = 100

    # Starting the game
    while counter == 3:
       print("I ma sorry, you ran out of lives.")
    else:
        run_game(canvas, counter,bricks_remaining)


def run_game(canvas, counter, bricks_remaining):


    # create ball
    ball = create_ball(canvas)
    change_x = 10
    change_y = 10

    # create paddle
    paddle = canvas.create_rectangle(0, PADDLE_Y, PADDLE_WIDTH, PADDLE_Y + BRICK_HEIGHT, fill="bisque4", width=0)

    while True:
        # paddle movement
        paddle_x = canvas.winfo_pointerx() - canvas.winfo_rootx() - PADDLE_WIDTH / 2
        canvas.moveto(paddle, paddle_x, PADDLE_Y)

        # ball movement
        canvas.move(ball, change_x, change_y)
        if hit_top(canvas, ball):
            change_y *= -1
        if hit_bottom(canvas, ball):
            game_over(canvas, counter)
        if hit_right(canvas, ball) or hit_left(canvas, ball):
            change_x *= -1
        if hit_brick(canvas, ball, paddle, bricks_remaining):
            change_y *= -1

            if bricks_remaining == 0:
                print("congratulations!")
                break

        # pause
        time.sleep(1 / 30.)
        canvas.update()

    # Pause (sleep)
    canvas.mainloop()


def create_brick(canvas, row, col):
    x = (BRICK_WIDTH + SPACING) * col + SPACING
    y = BRICK_START_Y + (BRICK_HEIGHT + SPACING) * row
    brick_color_list = ["indian red1", "indian red1", "navajo white", "navajo white", "khaki1", "khaki1",
                        "yellow green", "yellow green", "turquoise2", "turquoise2"]
    rect = canvas.create_rectangle(x, y, x + BRICK_WIDTH, y + BRICK_HEIGHT, width=0, fill=brick_color_list[row])
    return rect


def create_ball(canvas):
    x = (CANVAS_WIDTH - BALL_SIZE) / 2
    y = (CANVAS_HEIGHT - BALL_SIZE) / 2

    return canvas.create_oval(x, y, x + BALL_SIZE, y + BALL_SIZE, fill="brown4", width=0)


def hit_bottom(canvas, ball):
    ball_y = get_top_y(canvas, ball)
    return ball_y > CANVAS_HEIGHT - BALL_SIZE


def hit_right(canvas, ball):
    ball_x = get_left_x(canvas, ball)
    return ball_x > CANVAS_WIDTH - BALL_SIZE


def hit_left(canvas, ball):
    ball_x = get_left_x(canvas, ball)
    return ball_x < 0


def hit_top(canvas, ball):
    ball_y = get_top_y(canvas, ball)
    return ball_y < 0


def hit_brick(canvas, ball, paddle, bricks_remaining):
    ball_coords = canvas.coords(ball)
    x_1 = ball_coords[0]
    y_1 = ball_coords[1]
    x_2 = ball_coords[2]
    y_2 = ball_coords[3]

    colliding_list = canvas.find_overlapping(x_1, y_1, x_2, y_2)

    if len(colliding_list) > 1:
        for obj in colliding_list:
            if obj == ball or obj == paddle:
                return len(colliding_list) > 1
            else:
                bricks_remaining -= 1
                canvas.delete(obj)
                return len(colliding_list) > 1



def game_over(canvas, counter):
    if counter == 0 or counter == 1:
        message = input(canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text="Game is over, loser! You have 2 more tries. \nWould you like to try again? (y/n)", fill='red', font="Arial 20 bold", anchor="s"))
        counter += 1
        if message:
            return counter


    elif counter == 2:
        message = canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text="Game is over, loser! You have 1 more try.", fill='red', font="Arial 20 bold", anchor="s")
        counter += 1
        return counter

    else:
        canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text="Game is over, loser!", fill='red', font="Arial 20 bold", anchor="s")
        counter += 1
        return counter


def get_top_y(canvas, ball):
    '''
    This friendly method returns the y coordinate of the top of an object.
    Recall that canvas.coords(object) returns a list of the object
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 1 is the top-y
    '''
    return canvas.coords(ball)[1]


def get_left_x(canvas, ball):
    '''
    This friendly method returns the x coordinate of the left of an object.
    Recall that canvas.coords(object) returns a list of the object
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 0 is the left-x
    '''
    return canvas.coords(ball)[0]


def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas


if __name__ == '__main__':
    main()
