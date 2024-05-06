import pygame
import sys

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

            self.screen.update()
            self.clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    screen = Screen(700, 700)
    game = Game(screen)
    game.start_screen()