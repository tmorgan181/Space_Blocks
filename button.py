# CS 3100 Team 8
# Spring 2021
#
# This file defines the Button class. Button objects are used to display interactive
# button elements in various menus, and can optionally have text overlayed onto them.

import pygame as pg

class Button():
	def __init__(self, pos, width, height, text=''):
	    self.pos = pos
	    self.width = width
	    self.height = height
	    self.text = text

    # Call this method to draw the button on the window
	def draw(self, window, color):
		pg.draw.rect(window, "black", (self.pos[0]-2, self.pos[1]-2, self.width+4, self.height+4), 3)
		pg.draw.rect(window, color, (self.pos[0], self.pos[1], self.width, self.height), 0)

		if self.text != '':
			font = pg.font.SysFont('comicsans', 35)
			text = font.render(self.text, 1, (0,0,0))
			window.blit(text, (self.pos[0] + (self.width/2 - text.get_width()/2), self.pos[1] + (self.height/2 - text.get_height()/2)))

	# Pos is the mouse position or a tuple of (x,y) coordinates
	def is_over(self, pos):
	    if pos[0] > self.pos[0] and pos[0] < self.pos[0] + self.width:
	        if pos[1] > self.pos[1] and pos[1] < self.pos[1] + self.height:
	            return True

	    return False