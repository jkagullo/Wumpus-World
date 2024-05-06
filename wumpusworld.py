import pygame
import sys
import random

COLS, ROWS = 4, 4

wumpus_pos = None

def game_screen():
    size = (700, 700)
    screen = pygame.display.set_mode(size)

    # wumpus
    image = pygame.image.load("assets/wumpus.png")  # Replace "image_name.jpg" with the filename of your image
    image_rect = image.get_rect()

    #stench
    stench_image = pygame.image.load("assets/stench.png")
    stench_image_rect = image.get_rect()

    #pit
    pit_image = pygame.image.load("assets/pit.png")
    pit_image_rect = image.get_rect()

    #breeze
    breeze_image = pygame.image.load("assets/breeze.png")
    breeze_image_rect = image.get_rect()

    gold_image = pygame.image.load("assets/gold.png")
    gold_image_rect = image.get_rect()

    arrow_image = pygame.image.load("assets/arrow.png")
    arrow_image_rect = image.get_rect()

    # Determine the size of each cell
    cell_width = size[0] // COLS
    cell_height = size[1] // ROWS

    # Create a font object
    font = pygame.font.Font(None, 36)

    stench_pos = get_wumpus()
    breeze_pos = get_pit()
    gold_pos = get_gold()
    arrow_pos = get_arrow()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the grid
        for i in range(COLS):
            for j in range(ROWS):
                rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Draw a white rectangle with a width of 1

                # Create a text surface
                text = font.render(f'({i},{j})', True, (255, 255, 255))  # Change text color to white
                text_rect = text.get_rect(center=(i * cell_width + cell_width // 2, j * cell_height + cell_height // 2))

                if i == wumpus_pos[0] and j == wumpus_pos[1]:
                    wumpus_rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                    screen.blit(image, wumpus_rect)

                for pos in stench_pos:
                    if i == pos[0] and j == pos[1]:
                        stench_image_rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                        screen.blit(stench_image, stench_image_rect)

                if i == pit_pos[0] and j == pit_pos[1]:
                    pit_rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                    screen.blit(pit_image,pit_rect)

                for pos in breeze_pos:
                    if i == pos[0] and j == pos[1]:
                        breeze_image_rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                        screen.blit(breeze_image, breeze_image_rect)

                if i == gold_pos[0] and j == gold_pos[1]:
                    gold_rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                    screen.blit(gold_image, gold_rect)

                if i == arrow_pos[0] and j == arrow_pos[1]:
                    arrow_rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                    screen.blit(arrow_image, arrow_rect)

                # Draw the text surface on the screen
                screen.blit(text, text_rect)

        pygame.display.flip()
    pygame.quit()

def get_wumpus():
    global wumpus_pos

    while True:
        wumpus_pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if wumpus_pos not in [(0,0),(0,1),(1,0),(1,1)]:
            break

    row, col = wumpus_pos
    stench_pos = []

    if row > 0:
        stench_pos.append((row - 1, col))
    if row < ROWS - 1:
        stench_pos.append((row + 1, col))
    if col > 0:
        stench_pos.append((row, col - 1))
    if col < COLS-1:
        stench_pos.append((row, col + 1))

    print(f"wumpus pos: {wumpus_pos}")
    print(f"stench pos: {stench_pos}")

    return stench_pos

def get_pit():
    global pit_pos

    while True:
        pit_pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pit_pos not in [(0,0),(0,1),(1,0),(1,1)] and pit_pos != wumpus_pos:
            break

    row,col = pit_pos
    breeze_pos = []

    if row > 0:
        breeze_pos.append((row - 1, col))
    if row < ROWS - 1:
        breeze_pos.append((row + 1, col))
    if col > 0:
        breeze_pos.append((row, col - 1))
    if col < COLS-1:
        breeze_pos.append((row, col + 1))

    print(f"pit pos: {pit_pos}")
    print(f"breeze pos: {breeze_pos}")

    return breeze_pos

def get_gold():
    while True:
        gold_pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if gold_pos not in [(0,0),(0,1),(1,0),(1,1)]:
            break

    row, col = gold_pos
    print(f"gold pos: {gold_pos}")
    return gold_pos

def get_arrow():
    while True:
        arrow_pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if arrow_pos not in [(0, 0), (0, 1), (1, 0), (1, 1)] and pit_pos != arrow_pos and wumpus_pos != arrow_pos:
            break

    row,col = arrow_pos
    print(f"arrow_pos: {arrow_pos}")
    return arrow_pos


def start_screen():
    pygame.init()

    size = (800, 600)
    screen = pygame.display.set_mode(size)

    background_image = pygame.image.load("assets/splash.png")

    font = pygame.font.Font(None, 36)

    button_image = pygame.image.load("assets/startbutton.png")
    button_image = pygame.transform.scale(button_image, (200, 50))  # Scale the image to fit the button

    button_color = (0, 255, 0)  # Define button_color
    button_width = 200
    button_height = 50
    button_x = (size[0] - button_width) // 2
    button_y = (size[1] - button_height) // 2
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_screen()
                running = False

        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_image, button_rect.topleft)

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    start_screen()
