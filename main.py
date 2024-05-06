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
        self.fog_image = pygame.image.load('assets/fog.png')
        self.background = pygame.image.load('assets/gamescreenbg.png')

    def draw_grid(self):
        for i in range(4):
            for j in range(4):
                x = i * self.cell_size
                y = j * self.cell_size
                text = self.font.render(f'({i},{j})', True, (255, 255, 255))
                self.screen.blit(text, (x + self.cell_size // 2, y + self.cell_size // 2))

    '''def draw_fog(self, visited):
        for i in range(4):
            for j in range(4):
                if not visited[i][j] and not (i == 0 and j == 0):  # Exclude (0,0) from fog
                    x = i * self.cell_size
                    y = j * self.cell_size
                    self.screen.blit(self.fog_image, (x, y))'''

    def update(self, agent, visited):
        self.screen.blit(self.background, (0,0))
        self.draw_grid()
        agent.draw(self.screen)
        #self.draw_fog(visited)
        pygame.display.flip()

class GameElement:
    def __init__(self, cell_size, image_path, name):
        self.cell_size = cell_size
        self.image = pygame.image.load(image_path)
        self.name = name
        self.reset()

    def draw(self, screen):
        screen.blit(self.image, (self.x * self.cell_size, self.y * self.cell_size))

    def reset(self, taken_positions=None):
        if taken_positions is None:
            taken_positions = []
        while True:
            self.x = random.randint(0, 3)
            self.y = random.randint(0, 3)
            if (self.x, self.y) not in taken_positions and (self.x, self.y) != (0, 0):
                taken_positions.append((self.x, self.y))
                break

class GameScreen:
    def __init__(self):
        pygame.init()

        # Set the dimensions of the window
        self.size = (700, 700)
        self.screen = pygame.display.set_mode(self.size)
        self.visited = [[False] * 4 for _ in range(4)]  # Assuming a 4x4 grid
        self.ROWS = 4
        self.COLS = 4

        pygame.display.set_caption("Game is Running")

        self.background = pygame.image.load('assets/gamescreenbg.png')

        # Define the size of the grid cells
        self.cell_size = self.size[0] // 4  # Make the cell size a quarter of the screen width and height

        self.font = pygame.font.Font(None, 24)  # Define a font object

        # Create the agent
        self.agent = Agent(self.cell_size)

        # Create the game elements
        self.game_elements = []

        # Create and place the Wumpus
        wumpus = GameElement(self.cell_size, 'assets/wumpus.png', 'Wumpus')
        self.game_elements.append(wumpus)

        # Create and place the Gold
        gold = GameElement(self.cell_size, 'assets/gold.png', 'Gold')
        self.game_elements.append(gold)

        # Create and place the Pit
        pit = GameElement(self.cell_size, 'assets/pit.png', 'Pit')
        self.game_elements.append(pit)

        # Create and place the Stench near the Wumpus
        stench = GameElement(self.cell_size, 'assets/stench.png', 'Stench')
        stench.reset(taken_positions=self.get_adjacent_positions((wumpus.x, wumpus.y)))
        self.game_elements.append(stench)

        # Create and place the Glitter near the Gold
        glitter = GameElement(self.cell_size, 'assets/glitter.png', 'Glitter')
        glitter.reset(taken_positions=self.get_adjacent_positions((gold.x, gold.y)))
        self.game_elements.append(glitter)

        # Create and place the Breeze near the Pit
        breeze = GameElement(self.cell_size, 'assets/breeze.png', 'Breeze')
        breeze.reset(taken_positions=self.get_adjacent_positions((pit.x, pit.y)))
        self.game_elements.append(breeze)

        # Define play again and exit game buttons
        button_width = 150
        button_height = 50
        self.play_again_button = pygame.Rect((self.size[0] - button_width) // 2, (self.size[1] - button_height) // 2 + 100, button_width, button_height)
        self.exit_game_button = pygame.Rect((self.size[0] - button_width) // 2, (self.size[1] - button_height) // 2 + 200, button_width, button_height)

        # Instantiate the Screen object
        self.screen_manager = Screen(self.size)

        # Define the number of rows and columns in the grid
        self.ROWS = 4
        self.COLS = 4

    def reset_game(self):
        self.visited = [[False] * 4 for _ in range(4)]
        taken_positions = []
        for element in self.game_elements:
            if element.name in ['Wumpus', 'Gold', 'Pit']:
                element.reset(taken_positions)
                taken_positions.append((element.x, element.y))
            else:
                element.reset(taken_positions=self.get_adjacent_positions((element.x, element.y)))
                taken_positions.append((element.x, element.y))
        self.agent = Agent(self.cell_size)

    def get_adjacent_positions(self, position):
        x, y = position
        positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]  # left, right, up, down
        valid_positions = [(x, y) for x, y in positions if 0 <= x < self.ROWS and 0 <= y < self.COLS]
        return valid_positions
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

                # Check if the square has been visited
                if self.visited[i][j]:
                    pygame.draw.rect(self.screen, color, rect, 1)
                else:
                    # Render fog for unvisited squares
                    fog_color = (100, 100, 100)  # Adjust fog color as needed
                    pygame.draw.rect(self.screen, fog_color, rect)

                # Create a text surface and draw it on the screen
                text = self.font.render(f'({i},{j})', True, (255, 255, 255))
                self.screen.blit(text, (x + self.cell_size // 2, y + self.cell_size // 2))

    def update_visited(self, x, y):
        self.visited[x][y] = True

    def update(self):
        self.screen.blit(self.background, (0, 0))

        self.screen_manager.draw_grid()  # Draw the grid

        # Render all game elements
        for element in self.game_elements:
            element.draw(self.screen)

        self.agent.update()
        self.agent.draw(self.screen)
        self.update_visited(self.agent.x, self.agent.y)

        # Collision check and game over handling
        self.get_adjacent_positions((self.agent.x, self.agent.y))
        pygame.display.flip()

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
            elif collision == 'Pit':
                running = self.game_over_popup('Game Over! The agent fell into a pit.')

            # Delay for 0.5 seconds
            pygame.time.delay(5000)

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
