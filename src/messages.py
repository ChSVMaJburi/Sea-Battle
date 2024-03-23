import global_variable as glob
import pygame


def show_mess(mess: str, rectangle: tuple, w_f=glob.font):
    """
    Выводит сообщение на экран в центре заданного прямоугольника.
    Аргументы:
        mess (str): Сообщение для печати
        r (tuple): прямоугольник в формате
        w_f (объект шрифта pygame): Какой шрифт использовать для печати сообщения. По умолчанию используется шрифт.
    """
    mess_w, mess_h = w_f.size(mess)
    mess_r = pygame.Rect(rectangle)
    x = mess_r.centerx - mess_w / 2
    y = mess_r.centery - mess_h / 2
    backgr_r = pygame.Rect(x - glob.block_sz / 2,
                           y, mess_w + glob.block_sz, mess_h)
    mess_blit = w_f.render(mess, True, glob.RED)
    glob.screen.fill(glob.BLUE, backgr_r)
    glob.screen.blit(mess_blit, (x, y))
