from button import button
import global_variable as glob
from drawer import Drawer
from Grid import Grid

import pygame
import messages
import game_logic as logic

pygame.init()

st_game = glob.l_margin + glob.GRID_SIZE * glob.block_sz
st_button = button(st_game, "START GAME")


def main():
    glob.screen.fill(glob.BLUE)
    f = True
    Grid("COMPUTER", 0)
    Grid("HUMAN", glob.DISTANCE)
    Drawer.ship(glob.human.ships)
    game_over = False
    comp_turn = False
    while f:
        st_button.draw_button()
        st_button.change_color_on_hover()
        pygame.display.update()
        m = pygame.mouse.get_pos()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                f = False
            elif i.type == pygame.MOUSEBUTTONDOWN and st_button.rect.collidepoint(m):
                f = False
        pygame.display.update()
        glob.screen.fill(glob.BLUE, (glob.RECTANGLE_X, glob.RECTANGLE_Y, glob.RECTANGLE_WIDTH, glob.RECTANGLE_HEIGHT))

    while not game_over:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                game_over = True
            elif not comp_turn and i.type == pygame.MOUSEBUTTONDOWN:
                x, y = i.pos
                if glob.MIN_X <= x <= glob.MAX_X and glob.MIN_Y <= y <= glob.MAX_Y:
                    if (glob.l_margin < x < glob.l_margin + glob.GRID_OFFSET * glob.block_sz) and (
                            glob.upp_margin < y < glob.upp_margin + glob.GRID_OFFSET * glob.block_sz):
                        f = 0
                        shot_coordinates = ((x - glob.l_margin) // glob.block_sz + 1,
                                            (y - glob.upp_margin) // glob.block_sz + 1)
                        for i in glob.hit_Bl:
                            if i == shot_coordinates:
                                f = 1

                        for i in glob.dotted:
                            if i == shot_coordinates:
                                f = 1
                    if f == 0:
                        comp_turn = not logic.hit_or_miss(
                            shot_coordinates, glob.ship_w, comp_turn)

        if comp_turn:
            if glob.around_hit_set:
                comp_turn = logic.shot(glob.around_hit_set)
            else:
                comp_turn = logic.shot(glob.ava_to_fire_set)

        Drawer.dotted(glob.dotted)
        Drawer.hit_blocks(glob.hit_Bl)
        Drawer.ship(glob.destroyed_ships)
        if not glob.computer.ships_set:
            messages.show_mess(
                "YOU WIN!", (0, 0, glob.size[0], glob.size[1]), glob.gameover_f)
        if not glob.human.ships_set:
            messages.show_mess(
                "YOU LOSE!", (0, 0, glob.size[0], glob.size[1]), glob.gameover_f)
            Drawer.ship(glob.computer.ships)
        pygame.display.update()


main()
pygame.quit()
