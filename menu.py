# CS 3100 Team 8
# Spring 2021
#
# This file specifies a function to display the main menu of our Tetris clone.
# From this menu, a user can launch the game, view the leaderboard, navigate to
# the settings menu, or exit the application.

import pygame as pg
import sys
# Import Button class
from button import Button
# Import start_game functions
from game import start_game
from game import s_width, s_height
# Import leaderboard interaction functions
import leaderboard as lb
# Leaderboard screen display functions
from leaderboard_screen import show_leaderboard
# How to play screen function
from how_to_screen import how_to

def start_menu(window):
	# Title and background
	pg.display.set_caption("Space Blocks")
	bg_img = pg.image.load("main_menu_background.jpg")

	# Display logo
	logo = pg.image.load("logo.png").convert_alpha()

	# Button colors
	light_color = ("#50dbd4")	# light teal
	dark_color = ("#27aca5")	# dark teal

	# Store the width and height of the window
	s_width = window.get_width()
	s_height = window.get_height()

	# Load default mascot
	mascot = pg.image.load("mascot_start_screen.png").convert_alpha()
	mascot_width = mascot.get_width()
	mascot_pos = (100, (s_height - mascot_width)/2)
	mascot_small = pg.transform.rotozoom(mascot, 0, 0.8)

	# Load other mascot images
	mascot_settings = pg.image.load("mascot_settings_option.png").convert_alpha()
	settings_small = pg.transform.rotozoom(mascot_settings, 0, 0.75)

	mascot_start = pg.image.load("mascot_start_option.png").convert_alpha()
	start_small = pg.transform.rotozoom(mascot_start, 0, 0.75)

	mascot_tutorial = pg.image.load("mascot_how_to_play_option.png").convert_alpha()
	tutorial_small = pg.transform.rotozoom(mascot_tutorial, 0, 0.75)

	mascot_leaderboard = pg.image.load("mascot_leaderboard_option.png").convert_alpha()
	leaderboard_small = pg.transform.rotozoom(mascot_leaderboard, 0, 0.65)

	mascot_exit = pg.image.load("mascot_option_selected.png").convert_alpha()
	exit_small = pg.transform.rotozoom(mascot_exit, 0, 0.75)

	# Define button dimensions
	button_width = 600
	button_height = 60

	# Create the logo above the PLAY button
	logo_width = 1074
	logo_height = 336
	logo_pos = ((s_width - logo_width)/2, (s_height - (logo_height * 2.25))/2)

	# Create the QUIT button in the bottom left corner
	quit_pos = (10, s_height - button_height - 10)
	quit_button = Button(quit_pos, button_width/2, button_height, text='EXIT GAME')

	# Create the PLAY button in the center top
	play_pos = ((s_width - button_width)/2, (s_height - button_height)/2)
	play_button = Button(play_pos, button_width, button_height, text='PLAY SPACE BLOCKS')

	# Create the LEADERBOARD button under PLAY
	leaderboard_pos = (play_pos[0], play_pos[1] + button_height + 10)
	leaderboard_button = Button(leaderboard_pos, button_width, button_height, text='LEADERBOARD')

	# Create the HOW TO PLAY button under LEADERBOARD
	how_to_pos = (play_pos[0], play_pos[1] + 2*(button_height + 10))
	how_to_button = Button(how_to_pos, button_width, button_height, text='HOW TO PLAY')

	# Create the SETTINGS button under HOW TO PLAY
	settings_pos = (play_pos[0], play_pos[1] + 3*(button_height + 10))
	settings_button = Button(settings_pos, button_width, button_height, text='SETTINGS')

	# List of all buttons on this window
	button_list = [quit_button, play_button, leaderboard_button, how_to_button, settings_button]

	### MENU LOOP ###
	running = True
	while running:
		# Store the current mouse coordinates
		mouse = pg.mouse.get_pos()

		# Loop through all events
		for event in pg.event.get():
			# If a quit event is found, then exit the application
			if event.type == pg.QUIT:
				# Exit application next iteration
				running = False

			# If the mouse is clicked
			if event.type == pg.MOUSEBUTTONDOWN:
				# If the mouse is positioned over the QUIT button
				if quit_button.is_over(mouse):
					# Exit application next iteration
					running = False
				
				# If the mouse is positioned over the PLAY button
				if play_button.is_over(mouse):
					start_game(window)

				# If the mouse is positioned over the LEADERBOARD button
				if leaderboard_button.is_over(mouse):
					show_leaderboard(window)

				# If the mouse is positioned over the HOW TO PLAY button
				if how_to_button.is_over(mouse):
					how_to(window)

				# If the mouse is positioned over the SETTINGS button
				# if settings_button.is_over(mouse):
				#	settings()

		# Fill background image
		window.blit(bg_img, (0, 0))

		# Place logo on main screen
		window.blit(logo, logo_pos)

		draw_default = True
		# Draw the buttons one at a time, checking if mouse is hovering
		for button in button_list:
			
			# Highlight buttons when moused over
			if button.is_over(mouse):
				button.draw(window, light_color)
				draw_default = False

				# Display start sprite
				if play_button.is_over(mouse):
					window.blit(start_small, mascot_pos)

				# Display leaderboard sprite
				elif leaderboard_button.is_over(mouse):
					window.blit(leaderboard_small, mascot_pos)
				
				# Display settings sprite
				elif settings_button.is_over(mouse):
					window.blit(settings_small, mascot_pos)

				# Display how to play sprite
				elif how_to_button.is_over(mouse):
					window.blit(tutorial_small, mascot_pos)

				elif quit_button.is_over(mouse):
					window.blit(exit_small, mascot_pos)

			else:
				button.draw(window, dark_color)
		
		if draw_default:
			window.blit(mascot_small, mascot_pos)

		# Updates the frame
		pg.display.update()

	# When the loop is finished, destroy the application window
	pg.display.quit()
	sys.exit()
	print("Finished running.")
