import pygame
import sys
import random

class GameAssets:
    def __init__(self):
        self.agent_move_up = pygame.image.load('assets/agent/agent_up.png')
        self.agent_move_down = pygame.image.load('assets/agent/agent_down.png')
        self.agent_move_left = pygame.image.load('assets/agent/agent_left.png')
        self.agent_move_right = pygame.image.load('assets/agent/agent_right.png')

        self.wumpus = pygame.image.load('assets/wumpus.png')
        self.stench = pygame.image.load('assets/stench.png')
        self.glitter = pygame.image.load('assets/glitter.png')
        self.gold = pygame.image.load('assets/gold.png')
        self.arrow = pygame.image.load('assets/arrow.png')
        self.breeze = pygame.image.load('assets/breeze.png')
        self.pit = pygame.image.load('assets/pit.png')

class GameElement:
    def __init__(self, name, image, percept):
        self.name = name
        self.image = image
        self.percept = percept
        self.position = None

    def draw(self, screen, cell_size):
        if self.position is not None:
            x, y = self.position
            screen.blit(self.image, (x * cell_size, y * cell_size))

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, window, font):
        pygame.draw.rect(window, (255, 0, 0), self.rect)
        text = font.render(self.text, True, (255, 255, 255))
        window.blit(text, self.rect.move(20, 10))

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(None, 24)

    def fill(self, color):
        self.window.fill(color)

    def update(self):
        pygame.display.flip()

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.button = Button((self.screen.width - 150) // 2, (self.screen.height - 50) // 2, 150, 50, "Start Game")
        self.assets = GameAssets()  # Load the game assets

        self.wumpus = GameElement('wumpus', self.assets.wumpus, self.assets.stench)
        self.pit = GameElement('pit', self.assets.pit, self.assets.breeze)
        self.gold = GameElement('gold', self.assets.gold, self.assets.glitter)

        self.board = GameBoard(4, 4)
        self.board.place_element(self.wumpus)
        self.board.place_element(self.pit)
        self.board.place_element(self.gold)

    def start_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button.rect.collidepoint(event.pos):
                        self.game_screen()

            self.screen.fill((255, 255, 255))
            self.button.draw(self.screen.window, self.screen.font)

            self.screen.update()
            self.clock.tick(60)

    def print_element_positions(self):
        for i in range(self.board.width):
            for j in range(self.board.height):
                element = self.board.grid[i][j]
                if element is not None:
                    print(f'{element.name}: cell ({i},{j})')

    def game_screen(self):
        grid = [[0 for _ in range(4)] for _ in range(4)]  # This represents a 4x4 grid using a 2D list
        cell_size = self.screen.width // 4  # Make the cell size a quarter of the window size

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))

            # Draw the 4x4 grid
            for i in range(4):
                for j in range(4):
                    pygame.draw.rect(self.screen.window, (255, 255, 255),
                                     pygame.Rect(i * cell_size, j * cell_size, cell_size - 1, cell_size - 1), 1)

                    # Create a text surface and draw it on the screen
                    text = self.screen.font.render(f'({i},{j})', True, (255, 255, 255))
                    self.screen.window.blit(text, (i * cell_size + cell_size // 2, j * cell_size + cell_size // 2))

                    # Draw the game element at this cell if there is one
                    element = self.board.grid[i][j]
                    if element is not None:
                        element.draw(self.screen.window, cell_size)

            self.print_element_positions()

            self.screen.update()
            self.clock.tick(60)

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(height)] for _ in range(width)]

    def place_element(self, element):
        # Choose a random position for the element
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        element.position = (x, y)

        # Place the element on the grid
        self.grid[x][y] = element

        # Place the percept on the adjacent cells
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                percept_element = GameElement('percept', element.percept, None)
                self.grid[nx][ny] = percept_element


if __name__ == "__main__":
    pygame.init()
    screen = Screen(700, 700)
    game = Game(screen)
    game.start_screen()