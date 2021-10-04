# CS 3100 Team 8
# Spring 2021
#
# This file specifies a function to display the How To Play screen.\

import pygame as pg
from button import Button
import sys

def how_to(window):
	# Title and background
	pg.display.set_caption("Space Blocks")
	bg_img = pg.image.load("main_menu_background.jpg")
	logo = pg.image.load("logo.png")

	# Store the width and height of the window
	s_width = window.get_width()
	s_height = window.get_height()

	# Button colors
	light_color = ("#50dbd4")	# light teal
	dark_color = ("#27aca5")	# dark teal
	white = (255, 255, 255) # white	
	black = (0, 0, 0) # black

	# Load default mascot
	mascot = pg.image.load("mascot_start_screen.png").convert_alpha()
	mascot_width = mascot.get_width()
	mascot_pos = (100, (s_height - mascot_width)/2)
	mascot_small = pg.transform.rotozoom(mascot, 0, 0.75)

	# Define button dimensions
	button_width = 600
	button_height = 60

	# Create the logo above the PLAY button
	logo_width = 1074
	logo_height = 336
	logo_pos = ((s_width - (logo_width * 0.75))/2, (s_height - (logo_height * 3.25))/2)
	logo_small = pg.transform.rotozoom(logo, 0, 0.75)

	# Create the text positions in the center top
	pos1 = ((s_width)/2, (s_height)/3)
	pos2 = (pos1[0], pos1[1] + button_height + 10)
	pos3 = (pos1[0], pos1[1] + 2*(button_height + 10))
	pos4 = (pos1[0], pos1[1] + 3*(button_height + 10))

	# Create the QUIT button in the bottom left corner
	quit_pos = (10, s_height - button_height - 10)
	quit_button = Button(quit_pos, button_width/2, button_height, text='EXIT GAME')

	# Create the BACK button in the bottom right corner
	back_pos = (s_width - button_width/2 - 10, s_height - button_height - 10)
	back_button = Button(back_pos, button_width/2, button_height, text='BACK')

	# Define a new surface for the text background
	space_blue = "#0e135c"
	play_bg = space_blue
	area = pg.Surface((1500, 400))
	area.set_alpha(200)
	area.fill(play_bg)

	# List of all buttons on this window
	button_list = [quit_button, back_button]

	# Define the text boxes and their centers
	font = pg.font.Font('freesansbold.ttf', 32)
	text1 = font.render('Welcome to Space Blocks!', True, white)
	text2 = font.render('Use the left-right arrow keys to move and the up arrow key to rotate!', True, white)
	text3 = font.render('Use the down arrow key to speed up and the space bar to instantly drop!', True, white)
	text4 = font.render('Blocks will only drop faster as time goes on! Good luck!', True, white)
	textrect1 = text1.get_rect()
	textrect1.center = (pos1)
	textrect2 = text2.get_rect()
	textrect2.center = (pos2)
	textrect3 = text3.get_rect()
	textrect3.center = (pos3)
	textrect4 = text4.get_rect()
	textrect4.center = (pos4)

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
					# Exit application
					sys.exit()
					break
				
				# If the mouse is positioned over the PLAY button
				if back_button.is_over(mouse):
					# Return to the menu loop
					running = False
					break

		# Fill background image
		window.blit(bg_img, (0, 0))

		# Fill text box and border
		window.blit(area, ((s_width)/9, (s_height)/4))
		pg.draw.rect(window, black, ((s_width)/9, (s_height)/4, 1500, 400), 5)

		# Place logo
		window.blit(logo_small, logo_pos)

		# Place mascot
		window.blit(mascot_small, mascot_pos)

		# Render text
		window.blit(text1, textrect1)
		window.blit(text2, textrect2)
		window.blit(text3, textrect3)
		window.blit(text4, textrect4)

		# Draw the buttons one at a time, checking if mouse is hovering
		for button in button_list:
			if button.is_over(mouse):
			    button.draw(window, light_color)
			else:
				button.draw(window, dark_color)

		# Updates the frame
		pg.display.update()

	return