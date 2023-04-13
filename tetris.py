import pygame
import random

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 900
s_height = 745
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
global score
score = 0 
global level
level = 1
global r,g,b
r,g,b = (157, 240, 245)


# global Highest
# Highest = 0

# SHAPE FORMATS

S = [['....',
      '....',
      '..00',
      '.00.',],
     ['....',
      '..0.',
      '..00',
      '...0']]

Z = [['....',
      '....',
      '.00.',
      '..00'],
     ['....',
      '..0.',
      '.00.',
      '.0..']]

I = [['..0.',
      '..0.',
      '..0.',
      '..0.'],
     ['....',
      '0000',
      '....',
      '....']]

O = [['....',
      '....',
      '.00.',
      '.00.']]

J = [['....',
      '.0..',
      '.000',
      '....'],
     ['....',
      '..00',
      '..0.',
      '..0.'],
     ['....',
      '....',
      '.000',
      '...0'],
     ['....',
      '..0.',
      '..0.',
      '.00.']]

L = [['....',
      '...0',
      '.000',
      '....'],
     ['....',
      '..0.',
      '..0.',
      '..00'],
     ['....',
      '....',
      '.000',
      '.0..'],
     ['....',
      '.00.',
      '..0.',
      '..0.']]

T = [['....',
      '..0.',
      '.000',
      '....'],
     ['....',
      '..0.',
      '..00',
      '..0.'],
     ['....',
      '....',
      '.000',
      '..0.'],
     ['....',
      '..0.',
      '.00.',
      '..0.']
     ]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(1, 1, 240), (1, 240, 240), (0, 240, 0),
                (239, 160, 0), (160, 0, 241),(240, 1, 0), (240, 240, 1)]
# index 0 - 6 represent shape


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3


def create_grid(locked_positions={}):
    grid = [[(r,g,b) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shapes):
    positions = []
    format = shapes.shape[shapes.rotation % len(shapes.shape)]
    #print("format",format)

    for i, line in enumerate(format):
        row = list(line)
       #print("row",row)
        for j, column in enumerate(row):
            #print("column=",column)
            if column == '0':
                positions.append((shapes.x + j, shapes.y + i))
                
    #print(positions)
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(
        10) if grid[i][j] == (r,g,b)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
    #print(accepted_positions)
    #print(formatted)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    global shapes, shape_colors
    random.seed()
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2),
                 top_left_y + play_height/2 - label.get_height()/2))

    if text == "Game Over":
        score_label = pygame.font.SysFont('comicsans', 30).render(
            f"Final Score: {score}", True, (255, 255, 255))
        surface.blit(score_label, (top_left_x + play_width/2 - (score_label.get_width() / 2),
                               top_left_y + play_height/2 - label.get_height()/2 + 40))
        # Highest_Score = pygame.font.SysFont('comicsans', 30).render(f"Highest: {Highest}", True, (255, 255, 255))
        # surface.blit(Highest_Score, (top_left_x + play_width/2 - (Highest_Score.get_width() / 2),
                            #    top_left_y + play_height/2 - label.get_height()/2 + 80))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*30),
                         (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + play_height))  # vertical lines



def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one

    global score
    global level
    global Highest
    inc = 0
    
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (r,g,b) not in row:
            inc += 1
            n =column_music()
            # add positions to remove from locked
            ind = i
            score += 10 * level
            level = score // 30 + 1
            
            if score > Highest:
                Highest = score
                with open('highest_score.txt', 'w') as f:
                    f.write(str(Highest))

            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        column_music()
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    # column_music()

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface):
    #surface.fill((47, 167, 254))
    bg_img = pygame.image.load('back.jpg')
    bg_img = pygame.transform.scale(bg_img,(s_width,s_height))
        
    surface.blit(bg_img,(0,0))
    
    
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width /
                 2 - (label.get_width() / 2), 30))
                 
                 
                 
    sx = 0
    sy = top_left_y + play_height/2 - 100           
     #credits
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('CREDITS:-', 1, (255, 255, 255))

    surface.blit(label, (sx + 30, sy - 120))
     
     
     
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('AYUSH KUMAR', 1, (255, 255, 255))

    surface.blit(label, (sx + 43, sy - 60))
                 
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('ANKUSH KUMAR', 1, (255, 255, 255))

    surface.blit(label, (sx + 43, sy - 30))
                 
    font = pygame.font.SysFont('comicsans',30)
    label = font.render('NILADRI SADHU', 1, (255, 255, 255))

    surface.blit(label, (sx + 43, sy ))
                 
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('ROHIT KUMAR', 1, (255, 255, 255))

    surface.blit(label, (sx + 43, sy+30 ))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    # draw grid and border
    draw_grid(surface, 20, 10)
    score_label = pygame.font.SysFont('comicsans', 30).render(
        f"Score: {score}", True, (255, 255, 255))
    surface.blit(score_label, (top_left_x + play_width + 50, top_left_y + 20))

    level_label = pygame.font.SysFont('comicsans', 30).render(
        f"Level: {level}", True, (255, 255, 255))
    surface.blit(level_label, (top_left_x + play_width + 50, top_left_y + 50))

    Highest_Score = pygame.font.SysFont('comicsans', 30).render(
        f"Highest: {Highest}", True, (255, 255, 255))
    surface.blit(Highest_Score, (top_left_x +
                 play_width + 50, top_left_y + 80))

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x,
                     top_left_y, play_width, play_height), 5)
    # pygame.display.update()

def music(stop=0):
    if stop == 0:
        pygame.mixer.init()
        music_file = "etrisswing.flac"
        music_sound = pygame.mixer.Sound(music_file)
        music_sound.play()
        play = 1
    else:
        pygame.time.wait(int(1))
        pygame.mixer.quit()
        
def column_music():
    pygame.mixer.init()
    music_file = "column.mp3"
    music_sound = pygame.mixer.Sound(music_file)
    music_sound.play()
    return 1

def main():
    global grid
    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    play = 0
    

    while run:
        fall_speed = 1/level
        
        if play == 0 :
            music()
            play = 1
        

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 5
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
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
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + \
                        1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - \
                            1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                   # print(convert_shape_format(current_piece)) # todo fix

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            clear_rows(grid, locked_positions)

        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            music(1)
            run = False

    draw_text_middle("Game over", 100, (255, 255, 255), win)
    
    pygame.mixer.init()
    
    music_file = "game-over.flac"
    music_sound = pygame.mixer.Sound(music_file)
    music_sound.play()
    pygame.time.wait(int(music_sound.get_length() * 1000))
    pygame.mixer.quit()
    
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    # Load the highest score from a file
    with open('highest_score.txt', 'r') as f:
        try:
            global Highest
            Highest = int(f.read())
            # Highest=80
            print(Highest)
        except:
            Highest = 0
    run = True
    while run:
        # win.fill((100, 50, 55))
        bg_img = pygame.image.load('game_start.jpg')
        bg_img = pygame.transform.scale(bg_img,(s_width,s_height))
        
        win.blit(bg_img,(0,0))
        
        draw_text_middle('Start the game by pressing any key', 40, (0, 0, 0), win)
        pygame.display.update()
        global level
        level = 1
        global score
        score = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game