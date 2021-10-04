# CS 3100 Team 8
# Spring 2021
#
# This file initializes pygame and launches the application.

import pygame as pg

# Import start menu functions
from menu import start_menu
from menu import s_width, s_height

# Import leaderboard functions
import leaderboard as lb

def main():
    # Setup the leaderboard database
    lb.init_database()

    # Init pg constructor
    pg.init()

    # Init pygame sound module and start bg music
    pg.mixer.init()
    pg.mixer.music.load("space_music.mp3")
    pg.mixer.music.play(-1)

    # Create the window
    res = (s_width, s_height)
    window = pg.display.set_mode(res)

    print("Launching menu.")

    # Launch the start menu window
    start_menu(window)

if __name__ == "__main__":
    main()