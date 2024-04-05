"""Модуль для глобальных значений"""
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 180, 180)
RED = (255, 0, 0)
GREY = (0, 200, 50)
LIGHT_GRAY = (100, 200, 0)
DARK_RED = (75, 0, 0)
BLOCK_SIZE = 50
LEFT_MARGIN = 100
UP_MARGIN = 80
SIZE = (LEFT_MARGIN + 30 * BLOCK_SIZE, UP_MARGIN + 15 * BLOCK_SIZE)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

screen: pygame.surface.Surface
FONT_SIZE: int
FONT: pygame.font.Font
GAME_OVER: pygame.font.Font


DISTANCE = 15
GRID_SIZE = 10
MAX_DELAY_FOR_COMPUTER_SHOT = 700
MAX_COORDINATE_VALUE = 10
MIN_COORDINATE_VALUE = 1
MIN_X = 100
MAX_X = 600
MIN_Y = 80
MAX_Y = 580
RECTANGLE_X = 650
RECTANGLE_Y = 332
RECTANGLE_WIDTH = 154
RECTANGLE_HEIGHT = 72
BUTTON_BLOCK_OFFSET = 4
BUTTON_MARGIN = 40
TEXT_MARGIN = 20
GRID_LIMIT = 11
SHIPS_LIMIT = 5
DIVIDE = 7
IS_PYGAME_INIT = False
