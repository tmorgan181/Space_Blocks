# CS 3100 Team 8
# Spring 2021
#
# This file defines functions to display the top ten high scores
# on the leaderboard screen.

# Exit application
import sys
# Pygame functions
import pygame as pg
# Button class
from button import Button
# Database interaction functions
import leaderboard as lb

# Display the top ten scores in a table
def show_leaderboard(window):
	# Title and background
	pg.display.set_caption("Space Blocks")
	bg_img = pg.image.load("leaderboard_background.jpg")

	# Button colors
	light_color = ("#50dbd4")	# light teal
	dark_color = ("#27aca5")	# dark teal

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

	# List of all buttons on this window
	button_list = [quit_button, back_button]

	# Retrieve the top ten scores to be placed in the table
	table_data = lb.return_top_ten()
	# print(table_data)

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

		# Fill background image
		window.blit(bg_img, (0, 0))

		# Draw the buttons one at a time, checking if mouse is hovering
		for button in button_list:
			# Highlight buttons when moused over
			if button.is_over(mouse):
					button.draw(window, light_color)
			else:
				button.draw(window, dark_color)

		# Draw the grid of boxes for the table, and fill in the text from the database
		box_width = [100, 250, 250]
		box_height = 50
		start_x = (s_width/2) - ((box_width[0] + box_width[1] + box_width[2]) / 2)
		start_y = (s_height/2) - (5.5 * box_height) + 100
		x = start_x
		y = start_y
		for i in range(11):
			for j in range(3):
				# Create a surface to be filled
				box = pg.Surface((box_width[j], box_height))
				if (i != 0):
					box.fill(light_color)
				else:
					box.fill(dark_color)
				window.blit(box, (x, y))
				# Draw an outline around the box
				pg.draw.rect(window, "black", (x, y, box_width[j], box_height), 3)

				# Create text labels for the column headers
				if (i == 0):
					t = ["Rank", "Name", "Score"]
					text = t[j]
					font = pg.font.SysFont('freesansbold.ttf', 32, bold=True)
					label = font.render(text, 1, "black")
					window.blit(label, (x + 20, y + 20))

				# Now we have to populate the table with the score entries
				# Check if there is data available for this row
				if (i > 0 and i < len(table_data) + 1):
					# The rank is simply == i
					if (j == 0):
						text = str(i)
					# The other text is found from the table data
					else:
						text = str(table_data[i - 1][j])

					# Create a text label and place it in the box
					font = pg.font.SysFont('freesansbold.ttf', 32)
					label = font.render(text, 1, "black")
					window.blit(label, (x + 20, y + 20))

				# Move to the right
				x += box_width[j]

			# Reset the position for the next row
			x = start_x
			y += box_height

		# Updates the frame
		pg.display.update()

	return