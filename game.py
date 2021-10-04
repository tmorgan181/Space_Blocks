# CS 3100 Team 8
# Spring 2021
#
# This file defines various functions related to gameplay mechanics,
# including the start_game function, which launches the game window
# and begins a session of the game.

import pygame as pg
import random
import sys
# Button class
from button import Button
# Import database functions
import leaderboard as lb
# Loss screen functions
from game_over import show_game_over

# Scoring System
score = 0
dif_mult = 1
line_clears = 0
combo = 1

# Determine the width and height of the play area based on the given block_size
block_size = 35 # in pixels
play_width = 10 * block_size # 10 blocks per row
play_height = 20 * block_size # 20 blocks per col

# Store the width and height of the window
s_width = 1600
s_height = 800

# Determine the top left corner of the play area relative to the whole window
top_left_x = (s_width - play_width)/2
top_left_y = (s_height - play_height) - 50
tl_x = top_left_x
tl_y = top_left_y

# Color codes
white = (255,255,255)
grey = (128,128,128)
black = (0,0,0)

red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
light_blue = (0, 255, 255)
blue = (0, 0, 255)
pink = (128, 0, 128)

dark_blue = "#0e135c"

pink = "#d83dd7"
light_blue = "#50dbd4"
dark_purple = "#751077"
navy_blue = "#2e3192"
grey_blue = "#485c8f"
pale_mint = "#b4dbde"
pale_purple = "#8e75bc"

# Variable to adjust play area background color
play_bg = dark_blue



# Shape formats
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],

     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],

     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],

     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],

     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],

     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],

     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],

     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],

     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],

     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],

     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],

     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],

     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# Indices 0 - 6 represent shapes and their matching colors
shapes = [S, Z, I, O, J, L, T]
shape_colors = [pink, light_blue, dark_purple, pale_purple, pale_mint, navy_blue, grey_blue]

# Piece objects are used to represent each tetromino on the board.
class Piece():
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

# Define a 2d list grid datastructure, which represents the game's play area
# Each element in the grid is a tuple color code to fill the grid square
def create_grid(locked_positions={}):
    # Create a 20 row x 10 col grid, and fill every element with the alpha color code
    grid = [[play_bg for x in range(10)] for x in range(20)]

    # Check for positions that should be filled in with a different color
    # (i.e. there is a piece present in this position)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                # Get the color val of the position
                color_val = locked_positions[(j, i)]
                # Set the corresponding grid element's value to match
                grid[i][j] = color_val

    return grid

# Transition from the text-based shape formats (found above), to the corresponding positions
def convert_shape_format(piece):
    # List to store the filled positions of the shape
    positions = []
    # Get the sub-list that represents the current rotation of the shape
    curr_format = piece.shape[piece.rotation % len(piece.shape)]

    # Loop over each coordinate in the format
    for i, line in enumerate(curr_format):
        row = list(line)
        for j, column in enumerate(row):
            # If the format contains a '0' at this coordinate
            if column == '0':
                # Append the corresponding position to the list
                positions.append((piece.x + j, piece.y + i))

    # Account for offset from the formats
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    # Create a list of all acceptable positions (i.e. (0,0) through (10,20))
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == play_bg] for i in range(20)]
    # Convert the 2d list into a 1d list
    accepted_pos = [j for sub in accepted_pos for j in sub]

    # Get all positions from the given piece
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    # Check for any positions with a y-value less than 1
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
  return Piece(5, 1, random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    font = pg.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))

def draw_grid_lines(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pg.draw.line(surface, black, (sx, sy+ i*block_size), (sx + play_width, sy + i * block_size))  # horizontal lines
        for j in range(col):
            pg.draw.line(surface, black, (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))  # vertical lines

def clear_rows(grid, locked):
  # need to see if row is clear then shift every other row above down one
  global score
  global line_clears
  global combo
  global dif_mult
  inc = 0
  for i in range(len(grid)-1,-1,-1):
      row = grid[i]
      if play_bg not in row:
          inc += 1
          # add positions to remove from locked
          ind = i
          for j in range(len(row)):
              try:
                  del locked[(j, i)]
              except:
                  continue
  if inc > 0:
      for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
          x, y = key
          if y < ind:
              newKey = (x, y + inc)
              locked[newKey] = locked.pop(key)
  if inc == 1:
      score += 40 * dif_mult * combo 
  elif inc == 2:
      score += 100 * dif_mult * combo 
  elif inc == 3:
      score += 300 * dif_mult * combo 
  elif inc == 4:
      score += 1000 * dif_mult * combo 
  dif_mult = 1 + ((line_clears // 5) / 10)
  print(dif_mult)
# rudimentary combo system, more score for more line clears in a row
  line_clears += inc
  if inc > 0:
  	combo += inc
  else:
  	combo = 1

def update_score(surface):
  font = pg.font.SysFont('comicsans', block_size)
  label = font.render('Score: ' + str(int(score)), 1, (255,255,255))
  sx = top_left_x + play_width + 50
  sy = top_left_y + play_height/2 - 100
  surface.blit(label, (sx + 10, sy - 2*block_size))

def update_combo(surface):
  font = pg.font.SysFont('comicsans', block_size)
  label = font.render('Combo: ' + str(combo-1), 1, (255,255,255))
  sx = top_left_x + play_width + 50
  sy = top_left_y + play_height/2 - 100
  surface.blit(label, (sx + 10, sy - 3*block_size))

def update_level(surface):
  font = pg.font.SysFont('comicsans', block_size)
  label = font.render('Level: ' + str((line_clears // 5)+1), 1, (255,255,255))
  sx = top_left_x + play_width + 50
  sy = top_left_y + play_height/2 - 100
  surface.blit(label, (sx + 10, sy - 4*block_size))

def update_line_clears(surface):
  font = pg.font.SysFont('comicsans', block_size)
  label = font.render('Lines Cleared: ' + str(line_clears), 1, (255,255,255))
  sx = top_left_x + play_width + 50
  sy = top_left_y + play_height/2 - 100
  surface.blit(label, (sx + 10, sy - 5*block_size))

def draw_next_shape(shape, surface):
    font = pg.font.SysFont('comicsans', block_size)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pg.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - block_size))

def draw_window(surface, grid):
    bg_img = pg.image.load("main_menu_background.jpg")
    surface.blit(bg_img, (0, 0))

    # Define logo and make it smaller so it fits above board
    logo = pg.image.load("logo.png").convert_alpha()
    logo_small = pg.transform.rotozoom(logo, 0, 0.35)

    # Define mascot for the game screen
    mascot = pg.image.load("mascot_start_screen.png").convert_alpha()
    mascot_small = pg.transform.rotozoom(mascot, 0, 0.75)

    # Display background and mascot
    surface.blit(bg_img, (0, 0))
    surface.blit(mascot_small, ((top_left_x - 550), (top_left_y + play_height / 2 - (mascot_small.get_height() / 2))))


    # Define a new surface for the play area background
    area = pg.Surface((play_width, play_height))
    area.set_alpha(200)
    area.fill(play_bg)
    surface.blit(area, (top_left_x, top_left_y))

    # Tetris Title
    font = pg.font.SysFont('comicsans', 60)
    #label = font.render('SPACE BLOCKS', 1, (255,255,255))
    #surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # Display logo at the top of the screen
    surface.blit(logo_small, (top_left_x + play_width / 2 - (logo_small.get_width() / 2), 0))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (grid[i][j] != play_bg):
                pg.draw.rect(surface, grid[i][j], (top_left_x + j* block_size, top_left_y + i * block_size, block_size, block_size), 0)

    # draw grid and border
    draw_grid_lines(surface, 20, 10)
    pg.draw.rect(surface, black, (top_left_x, top_left_y, play_width, play_height), 5)

def start_game(window):
    global score
    global line_clears
    print("Starting the game!")

    # Button colors
    light_color = ("#50dbd4") # light teal
    dark_color = ("#27aca5")  # dark teal

    # Store the width and height of the window
    s_width = window.get_width()
    s_height = window.get_height()

    # Define button dimensions
    button_width = 600
    button_height = 60

    # Create the QUIT button in the bottom left corner
    quit_pos = (10, s_height - button_height - 10)
    quit_button = Button(quit_pos, button_width/2, button_height, text='EXIT GAME')

    # Create the BACK button in the bottom right corner
    back_pos = (s_width - button_width/2 - 10, s_height - button_height - 10)
    back_button = Button(back_pos, button_width/2, button_height, text='BACK')
    button_list = [quit_button, back_button]

    # Fill background image
    bg_img = pg.image.load("main_menu_background.jpg")
    window.blit(bg_img, (0, 0))

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    running = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pg.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    score = 0
    line_clears = 0
    play_again = False
    done = []
    limit = 5

    while running:
        # Store the current mouse coordinates
        mouse = pg.mouse.get_pos()

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            
            # If the mouse is clicked
            if event.type == pg.MOUSEBUTTONDOWN:
              # If the mouse is positioned over the QUIT button
              if quit_button.is_over(mouse):
                # Exit application
                sys.exit()

              # If the mouse is positioned over the BACK button
              if back_button.is_over(mouse):
                running = False
                break

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pg.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pg.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                # move shape down
                if event.key == pg.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                # Full drop on spacebar
                if event.key == pg.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            clear_rows(grid, locked_positions)

        draw_window(window, grid)
        draw_next_shape(next_piece, window)
        update_line_clears(window)
        update_level(window)
        update_score(window)
        update_combo(window)

        # Draw the buttons one at a time, checking if mouse is hovering
        for button in button_list:
          # Highlight buttons when moused over
          if button.is_over(mouse):
              button.draw(window, light_color)
          else:
            button.draw(window, dark_color)

        # Update the fall speed every five line clears,
        if ((line_clears > limit-1) and (line_clears//limit not in done)):
          done.append(line_clears//limit)
          print(done)
          fall_speed *= (.9 ** (line_clears // limit))
          print("Clears:", line_clears)
          print("Fall speed decreased:", fall_speed)

        pg.display.update()

        # Check if user lost
        if check_lost(locked_positions):
          # Display the loss screen and get the return value
          play_again = show_game_over(window, score)
          score = 0
          line_clears = 0
          done = []
          running = False

    pg.display.update()

    if play_again:
      start_game(window)