import pygame
import sys
import random
import time

class Agent:
    def __init__(self, cell_size):
        self.x = 0
        self.y = 0
        self.cell_size = cell_size
        self.directions = ['up', 'down', 'left', 'right']
        self.direction = random.choice(self.directions)
        self.images = {
            'up': pygame.image.load('assets/agent/agent_up.png'),
            'down': pygame.image.load('assets/agent/agent_down.png'),
            'left': pygame.image.load('assets/agent/agent_left.png'),
            'right': pygame.image.load('assets/agent/agent_right.png'),
        }

    def update(self):
        self.direction = random.choice(self.directions)
        if self.direction == 'up':
            self.y -= 1
        elif self.direction == 'down':
            self.y += 1
        elif self.direction == 'left':
            self.x -= 1
        elif self.direction == 'right':
            self.x += 1

        # Ensure the agent stays within the grid
        self.x = max(0, min(self.x, 3))
        self.y = max(0, min(self.y, 3))

    def draw(self, screen):
        image = self.images[self.direction]
        screen.blit(image, (self.x * self.cell_size, self.y * self.cell_size))
def start_screen():
    pygame.init()

    # Set the dimensions of the window
    size = (800, 600)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Wumpus World")

    #load background image
    background = pygame.image.load('assets/splash.png')

    button_width = 150
    button_height = 50

    # Define the button's position and size
    button = pygame.Rect((size[0] - button_width) // 2, (size[1] - button_height) // 2 + 100, button_width, button_height)

    # Load the button image
    button_image = pygame.image.load('assets/startbutton.png')
    button_image = pygame.transform.scale(button_image, (button_width, button_height))  # Scale the image to fit the button

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                if button.collidepoint(mouse_pos):  # checks if mouse position is over the button
                    return game_screen()  # leads to game screen

        screen.blit(background, (0,0))  # fill the screen with black
        screen.blit(button_image, button.topleft)  # draw the button image at the position of the button

        pygame.display.flip()  # update the display

def game_screen():
    pygame.init()

    # Set the dimensions of the window
    size = (700, 700)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Game is Running")

    background = pygame.image.load('assets/gamescreenbg.png')

    # Define the size of the grid cells
    cell_size = size[0] // 4  # Make the cell size a quarter of the screen width and height

    font = pygame.font.Font(None, 24)  # Define a font object

    # Create the agent
    agent = Agent(cell_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0,0))  # fill the screen with black

        # Draw the 4x4 grid
        for i in range(4):
            for j in range(4):
                x = i * cell_size
                y = j * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)
                color = (255, 0, 0) if (i, j) == (0, 0) else (255, 255, 255)  # Change color to red if box is at (0,0)
                pygame.draw.rect(screen, color, rect, 1)

                # Create a text surface and draw it on the screen
                text = font.render(f'({i},{j})', True, (255, 255, 255))
                screen.blit(text, (x + cell_size // 2, y + cell_size // 2))

        # Update and draw the agent
        agent.update()
        agent.draw(screen)

        pygame.display.flip()  # update the display

        # Delay for 1 second
        time.sleep(1)

    pygame.quit()

if __name__ == "__main__":
    start_screen()