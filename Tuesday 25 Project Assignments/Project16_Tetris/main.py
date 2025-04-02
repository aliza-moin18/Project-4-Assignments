import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width, s_height = 800, 700
play_width, play_height = 300, 600  # grid size 10x20
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS
S = [[".....", ".....", "..00.", ".00..", "....."], [".....", "..0..", "..00.", "...0.", "....."]]
Z = [[".....", ".....", ".00..", "..00.", "....."], [".....", "..0..", ".00..", ".0...", "....."]]
I = [["..0..", "..0..", "..0..", "..0..", "....."], [".....", "0000.", ".....", ".....", "....."]]
O = [[".....", ".....", ".00..", ".00..", "....."]]
J = [[".....", ".0...", ".000.", ".....", "....."], [".....", "..00.", "..0..", "..0..", "....."]]
L = [[".....", "...0.", ".000.", ".....", "....."], [".....", "..0..", "..0..", "..00.", "....."]]
T = [[".....", "..0..", ".000.", ".....", "....."]]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece:
    rows, columns = 20, 10
    def __init__(self, x, y, shape):
        self.x, self.y = x, y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        for j, column in enumerate(line):
            if column == '0':
                positions.append((shape.x + j - 2, shape.y + i - 4))
    return positions

def valid_space(shape, grid):
    accepted_positions = [(x, y) for y in range(20) for x in range(10) if grid[y][x] == (0, 0, 0)]
    return all(pos in accepted_positions or pos[1] < 0 for pos in convert_shape_format(shape))

def check_lost(locked_positions):
    return any(y < 1 for _, y in locked_positions)

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))

def draw_window(surface, grid, locked_positions):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2, 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size))

    draw_grid(surface)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

def draw_grid(surface):
    for i in range(20):
        pygame.draw.line(surface, (128, 128, 128), (top_left_x, top_left_y + i * block_size), (top_left_x + play_width, top_left_y + i * block_size))  
        for j in range(10):
            pygame.draw.line(surface, (128, 128, 128), (top_left_x + j * block_size, top_left_y), (top_left_x + j * block_size, top_left_y + play_height))  

def clear_rows(grid, locked_positions):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        if (0, 0, 0) not in grid[i]:
            inc += 1
            for j in range(len(grid[i])):
                del locked_positions[(j, i)]
    if inc > 0:
        for key in sorted(list(locked_positions), key=lambda x: x[1], reverse=True):
            x, y = key
            if y < i:
                locked_positions[(x, y + inc)] = locked_positions.pop((x, y))
    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))
    sx, sy = top_left_x + play_width + 50, top_left_y + play_height / 2 - 100
    for i, line in enumerate(shape.shape[shape.rotation % len(shape.shape)]):
        for j, column in enumerate(line):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)
    surface.blit(label, (sx + 10, sy - 30))

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    current_piece, next_piece = get_shape(), get_shape()
    change_piece, run = False, True
    clock, fall_time = pygame.time.Clock(), 0

    while run:
        fall_speed = 0.27
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)
        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                locked_positions[(pos[0], pos[1])] = current_piece.color
            current_piece, next_piece = next_piece, get_shape()
            change_piece = False
            clear_rows(grid, locked_positions)

        draw_window(win, grid, locked_positions)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)

def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press any key to begin.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

pygame.display.set_caption('Tetris')
win = pygame.display.set_mode((s_width, s_height))

main_menu()
