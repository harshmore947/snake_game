import tkinter as tk
from tkinter import messagebox
import random

game_screen = tk.Tk()

# Game screen top title
game_screen.title("Snake game")

# Game Screen resolution
game_screen.geometry("641x641")

# Game screen bg
game_screen.configure(bg="black")

# Snake body
snake_body = [
    (5, 5),  # head
    (4, 5),  # body
    (3, 5),  # tail
    (2, 5),  # tail
]

direction = (1, 0)


# Screen on close
def on_closing():
    if messagebox.askokcancel("Quit", "Do you really want to quit"):
        game_screen.destroy()


game_screen.protocol("WM_DELETE_WINDOW", on_closing)

canvas = tk.Canvas(game_screen, height=601, width=601, bg="black", highlightthickness=0)


def draw_grid(canvas):
    canvas.pack(padx=20, pady=20)

    for y in range(0, 601, 20):
        canvas.create_line(0, y, 600, y, fill="grey")

    for x in range(0, 601, 20):
        canvas.create_line(x, 0, x, 600, fill="grey")


# Creating a game board
def create_game_board(canvas, snake_body):
    draw_grid(canvas)
    draw_snake(canvas, snake_body)


# Draw snake function
def draw_snake(canvas, snake_body):

    for x, y in snake_body:
        x_pixel = x * 20
        y_pixel = y * 20
        canvas.create_rectangle(
            # now the cordinates as per the rows and columns
            x_pixel,
            y_pixel,
            x_pixel + 20,
            y_pixel + 20,
            fill="green",
            outline="black",
        )


create_game_board(canvas, snake_body)


def move_snake(snake_body, direction, food_position,canvas):
    # Step 1 get the current head of the snake
    current_head = snake_body[0]

    # step 2 Get the current direction
    direction_x = direction[0]
    direction_y = direction[1]

    # step 3 calculate new head postion
    new_x = current_head[0] + direction_x
    new_y = current_head[1] + direction_y

    # step 4 calculate
    new_head = (new_x, new_y)

    if new_head != food_position:
       snake_body.pop()

    # step 5 insert new head
    snake_body.insert(0, new_head)

    # step 6 remove the last tail


    # #step 7  delete all
    # canvas.delete("all")

    # #step 8 render gri
    # draw_grid(canvas)

    # # step 9
    # draw_snake(canvas,snake_body)

def generate_food(snake_body,canvas):
    while True:
        x = random.randint(0,29)
        y = random.randint(0,29)

        position = (x,y)

        if position not in snake_body:
            break

    x_pixel = position[0] * 20
    y_pixel = position[1] * 20

    canvas.create_rectangle(
        x_pixel,
        y_pixel,
        x_pixel + 20,
        y_pixel + 20,
        fill="white",
        outline="black",
    )

    return position



def update_game(canvas, snake_body,food_position):
    # step 1 move snake
    move_snake(snake_body, direction,food_position,canvas)

    # check if the body collision
    if snake_body[0] in snake_body[1:]:
        print("Game Over")
        return

    # wall collison
    if (
        snake_body[0][0] < 0
        or snake_body[0][0] > 29
        or snake_body[0][1] < 0
        or snake_body[0][1] > 29
    ):
        print("Game Over")
        return

    if snake_body[0] ==food_position:
        food_position = generate_food(snake_body,canvas)

    # step 2 clear canvas
    canvas.delete("all")

    # step 3 draw grid
    draw_grid(canvas)

    # step 4 draw snake
    draw_snake(canvas, snake_body)

    # Generate random food
    x_pixel = food_position[0] * 20
    y_pixel = food_position[1] * 20

    canvas.create_rectangle(
            x_pixel,
            y_pixel,
            x_pixel + 20,
            y_pixel + 20,
            fill="white",
            outline="black",
    )

    # 5 timer
    game_screen.after(150, update_game, canvas, snake_body,food_position)


def on_key_press(event):
    print(f"key pressed:{event.char} (Keysym:{event.keysym})")

    global direction

    new_direction = direction

    match event.keysym.lower():
        case "w":
            new_direction = (0, -1)

        case "s":
            new_direction = (0, 1)

        case "a":
            new_direction = (-1, 0)

        case "d":
            new_direction = (1, 0)

    # opposite direction checking if valid then only update the direction
    if new_direction != (-direction[0], -direction[1]):
        direction = new_direction


canvas.bind("<Key>", on_key_press)

food_position = generate_food(snake_body,canvas)
update_game(canvas, snake_body,food_position)
canvas.focus_set()
game_screen.mainloop()
