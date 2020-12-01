import curses
import random
from time import sleep


class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = self.render(self.height, self.width)
        self.apple_coordinates = (-1, -1)

    @staticmethod
    def render(height, width):
        grid = [[' ' for cols in range(width)] for rows in range(height)]
        for rows in range(height):
            grid[rows].insert(0, '|')
            grid[rows].append('|')
        grid.insert(0, list('-' * width))
        grid.append(list('-' * width))
        grid[0].insert(0, '+')
        grid[0].append('+')
        grid[-1].insert(0, '+')
        grid[-1].append('+')
        return grid

    def place_apple(self):
        random.seed()
        y_coord = int(((random.random() * 50) % 30) + 1)
        x_coord = int(((random.random() * 50) % 30) + 1)
        self.apple_coordinates = (y_coord, x_coord)

    def display_board(self, screen, score):
        if self.apple_coordinates != (-1, -1):
            self.grid[self.apple_coordinates[0]][self.apple_coordinates[1]] = '#'
        row_counter = 3
        screen.move(3, 0)
        for row in self.grid:
            for col in row:
                if col == '#':
                    screen.addstr(col, curses.color_pair(2))
                elif col == 'O' or col == 'X':
                    screen.addstr(col, curses.color_pair(3))
                else:
                    screen.addstr(col)
                screen.addstr(' ')
            row_counter += 1
            screen.move(row_counter, 0)
        screen.addstr(self.height + 6, len('Current move:            Current score: '), str(score))


class Snake:
    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)

    def __init__(self):
        self.pos = [(3, 1), (3, 2), (3, 3), (3, 4)]
        self.dir = self.right

    def move(self, new_direction, apple_coordinates):
        self.dir = new_direction
        head = self.get_new_head(self.dir)
        apple_ingestion = self.is_apple_ingested(apple_coordinates, head)
        if not apple_ingestion:
            self.pos = self.pos[1:] + [head]
            return False
        else:
            self.pos = self.pos + [head]
            return True

    @staticmethod
    def is_apple_ingested(apple_coordinates, head):
        return True if head == apple_coordinates else False

    def get_new_head(self, new_direction):
        head = (self.pos[-1][0] + new_direction[0], self.pos[-1][1] + new_direction[1])
        return head

    def is_over(self):
        for segment in self.pos:
            if segment[0] == 0 or segment[0] == 36 or segment[1] == 0 or segment[1] == 36:
                return True
        pos = list(set(self.pos))
        return True if len(pos) != len(self.pos) else False

    def display_snake(self, board, screen, score):
        # print(self.pos)
        height = board.height
        width = board.width
        for row in range(1, height + 1, 1):
            for col in range(1, width + 1, 1):
                board.grid[row][col] = ' '
        for segment in self.pos:
            board.grid[segment[0]][segment[1]] = 'O'
        head = self.pos[-1]
        board.grid[head[0]][head[1]] = 'X'
        board.display_board(screen, score)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.board = Board(35, 35)
        self.snake = Snake()
        self.display()

    def player_move(self, player_input, apple_coordinates):
        direction = self.snake.dir
        if player_input == ord('w'):
            direction = self.snake.up
        elif player_input == ord('s'):
            direction = self.snake.down
        elif player_input == ord('a'):
            direction = self.snake.left
        elif player_input == ord('d'):
            direction = self.snake.right
        ingestion_status = self.snake.move(direction, apple_coordinates)
        if ingestion_status:
            self.score += 1
            self.board.place_apple()

    def display(self):
        self.snake.display_snake(self.board, self.screen, self.score)


def curses_main(screen):
    game = Game(screen)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    screen.addstr(0, 0, 'Press w, a, s or d to move or press q to quit...', curses.color_pair(1))
    screen.addstr(game.board.height + 6, 0, 'Current move: \t\t Current score: ')
    curses.curs_set(0)
    screen.nodelay(True)
    counter = 0
    while True:
        if 5 > counter >= 0:
            counter += 1
        elif not counter < 0:
            counter = -1
            game.board.place_apple()
        player_input = screen.getch()
        if player_input != -1:
            screen.addstr(game.board.height + 6, len('Current move: '), chr(player_input))
            screen.getch()
        if player_input == ord('q'):
            break
        game.player_move(player_input, game.board.apple_coordinates)
        game.display()
        if game.snake.is_over():
            screen.nodelay(False)
            screen.addstr(game.board.height + 6, 0, 'GAME OVER!!\n', curses.color_pair(1))
            screen.addstr('Press any key to exit...', curses.color_pair(1))
            screen.getch()
            break
        sleep(0.1)


def main():
    return curses.wrapper(curses_main)


if __name__ == '__main__':
    exit(main())
