import pygame

pygame.init()
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
available_to_fire_set = set((a, b) for a in range(1, 11) for b in range(1, 11))
around_hit_set = set()
hit_blocks = set()
dotted = set()
dotted_to_shot = set()
for_comp_to_shot = set()
last_hits = []
destroyed_ships = []
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

pygame.display.set_caption("Sea Battle")
screen = pygame.display.set_mode(SIZE)
FONT_SIZE = int(BLOCK_SIZE / 1.5)
font = pygame.font.SysFont('notosans', FONT_SIZE)
GAME_OVER = pygame.font.SysFont('notosans', 3 * BLOCK_SIZE)
human = ""
computer = ""
human_ships = ""
computer_ships = ""

DISTANCE = 15
GRID_SIZE = 10
MAX_DELAY_FOR_COMPUTER_SHOT = 700
MAX_DIGIT = 10
MAX_COORDINATE_VALUE = 10
MIN_COORDINATE_VALUE = 1
MIN_X = 100
MAX_X = 600
MIN_Y = 80
MAX_Y = 580
GRID_OFFSET = 10
RECTANGLE_X = 650
RECTANGLE_Y = 332
RECTANGLE_WIDTH = 154
RECTANGLE_HEIGHT = 72
MAX_X_OFFSET = 15
BUTTON_BLOCK_OFFSET = 4
BUTTON_MARGIN = 40
TEXT_MARGIN = 20
GRID_LIMIT = 11
FIVE = 5
SEVEN = 7
