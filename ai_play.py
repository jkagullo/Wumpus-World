import pygame
import random

class Agent:
    def __init__(self, cols, rows):
        self.COLS = cols
        self.ROWS = rows
        self.pos = (0, 0)  # Start at the top-left cell
        self.direction = "down"  # Initial direction
        self.has_arrow = False
        self.is_shooting = False
        self.arrow_direction = self.direction
        self.knowledge_base = {
            "visited": set(),
            "stench": set(),
            "breeze": set()
        }

    def process_percept(self, percept):
        stench, breeze = percept
        x, y = self.pos

        # Update knowledge base
        self.knowledge_base["visited"].add((x, y))
        if stench:
            self.knowledge_base["stench"].add((x, y))
        if breeze:
            self.knowledge_base["breeze"].add((x, y))

    def move(self, percept):
        x, y = self.pos

        # Unpack the percept tuple
        stench, breeze = percept

        # Process the percept and update knowledge base
        self.process_percept(percept)

        # Apply logical reasoning based on the knowledge base and choose direction
        if (x, y) in self.knowledge_base["stench"]:
            # If stench is perceived, avoid moving towards it
            if self.direction == "up":
                self.direction = "right" if random.random() < 0.5 else "left"
            elif self.direction == "down":
                self.direction = "right" if random.random() < 0.5 else "left"
            elif self.direction == "left":
                self.direction = "up" if random.random() < 0.5 else "down"
            elif self.direction == "right":
                self.direction = "up" if random.random() < 0.5 else "down"
        elif (x, y) in self.knowledge_base["breeze"]:
            # If breeze is perceived, avoid moving towards it
            if self.direction == "up":
                self.direction = "right" if random.random() < 0.5 else "left"
            elif self.direction == "down":
                self.direction = "right" if random.random() < 0.5 else "left"
            elif self.direction == "left":
                self.direction = "up" if random.random() < 0.5 else "down"
            elif self.direction == "right":
                self.direction = "up" if random.random() < 0.5 else "down"
        else:
            # If no percept is present, move randomly
            if random.random() < 0.5:
                # Change direction randomly
                self.direction = random.choice(["up", "down", "left", "right"])

        # Face the direction first
        if self.direction == "up":
            self.direction = "up"
        elif self.direction == "down":
            self.direction = "down"
        elif self.direction == "left":
            self.direction = "left"
        elif self.direction == "right":
            self.direction = "right"

        # Then move forward
        if self.direction == "up":
            self.pos = (x, y - 1) if y > 0 else (x, y)
        elif self.direction == "down":
            self.pos = (x, y + 1) if y < self.ROWS - 1 else (x, y)
        elif self.direction == "left":
            self.pos = (x - 1, y) if x > 0 else (x, y)
        elif self.direction == "right":
            self.pos = (x + 1, y) if x < self.COLS - 1 else (x, y)

    def handle_shooting(self, world):
        if not self.is_shooting and self.has_arrow:
            x, y = self.pos
            # Check if the Wumpus is detected in any of the adjacent cells
            if (x + 1, y) == self.world.wumpus_pos or \
                    (x - 1, y) == self.world.wumpus_pos or \
                    (x, y + 1) == self.world.wumpus_pos or \
                    (x, y - 1) == self.world.wumpus_pos:
                # If the Wumpus is detected, shoot the arrow
                self.shoot()
                print("The agent shoots the arrow at the Wumpus!")

    def shoot(self):
        if self.has_arrow:
            self.is_shooting = True
            self.arrow_direction = self.direction
            self.has_arrow = False


class WumpusWorld:
    def __init__(self, cols, rows):
        self.COLS = cols
        self.ROWS = rows
        self.occupied_cells = []

    def place_wumpus_and_stench(self):
        while True:
            pos = (random.randint(0, self.COLS - 1), random.randint(0, self.ROWS - 1))
            if pos not in [(0,0),(0,1),(1,0),(1,1)] and pos not in self.occupied_cells:
                self.occupied_cells.append(pos)
                self.wumpus_pos = pos
                break

        row, col = self.wumpus_pos
        self.stench_pos = []

        if row > 0:
            self.stench_pos.append((row - 1, col))
        if row < self.ROWS - 1:
            self.stench_pos.append((row + 1, col))
        if col > 0:
            self.stench_pos.append((row, col - 1))
        if col < self.COLS - 1:
            self.stench_pos.append((row, col + 1))

    def place_pit_and_breeze(self):
        while True:
            pos = (random.randint(0, self.COLS -1), random.randint(0, self.ROWS -1))
            if pos not in [(0, 0), (0, 1), (1, 0), (1, 1)] and pos not in self.occupied_cells:
                self.occupied_cells.append(pos)
                self.pit_pos = pos
                break

        row, col = self.pit_pos
        self.breeze_pos = []

        if row > 0:
            self.breeze_pos.append((row - 1, col))
        if row < self.ROWS - 1:
            self.breeze_pos.append((row + 1, col))
        if col > 0:
            self.breeze_pos.append((row, col - 1))
        if col < self.COLS - 1:
            self.breeze_pos.append((row, col + 1))

    def place_gold_and_glitter(self):
        while True:
            pos = (random.randint(0, self.COLS -1), random.randint(0, self.ROWS -1))
            if pos not in [(0, 0), (0, 1), (1, 0), (1, 1)] and pos not in self.occupied_cells:
                self.occupied_cells.append(pos)
                self.gold_pos = pos
                break

        row, col = self.gold_pos
        self.glitter_pos = []

        if row > 0:
            self.glitter_pos.append((row - 1, col))
        if row < self.ROWS - 1:
            self.glitter_pos.append((row + 1, col))
        if col > 0:
            self.glitter_pos.append((row, col - 1))
        if col < self.COLS - 1:
            self.glitter_pos.append((row, col + 1))

    def place_arrow(self):
        while True:
            pos = (random.randint(0, self.COLS - 1), random.randint(0, self.ROWS - 1))
            if pos not in [(0, 0), (0, 1), (1, 0), (1, 1)] and pos not in self.occupied_cells:
                self.occupied_cells.append(pos)
                self.arrow_pos = pos
                break

    # implement arrow

    def check_arrow_hit(self, arrow_pos, arrow_direction):
        # Check if the arrow hit the wumpus
        if arrow_direction == "up":
            for y in range(arrow_pos[1], -1, -1):
                if (arrow_pos[0], y) == self.wumpus_pos:
                    return True
        elif arrow_direction == "down":
            for y in range(arrow_pos[1], self.ROWS):
                if (arrow_pos[0], y) == self.wumpus_pos:
                    return True
        elif arrow_direction == "left":
            for x in range(arrow_pos[0], -1, -1):
                if (x, arrow_pos[1]) == self.wumpus_pos:
                    return True
        elif arrow_direction == "right":
            for x in range(arrow_pos[0], self.COLS):
                if (x, arrow_pos[1]) == self.wumpus_pos:
                    return True
        return False

    def is_stench(self, pos):
        return pos in self.stench_pos

    def is_breeze(self, pos):
        return pos in self.breeze_pos

    def setup(self):
        # Place wumpus and stench
        self.place_wumpus_and_stench()
        print(f"Wumpus pos: {self.wumpus_pos}")
        print(f"Stench pos: {self.stench_pos}")

        # Place pit and breeze
        self.place_pit_and_breeze()
        print(f"Pit pos: {self.pit_pos}")
        print(f"Breeze pos: {self.breeze_pos}")

        # Place gold and glitter
        self.place_gold_and_glitter()
        print(f"Gold pos: {self.gold_pos}")
        print(f"Glitter pos: {self.glitter_pos}")

        # Place arrow
        self.place_arrow()
        print(f"Arrow pos: {self.arrow_pos}")

        # Print occupied cells
        print(f"Occupied cells: {self.occupied_cells}")

class StartScreen:
    def __init__(self):
        pygame.init()
        self.size = (700, 700)
        self.screen = pygame.display.set_mode(self.size)
        self.button_image = pygame.image.load("assets/startbutton.png")
        self.button_rect = self.button_image.get_rect()
        self.button_rect.center = (self.size[0] // 2, self.size[1] // 2)
        pygame.display.set_caption("Start Screen")
        self.start_screen_bg = pygame.image.load("assets/splash.png")


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        game_screen = GameScreen()
                        game_screen.run()
                        running = False

            self.screen.blit(self.start_screen_bg, (0,0))
            self.screen.blit(self.button_image, self.button_rect.topleft)
            pygame.display.flip()

class GameScreen:
    def __init__(self):
        pygame.init()
        self.size = (700, 800)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Wumpus World")
        self.COLS = 4
        self.ROWS = 4
        self.grid_size = (700, 700)
        self.cell_width = self.grid_size[0] // self.COLS
        self.cell_height = self.grid_size[1] // self.ROWS
        self.font = pygame.font.Font(None, 24)  # Create a font object
        # Background image
        self.game_background_image = pygame.image.load("assets/gamescreenbg.png")
        self.fog_covered_cells = {(i, j) for i in range(self.COLS) for j in range(self.ROWS) if (i, j) != (0, 0)}

        # load fog
        self.fog_image = pygame.image.load("assets/fog.png")
        # Load images for elements
        self.wumpus_image = pygame.image.load("assets/wumpus.png")
        self.arrow_image = pygame.image.load("assets/arrow.png")
        self.breeze_image = pygame.image.load("assets/breeze.png")
        self.fog_image = pygame.image.load("assets/fog.png")
        self.gold_image = pygame.image.load("assets/gold.png")
        self.pit_image = pygame.image.load("assets/pit.png")
        self.stench_image = pygame.image.load("assets/stench.png")
        self.glitter_image = pygame.image.load("assets/glitter.png")

        # Load images for holding arrow images
        self.hold_arrow_images = {
            "up": pygame.image.load("assets/agent/hold_up.png"),
            "down": pygame.image.load("assets/agent/hold_down.png"),
            "left": pygame.image.load("assets/agent/hold_left.png"),
            "right": pygame.image.load("assets/agent/hold_right.png")
        }

        # Load images for arrow direction
        self.arrow_images = {
            "up": pygame.image.load("assets/agent/arrow_up.png"),
            "down": pygame.image.load("assets/agent/arrow_down.png"),
            "left": pygame.image.load("assets/agent/arrow_left.png"),
            "right": pygame.image.load("assets/agent/arrow_right.png")
        }

        # Load images for agent movement
        self.agent_images = {
            "up": pygame.image.load("assets/agent/agent_up.png"),
            "down": pygame.image.load("assets/agent/agent_down.png"),
            "left": pygame.image.load("assets/agent/agent_left.png"),
            "right": pygame.image.load("assets/agent/agent_right.png")
        }

    def draw_grid(self):
        for i in range(self.COLS):
            for j in range(self.ROWS):
                pygame.draw.rect(self.screen, (255, 255, 255), (i * self.cell_width, j * self.cell_height, self.cell_width, self.cell_height), 1)
                text = self.font.render(f"({i}, {j})", True, (255, 255, 255))
                self.screen.blit(text, (i * self.cell_width + 10, j * self.cell_height + 10))  # Adjust the position of the text

    def draw_elements(self,world,agent):
        # draw stench
        for pos in world.stench_pos:
            stench_rect = pygame.Rect(pos[0] * self.cell_width, pos[1] * self.cell_height, self.cell_width,self.cell_height)
            self.screen.blit(self.stench_image, stench_rect)

        # draw pit
        if world.pit_pos is not None:
            pit_rect = pygame.Rect(world.pit_pos[0] * self.cell_width, world.pit_pos[1] * self.cell_height, self.cell_width, self.cell_height)
            self.screen.blit(self.pit_image, pit_rect)

        # draw breeze
        for pos in world.breeze_pos:
            breeze_rect = pygame.Rect(pos[0] * self.cell_width, pos[1] * self.cell_height, self.cell_width,self.cell_height)
            self.screen.blit(self.breeze_image, breeze_rect)

        # draw glitter
        for pos in world.glitter_pos:
            glitter_rect = pygame.Rect(pos[0] * self.cell_width, pos[1] * self.cell_height, self.cell_width,self.cell_height)
            self.screen.blit(self.glitter_image, glitter_rect)

        # draw arrow
        if world.arrow_pos is not None:
            arrow_rect = pygame.Rect(world.arrow_pos[0] * self.cell_width, world.arrow_pos[1] * self.cell_height,self.cell_width, self.cell_height)
            self.screen.blit(self.arrow_image, arrow_rect)

        # draw gold
        if world.gold_pos is not None:
            gold_rect = pygame.Rect(world.gold_pos[0] * self.cell_width, world.gold_pos[1] * self.cell_height,
                                    self.cell_width, self.cell_height)
            self.screen.blit(self.gold_image, gold_rect)

        # draw wumpus
        if world.wumpus_pos is not None:
            wumpus_rect = pygame.Rect(world.wumpus_pos[0] * self.cell_width, world.wumpus_pos[1] * self.cell_height,self.cell_width, self.cell_height)
            self.screen.blit(self.wumpus_image, wumpus_rect)

        # Draw agent
        agent_rect = pygame.Rect(agent.pos[0] * self.cell_width, agent.pos[1] * self.cell_height, self.cell_width,self.cell_height)
        if agent.has_arrow:
            self.screen.blit(self.hold_arrow_images[agent.direction], agent_rect)
        else:
            self.screen.blit(self.agent_images[agent.direction], agent_rect)

        for pos in self.fog_covered_cells:
            fog_rect = pygame.Rect(pos[0] * self.cell_width, pos[1] * self.cell_height, self.cell_width,
                                   self.cell_height)
            self.screen.blit(self.fog_image, fog_rect)

    # Implement the arrow
    def handle_arrow(self, world, agent):
        # if the agent is on the arrow cell and doesnt have the arrow yet, pick it up
        if agent.pos == world.arrow_pos and not agent.has_arrow:
            agent.has_arrow = True
            world.arrow_pos = None # remove the arrow from the world
            if agent.pos in self.fog_covered_cells:
                self.fog_covered_cells.remove(agent.pos)  # Remove fog from the cell
            print("The agent grabs the arrow")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not agent.is_shooting and agent.has_arrow:
            agent.shoot()
            print("The agent shoots the arrow")
            self.animate_arrow(agent)  # Animate the arrow
            if agent.is_shooting:
                arrow_hit = world.check_arrow_hit(agent.pos, agent.arrow_direction)
                if arrow_hit:
                    print("The agent shot the wumpus and won the game!")
                    return "win"
                    # implement winning condition
                agent.is_shooting = False

    def animate_arrow(self, agent):
        arrow_direction = agent.arrow_direction
        arrow_pos = list(agent.pos)  # Start from the agent's position
        while True:
            # Update arrow position based on the direction
            if arrow_direction == "up":
                arrow_pos[1] -= 1
            elif arrow_direction == "down":
                arrow_pos[1] += 1
            elif arrow_direction == "left":
                arrow_pos[0] -= 1
            elif arrow_direction == "right":
                arrow_pos[0] += 1

            # Check if the arrow is still within the grid
            if 0 <= arrow_pos[0] < self.COLS and 0 <= arrow_pos[1] < self.ROWS:
                # Draw the arrow
                arrow_rect = pygame.Rect(arrow_pos[0] * self.cell_width, arrow_pos[1] * self.cell_height,
                                         self.cell_width, self.cell_height)
                self.screen.blit(self.arrow_images[arrow_direction], arrow_rect)
                pygame.display.flip()
                pygame.time.wait(100)  # Wait for a short time to create the animation effect
            else:
                break  # If the arrow is out of the grid, stop the animation

    def check_game_state(self, world, agent):
        if agent.pos == world.wumpus_pos:
            print("The agent was killed by the wumpus, the agent lose!")
            return "lose"
        elif agent.pos == world.pit_pos:
            print("The agent fell into a pit, the agent lose!")
            return "lose"
        elif agent.pos == world.gold_pos:
            print("The agent grabs the gold, the agent won!")
            return "win"
        elif agent.is_shooting and world.check_arrow_hit(agent.pos, agent.arrow_direction):
            print("The agent shot the wumpus, the agent won!")
            return "win"
        return None

    def run(self):
        world = WumpusWorld(self.COLS, self.ROWS)
        world.setup()
        # Define the agent from agent class
        agent = Agent(self.COLS, self.ROWS)

        # Define the timer event for moving the agent
        MOVE_AGENT_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(MOVE_AGENT_EVENT, 1000)  # Move the agent every 1000 milliseconds (1 second)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == MOVE_AGENT_EVENT:
                    # Move the agent automatically
                    percept = (world.is_stench(agent.pos), world.is_breeze(agent.pos))
                    agent.move(percept)

            agent.handle_shooting(world)
            self.fog_covered_cells.discard(agent.pos)
            self.screen.blit(self.game_background_image, (0, 0))
            self.draw_grid()
            self.draw_elements(world, agent)
            self.handle_arrow(world, agent)
            game_state = self.check_game_state(world, agent)
            if game_state is not None:
                running = False
                end_screen = EndGameScreen(self)
                end_screen.run()
            pygame.display.flip()


class EndGameScreen:
    def __init__(self, game_screen):
        self.game_screen = game_screen
        pygame.init()
        self.size = (500, 500)
        self.screen = pygame.display.set_mode(self.size)

        self.new_game_button_image = pygame.image.load("assets/playagainbutton.png")
        self.exit_game_button_image = pygame.image.load("assets/exitbutton.png")

        pygame.display.set_caption("Game Ended.")

        self.end_bg_image = pygame.image.load("assets/endbg.png")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.new_game_button_image_rect.collidepoint(event.pos):
                        pygame.quit()  # Dispose of the initial game
                        game_screen = GameScreen()  # Start a new game
                        game_screen.run()
                        running = False
                    elif self.exit_game_button_image_rect.collidepoint(event.pos):
                        running = False
                        pygame.quit()
                        quit()

            self.screen.blit(self.end_bg_image, (0, 0))

            # Get rect for button images
            self.new_game_button_image_rect = self.new_game_button_image.get_rect()
            self.exit_game_button_image_rect = self.exit_game_button_image.get_rect()

            # Center the buttons horizontally and vertically
            self.new_game_button_image_rect.center = (self.size[0] // 2, self.size[1] // 2 - 10)
            self.exit_game_button_image_rect.center = (self.size[0] // 2, self.size[1] // 2 + 60)

            # Blit button images onto the screen
            self.screen.blit(self.new_game_button_image, self.new_game_button_image_rect)
            self.screen.blit(self.exit_game_button_image, self.exit_game_button_image_rect)

            pygame.display.flip()


if __name__ == "__main__":
    start_screen = StartScreen()
    start_screen.run()