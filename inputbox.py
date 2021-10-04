# CS 3100 Team 8
# Spring 2021
#
# This file defines the InputBox class. These objects are used to display interactive
# input box elements, which allow the user to type and submit some text.
import pygame as pg

grey = "#d6d6d6"
white = "#ffffff"

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = grey
        self.text = text
        font = pg.font.SysFont('freesansbold.ttf', 32)
        self.txt_surface = font.render(text, True, "black")
        self.active = False
        self.submitted = False

    def handle_event(self, event):
        text = ""

        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos) and not self.submitted:
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = white if self.active else grey

        if event.type == pg.KEYDOWN:
            if self.active and not self.submitted:
                if event.key == pg.K_RETURN:
                    text = self.text
                    self.submitted = True
                    self.color = grey
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                font = pg.font.SysFont('freesansbold.ttf', 32)
                self.txt_surface = font.render(self.text, True, "black")

        return text

    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 0)
        pg.draw.rect(screen, "black", self.rect, 3)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
