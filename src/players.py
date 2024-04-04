from abc import ABC, abstractmethod
import random
from typing import Tuple, List, Set
import shooting_process as shooting
import global_variables as my_space
from grid_class import Grid
from drawer import ShipDrawer


class Player(ABC):
    def __init__(self, name: str, offset: int):
        self.name = name
        self.offset = offset
        self.create_board()
        self.drawer = ShipDrawer()

    def create_board(self):
        """Начинает процесс рисования доски"""
        Grid(self.name, self.offset)

    @abstractmethod
    def make_move(self, opponent_board):
        pass

    @abstractmethod
    def update_dotted_and_hit(self, shot_coordinates: Tuple[int, int],
                              diagonal_only: bool) -> None:
        pass

    @abstractmethod
    def update_around_comp_hit(self, shot_coordinates: tuple) -> None:
        pass

    def process_destroyed_ship(self, pos: int, other_player, diagonal_only: bool) -> None:
        """
        Обрабатывает процесс уничтожения корабля
        """
        ship = sorted(other_player.drawer.ships[pos])
        for ind in range(-1, 1):
            self.update_dotted_and_hit(ship[ind], diagonal_only)


class ComputerPlayer(Player):
    def __init__(self, name: str, offset: int):
        super().__init__(name, offset)
        self.need_to_fire = set()
        self.last_hit = None
        self.available_to_fire_set = set(
            (a + offset, b) for a in range(1, my_space.GRID_SIZE) for b in
            range(1, my_space.GRID_SIZE))

    def make_move(self, opponent_board):
        pass

    def update_dotted_and_hit(self, shot_coordinates: Tuple[int, int],
                              diagonal_only: bool) -> None:
        """Эта процедура добавляет точки вокруг клетки, в которую был произведен выстрел"""
        fire_x_coordinate, fire_y_coordinate = shot_coordinates
        min_x, max_x = self.offset, self.offset + my_space.GRID_LIMIT
        fire_x_coordinate += self.offset
        self.available_to_fire_set.remove(shot_coordinates)
        for add_x_coordinate in range(-1, 2):
            for add_y_coordinate in range(-1, 2):
                if (not diagonal_only and min_x < fire_x_coordinate + add_x_coordinate < max_x and
                        0 < fire_y_coordinate + add_y_coordinate < my_space.GRID_LIMIT):
                    self.drawer.draw_dot((fire_x_coordinate + add_x_coordinate,
                                          fire_y_coordinate + add_y_coordinate))
                    self.need_to_fire.add((shot_coordinates[0] + add_x_coordinate,
                                           fire_y_coordinate + add_y_coordinate))

    def shoot(self, other_player: Player, game_over: bool) -> tuple[bool, bool]:
        """Стреляет от имени компьютера"""
        is_hit = False
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         return True, is_hit
        if not game_over:
            if self.need_to_fire:
                is_hit = self.__random_shoot(self.need_to_fire, other_player)
            else:
                is_hit = self.__random_shoot(self.available_to_fire_set, other_player)
        return game_over, is_hit

    def __random_shoot(self, set_to_shot: set, other_player: Player) -> bool:
        """
        Случайным образом выбирает блок из доступных для стрельбы из набора и возвращает hit_or_miss
        """
        pygame.time.delay(my_space.MAX_DELAY_FOR_COMPUTER_SHOT)
        computer_fired = random.choice(tuple(set_to_shot))
        self.available_to_fire_set.discard(computer_fired)
        self.drawer.draw_dot(computer_fired)
        return self.__check_is_successful_hit(computer_fired, other_player)

    def __check_is_successful_hit(self, shot_coordinates: tuple[int, int],
                                  other_player: Player) -> bool:
        """Проверяет попадание в корабль противника и выполняет соответствующие действия.
        Возвращает True при попадании, иначе False."""
        for ship in other_player.drawer.ships:
            if shot_coordinates in ship:
                self.update_dotted_and_hit(shot_coordinates)
                position = other_player.drawer.ships.index(ship)
                # if len(ship) == 1:
                #     self.update_dotted_and_hit(shot_coordinates, True)
                ship.remove(shot_coordinates)
                other_player.drawer.ships_set.discard(shot_coordinates)
                self.update_around_comp_hit(shot_coordinates, True)
                self.last_hit = shot_coordinates
                if not ship:
                    other_player.process_destroyed_ship(position, other_player, False)
                    self.last_hit = None
                    self.need_to_fire.clear()
                return True

        self.drawer.draw_dot((shot_coordinates[0], shot_coordinates[1]))
        # my_space.dotted_to_shot.add(shot_coordinates)
        self.update_around_comp_hit(shot_coordinates, False)
        return False

    def update_around_comp_hit(self, shot_coordinates: tuple) -> None:
        """
        Обновляет набор блоков вокруг последнего поражения компьютера, удаляя блоки,
        по которым компьютер промахнулся, для эффективного поиска кораблей противника.
        """
        if computer_hits:
            shooting.update_around_last_hit(shot_coordinates)
        else:
            shooting.remove_from_around_hit_set(shot_coordinates)

        shooting.remove_used_blocks_from_around_hit_set()
        shooting.update_available_to_fire_set()


class HumanPlayer(Player):
    def __handle_mouse_event(self, event):
        """Обрабатывает события мыши для хода игрока."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_coordinate, y_coordinate = event.pos
            if (my_space.MIN_X <= x_coordinate <= my_space.MAX_X and
                    my_space.MIN_Y <= y_coordinate <= my_space.MAX_Y):
                if ((my_space.LEFT_MARGIN < x_coordinate < my_space.LEFT_MARGIN +
                     my_space.GRID_OFFSET * my_space.BLOCK_SIZE) and
                        (my_space.UP_MARGIN < y_coordinate < my_space.UP_MARGIN +
                         my_space.GRID_OFFSET * my_space.BLOCK_SIZE)):
                    return ((x_coordinate - my_space.LEFT_MARGIN) // my_space.BLOCK_SIZE + 1,
                            (y_coordinate - my_space.UP_MARGIN) // my_space.BLOCK_SIZE + 1)
        return None

    def make_move(self, opponent_board):
        pass

    def update_dotted_and_hit(self, shot_coordinates: Tuple[int, int], computer_turn: bool,
                              diagonal_only: bool = True) -> None:
        """Эта процедура добавляет точки вокруг клетки, в которую был произведен выстрел"""
        fire_x_coordinate, fire_y_coordinate = shot_coordinates
        min_x, max_x = self.offset, self.offset + my_space.GRID_LIMIT
        if computer_turn:
            fire_x_coordinate += self.offset
            my_space.nado_ubrat_for_comp_to_shot.add(shot_coordinates)
        my_space.hit_blocks.add((fire_x_coordinate, fire_y_coordinate))
        for add_x_coordinate in range(-1, 2):
            for add_y_coordinate in range(-1, 2):
                if (not diagonal_only and min_x < fire_x_coordinate + add_x_coordinate < max_x and
                        0 < fire_y_coordinate + add_y_coordinate < my_space.GRID_LIMIT):
                    my_space.dotted.add(
                        (
                            fire_x_coordinate + add_x_coordinate,
                            fire_y_coordinate + add_y_coordinate))
                    if computer_turn:
                        my_space.dotted_to_shot.add((shot_coordinates[0] + add_x_coordinate,
                                                     fire_y_coordinate + add_y_coordinate))
        my_space.dotted -= my_space.hit_blocks

    def shoot(self, game_over: bool, shot_taken: bool) -> tuple[bool, bool]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, shot_taken
            shot_coordinates = self.__handle_mouse_event(event)
            if shot_coordinates is not None:
                shot_taken = False
                for hit_block in my_space.hit_blocks:
                    if hit_block == shot_coordinates:
                        shot_taken = True
                for dot in my_space.dotted:
                    if dot == shot_coordinates:
                        shot_taken = True
                if not shot_taken:
                    computer_turn = not shooting.check_is_successful_hit(
                        shot_coordinates, my_space.COMPUTER_SHIPS)
        return game_over, computer_turn, shot_taken

    def __check_is_successful_hit(self, shot_coordinates: tuple[int, int],
                                  other_player: Player) -> bool:
        """Проверяет попадание в корабль противника и выполняет соответствующие действия.
        Возвращает True при попадании, иначе False."""
        for ship in other_player.drawer.ships:
            if shot_coordinates in ship:
                self.update_dotted_and_hit(shot_coordinates)
                position = other_player.drawer.ships.index(ship)
                # if len(ship) == 1:
                #     self.update_dotted_and_hit(shot_coordinates, True)
                ship.remove(shot_coordinates)
                if computer_turn:
                    my_space.last_hits.append(shot_coordinates)
                    my_space.HUMAN.ships_set.discard(shot_coordinates)
                    update_around_comp_hit(shot_coordinates)
                else:
                    my_space.COMPUTER.ships_set.discard(shot_coordinates)
                if not ship:
                    other_player.drawer.process_destroyed_ship(position, other_player, False)
                    if computer_turn:
                        my_space.last_hits.clear()
                        my_space.izmeni_shahrom.clear()
                    else:
                        my_space.destroyed_ships.append(
                            my_space.COMPUTER.ships[position])
                return True
        if not computer_turn:
            my_space.dotted.add(shot_coordinates)
        else:
            my_space.dotted.add((shot_coordinates[0] + 15, shot_coordinates[1]))
            my_space.dotted_to_shot.add(shot_coordinates)
        if computer_turn:
            update_around_comp_hit(shot_coordinates, False)
        return False

    def update_around_comp_hit(self, shot_coordinates: tuple, computer_hits: bool = True) -> None:
        """
        Обновляет набор блоков вокруг последнего поражения компьютера, удаляя блоки,
        по которым компьютер промахнулся, для эффективного поиска кораблей противника.
        """
        if computer_hits:
            shooting.update_around_last_hit(shot_coordinates)
        else:
            shooting.remove_from_around_hit_set(shot_coordinates)

        shooting.remove_used_blocks_from_around_hit_set()
        shooting.update_available_to_fire_set()
