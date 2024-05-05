import pygame
import sys

def start_screen():
    pygame.init()

    # Set the dimensions of the window
    size = (800, 600)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Wumpus World")

    #load background image
    background = pygame.image.load('assets/splash.png')

    button = pygame.Rect(350, 350, 150, 50) # creates a rect object
    font = pygame.font.Font(None, 36)
    text = font.render('Start Game', True, (0, 0, 0))  # create text surface
    textRect = text.get_rect(center=button.center)  # center the text on the button

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
        pygame.draw.rect(screen, [0, 255, 0], button)  # draw button with green color
        screen.blit(text, textRect)  # draw text on button

        pygame.display.flip()  # update the display

def game_screen():
    pygame.init()

    # Set the dimensions of the window
    size = (800, 600)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Game is Running")

    font = pygame.font.Font(None, 36)
    text = font.render('Game is running', True, (255, 255, 255), (0, 0, 0))

    textRect = text.get_rect()
    textRect.center = (400, 300)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0,0,0))  # fill the screen with black
        screen.blit(text, textRect)

        pygame.display.flip()  # update the display

    pygame.quit()

if __name__ == "__main__":
    start_screen()