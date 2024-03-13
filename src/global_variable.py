import pygame
import copy
from draw import ships


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
ava_to_fire_set = set((a, b)for a in range(1, 11) for b in range(1, 11))
around_hit_set = set()
hit_Bl = set()
dotted = set()
dotted_to_shoot = set()
for_comp_to_shoot = set()
last_hits = []
destroyed_ships = []
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

pygame.display.set_caption("Sea Battle")
screen = pygame.display.set_mode(size)
font_sz = int(block_sz / 1.5)
font = pygame.font.SysFont('notosans', font_sz)
gameover_f = pygame.font.SysFont('notosans', 3 * block_sz)

human = ships()
H_ships_w = copy.deepcopy(human.ships)
computer = ships()
ship_w = copy.deepcopy(computer.ships)
