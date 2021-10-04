# CS 3100 Team 8
# Spring 2021
#
# This file contains the functions needed to display the game over screen after a
# session is completed. If the final score of the game is a new high score, it
# will prompt the user to enter their name and add the score to the database.

import pygame as pg
import sys
from button import Button
import leaderboard as lb
from inputbox import InputBox

def show_game_over(window, score):
	# Button colors
	light_color = ("#50dbd4")	# light teal
	dark_color = ("#27aca5")	# dark teal

	# Store the width and height of the window
	s_width = window.get_width()
	s_height = window.get_height()

	# Define button dimensions
	button_width = 600
	button_height = 60

	# Define the game over screen dimensions and position
	g_width = 380
	g_height = 600
	g_x = (s_width - g_width) / 2
	g_y = (s_height - g_height) / 2
	g_radius = 30

	# Load game over image and determine placement position
	img = pg.image.load("game_over_round.png")
	img_width = img.get_width()
	img_pos = (g_x+4, g_y+4)
	img_small = pg.transform.scale(img, (g_width-8, g_height-8))

	# Create the QUIT button in the bottom left corner
	quit_pos = (10, s_height - button_height - 10)
	quit_button = Button(quit_pos, button_width/2, button_height, text='EXIT GAME')

	# Create the BACK button in the bottom right corner
	back_pos = (s_width - button_width/2 - 10, s_height - button_height - 10)
	back_button = Button(back_pos, button_width/2, button_height, text='BACK')

	# Create the PLAY AGAIN button on the game over screen
	play_again_pos = (g_x + (g_width - button_width/2)/2, g_y + (g_height - 100))
	play_again_button = Button(play_again_pos, button_width/2, button_height, text='PLAY AGAIN')

	# List of all buttons on this window
	button_list = [quit_button, back_button, play_again_button]

	# Retrieve the top ten scores to be placed in the table
	table_data = lb.return_top_ten()
	# print(table_data)

	# Define a text box for the user's name
	box_w = 300
	box_h = 60
	# InputBox(x, y, w, h)
	name_box = InputBox(g_x + (g_width - box_w)/2, g_y + (g_height - 450), box_w, box_h)
	input_boxes = [name_box]

	### MENU LOOP ###
	running = True
	while running:
		# Store the current mouse coordinates
		mouse = pg.mouse.get_pos()

		# Loop through all events
		for event in pg.event.get():
			# If a quit event is found, then exit the application
			if event.type == pg.QUIT:
				# Exit application
				sys.exit()

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

				# If mouse is over play again, then launch another game session
				if play_again_button.is_over(mouse):
					running = False
					return True

			# Handle input box events
			for box in input_boxes:
				output = box.handle_event(event)
				if output != "":
					print("Submission received:", output, "/", score)
					lb.add_entry(output, score)

		# Create a rectangle to outline the game over screen
		pg.draw.rect(window, "black", (g_x, g_y, g_width, g_height), border_radius=g_radius)
		window.blit(img_small, img_pos)

		# Draw the GAME OVER text
		text = "GAME OVER"
		font = pg.font.SysFont('freesansbold.ttf', 64)
		label = font.render(text, 1, "white")
		window.blit(label, (g_x + 50, g_y + 40))

		# Draw the Final Score text
		text = "Final Score:    " + str(int(score))
		font = pg.font.SysFont('freesansbold.ttf', 32)
		label = font.render(text, 1, "white")
		window.blit(label, (g_x + 50, g_y + 100))

		# Draw the buttons one at a time, checking if mouse is hovering
		for button in button_list:
			# Highlight buttons when moused over
			if button.is_over(mouse):
					button.draw(window, light_color)
			else:
				button.draw(window, dark_color)

		# Draw the input box
		for box in input_boxes:
			box.draw(window)

		# Updates the frame
		pg.display.update()

	return False