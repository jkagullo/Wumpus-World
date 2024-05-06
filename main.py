import pygame
import sys
import random
import time

# TO DO: 1. rules of inference. 2. fog. 3. darken background
class Agent:
    def __init__(self, cell_size):
        self.x = 0
        self.y = 0
        self.prev_x = 0
        self.prev_y = 0
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
        self.prev_x = self.x
        self.prev_y = self.y
        if self.direction == 'up' and self.y > 0:
            self.y -= 1
        elif self.direction == 'down' and self.y < 3:
            self.y += 1
        elif self.direction == 'left' and self.x > 0:
            self.x -= 1
        elif self.direction == 'right' and self.x < 3:
            self.x += 1
        else:
            # If the agent is at a boundary and can't move in the current direction,
            # choose a new direction
            self.direction = random.choice(self.directions)
        self.print_position()

    def draw(self, screen):
        image = self.images[self.direction]
        screen.blit(image, (self.x * self.cell_size, self.y * self.cell_size))

    def print_position(self):
        print(f'Agent moved from ({self.prev_x},{self.prev_y}) to ({self.x},{self.y})')

class Screen:
    def __init__(self, size):
        self.size = size
        self.screen = pygame.display.set_mode(size)
        self.cell_size = size[0] // 4
        self.font = pygame.font.Font(None, 24)
        self.background = pygame.image.load('assets/gamescreenbg.png')

    def draw_grid(self):
        for i in range(4):
            for j in range(4):
                x = i * self.cell_size
                y = j * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                color = (255, 0, 0) if (i, j) == (0, 0) else (255, 255, 255)
                pygame.draw.rect(self.screen, color, rect, 1)
                text = self.font.render(f'({i},{j})', True, (255, 255, 255))
                self.screen.blit(text, (x + self.cell_size // 2, y + self.cell_size // 2))

    def update(self, agent):
        self.screen.blit(self.background, (0,0))
        self.draw_grid()
        agent.draw(self.screen)
        pygame.display.flip()

class GameElement:
    def __init__(self, cell_size, image_path, name):
        self.cell_size = cell_size
        self.image = pygame.image.load(image_path)
        self.name = name
        self.reset()

    def draw(self, screen):
        screen.blit(self.image, (self.x * self.cell_size, self.y * self.cell_size))

    def reset(self):
        self.x = random.randint(0, 3)
        self.y = random.randint(0, 3)

class GameScreen:
    def __init__(self):
        pygame.init()

        # Set the dimensions of the window
        self.size = (700, 700)
        self.screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption("Game is Running")

        self.background = pygame.image.load('assets/gamescreenbg.png')

        # Define the size of the grid cells
        self.cell_size = self.size[0] // 4  # Make the cell size a quarter of the screen width and height

        self.font = pygame.font.Font(None, 24)  # Define a font object

        # Create the agent
        self.agent = Agent(self.cell_size)

        # Create the game elements
        self.game_elements = [
            GameElement(self.cell_size, 'assets/wumpus.png', 'Wumpus'),
            GameElement(self.cell_size, 'assets/gold.png', 'Gold'),
            GameElement(self.cell_size, 'assets/arrow.png', 'Arrow'),
            GameElement(self.cell_size, 'assets/stench.png', 'Stench'),
            GameElement(self.cell_size, 'assets/breeze.png', 'Breeze'),
            GameElement(self.cell_size, 'assets/pit.png', 'Pit'),
        ]

        # Define play again and exit game buttons
        button_width = 150
        button_height = 50
        self.play_again_button = pygame.Rect((self.size[0] - button_width) // 2, (self.size[1] - button_height) // 2 + 100, button_width, button_height)
        self.exit_game_button = pygame.Rect((self.size[0] - button_width) // 2, (self.size[1] - button_height) // 2 + 200, button_width, button_height)

    def reset_game(self):
        # Reset the agent's position
        self.agent.x = 0
        self.agent.y = 0

        # Reset the positions of game elements
        for element in self.game_elements:
            element.reset()

    def game_over_popup(self, message):
        print(message)
        return False

    def print_element_coordinates(self):
        for element in self.game_elements:
            print(f'{element.name}: ({element.x}, {element.y})')

    def check_collision(self):
        for element in self.game_elements:
            if (self.agent.x, self.agent.y) == (element.x, element.y):
                if element.name == 'Wumpus':
                    return 'Wumpus'
                elif element.name == 'Gold':
                    return 'Gold'
                elif element.name == 'Pit':
                    return 'Pit'
        return None

    def game_over_popup(self, message):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.play_again_button.collidepoint(mouse_pos):
                        self.reset_game()  # Reset the game
                        return True
                    elif self.exit_game_button.collidepoint(mouse_pos):
                        return False

            self.screen.fill((0, 0, 0))  # fill the screen with black
            text = self.font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.size[0] // 2, self.size[1] // 2 - 50))
            self.screen.blit(text, text_rect)

            pygame.draw.rect(self.screen, (255, 0, 0), self.play_again_button)
            pygame.draw.rect(self.screen, (255, 0, 0), self.exit_game_button)

            # Draw text on the buttons
            play_again_text = self.font.render("Play Again", True, (255, 255, 255))
            play_again_text_rect = play_again_text.get_rect(center=self.play_again_button.center)
            self.screen.blit(play_again_text, play_again_text_rect)

            exit_game_text = self.font.render("Exit Game", True, (255, 255, 255))
            exit_game_text_rect = exit_game_text.get_rect(center=self.exit_game_button.center)
            self.screen.blit(exit_game_text, exit_game_text_rect)

            pygame.display.flip()

    def draw_grid(self):
        for i in range(4):
            for j in range(4):
                x = i * self.cell_size
                y = j * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                color = (255, 0, 0) if (i, j) == (0, 0) else (255, 255, 255)
                pygame.draw.rect(self.screen, color, rect, 1)

                # Create a text surface and draw it on the screen
                text = self.font.render(f'({i},{j})', True, (255, 255, 255))
                self.screen.blit(text, (x + self.cell_size // 2, y + self.cell_size // 2))

    def update(self):
        self.screen.blit(self.background, (0, 0))  # fill the screen with black

        # Draw the 4x4 grid
        self.draw_grid()

        # Update and draw the agent
        self.agent.update()
        self.agent.draw(self.screen)

        # Check for collision after updating the agent's position
        collision = self.check_collision()
        if collision == 'Wumpus':
            self.game_over_popup('Game Over! The agent encountered the Wumpus.')
        elif collision == 'Pit':  # Added this condition for pit collision
            self.game_over_popup('Game Over! The agent fell into the pit.')

        # Draw the game elements
        for element in self.game_elements:
            element.draw(self.screen)

        pygame.display.flip()  # update the display

    def run(self):
        self.print_element_coordinates()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()

            collision = self.check_collision()
            if collision == 'Wumpus':
                running = self.game_over_popup('Game Over! The agent encountered the Wumpus.')
            elif collision == 'Gold':
                running = self.game_over_popup('Congratulations! The agent found the gold.')

            # Delay for 0.5 seconds
            pygame.time.delay(500)

        pygame.quit()

def start_screen():
    pygame.init()

    # Set the dimensions of the window
    size = (800, 600)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Wumpus World")

    # Load background image
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
                    game_screen = GameScreen()
                    game_screen.run()  # leads to game screen

        screen.blit(background, (0,0))  # fill the screen with black
        screen.blit(button_image, button.topleft)  # draw the button image at the position of the button

        pygame.display.flip()  # update the display

if __name__ == "__main__":
    start_screen()
