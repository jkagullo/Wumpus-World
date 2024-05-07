import pygame
import sys
import random
from collections import deque

COLS, ROWS = 4, 4

wumpus_pos = None


# Game Loop
def game_screen():
    size = (700, 700)
    screen = pygame.display.set_mode(size)

    # Determine the size of each cell
    cell_width = size[0] // COLS
    cell_height = size[1] // ROWS

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Load images for game elements
    agent_images = {
        "up": pygame.image.load("assets/agent/agent_up.png"),
        "down": pygame.image.load("assets/agent/agent_down.png"),
        "left": pygame.image.load("assets/agent/agent_left.png"),
        "right": pygame.image.load("assets/agent/agent_right.png")
    }
    wumpus_image = pygame.image.load("assets/wumpus.png")
    stench_image = pygame.image.load("assets/stench.png")
    pit_image = pygame.image.load("assets/pit.png")
    breeze_image = pygame.image.load("assets/breeze.png")
    gold_image = pygame.image.load("assets/gold.png")
    arrow_image = pygame.image.load("assets/arrow.png")

    # Initialize agent position and other game element positions
    agent_pos = (0, 0)
    stench_pos = get_wumpus()
    breeze_pos = get_pit()
    gold_pos = get_gold()
    arrow_pos = get_arrow()

    running = True
    # Inside the game_screen() function
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the grid and game elements
        for i in range(COLS):
            for j in range(ROWS):
                rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Draw grid lines

                # Draw agent
                if (i, j) == agent_pos:
                    agent_rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                    # Update agent image based on its direction
                    agent_image = agent_images["down"]  # Placeholder, update based on actual direction
                    screen.blit(agent_image, agent_rect)

                if i == wumpus_pos[0] and j == wumpus_pos[1]:
                    wumpus_rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                    screen.blit(wumpus_image, wumpus_rect)

                for pos in stench_pos:
                    if i == pos[0] and j == pos[1]:
                        stench_image_rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                        screen.blit(stench_image, stench_image_rect)

                if i == pit_pos[0] and j == pit_pos[1]:
                    pit_rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                    screen.blit(pit_image, pit_rect)

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

        pygame.display.flip()
    pygame.quit()


#FUNCTIONS
def get_wumpus():
    global wumpus_pos

    while True:
        wumpus_pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if wumpus_pos not in [(0,0),(0,1),(1,0),(1,1)]:
            break

    row,col = wumpus_pos
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

    button_image = pygame.image.load("assets/startbutton.png")
    button_rect = button_image.get_rect()
    button_rect.center = (size[0] // 2, size[1] // 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_screen()
                    running = False

        screen.blit(background_image, (0, 0))
        screen.blit(button_image, button_rect.topleft)

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    start_screen()
