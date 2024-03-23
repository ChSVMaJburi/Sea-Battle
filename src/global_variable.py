import pygame
import copy
from drawer import Shipyard

pygame.init()
WH = (255, 255, 255)
BL = (0, 0, 0)
BLUE = (0, 180, 180)
RED = (255, 0, 0)
GR = (0, 200, 50)
L_GRAY = (100, 200, 0)
RB = (75, 0, 0)
block_sz = 50
l_margin = 100
upp_margin = 80
size = (l_margin + 30 * block_sz, upp_margin + 15 * block_sz)
ava_to_fire_set = set((a, b) for a in range(1, 11) for b in range(1, 11))
around_hit_set = set()
hit_Bl = set()
dotted = set()
dotted_to_shot = set()
for_comp_to_shot = set()
last_hits = []
destroyed_ships = []
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

pygame.display.set_caption("Sea Battle")
screen = pygame.display.set_mode(size)
font_sz = int(block_sz / 1.5)
font = pygame.font.SysFont('notosans', font_sz)
gameover_f = pygame.font.SysFont('notosans', 3 * block_sz)

human = Shipyard()
H_ships_w = copy.deepcopy(human.ships)
computer = Shipyard()
ship_w = copy.deepcopy(computer.ships)

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