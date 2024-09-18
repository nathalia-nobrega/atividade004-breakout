import pygame

# Define some colors
WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)
BLACK = (0,0,0)
RED = (255,0,0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)

class Paddle(pygame.sprite.Sprite):
    # This class represents a paddle. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the paddle, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

pygame.init()

score = 0
lives = 3

# Open a new window
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

#Create the Paddle
paddle = Paddle(LIGHTBLUE, 70, 15)
paddle.rect.x = 350
paddle.rect.y = 560

# Add the paddle to the list of sprites
all_sprites_list.add(paddle)

# The loop will carry on until the user exits the game (e.g. clicks the close button).
game_running = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while game_running:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            game_running = False  # Flag that we are done so we exit this loop

    # --- Game logic should go here
    all_sprites_list.update()
    # --- Drawing code should go here
    # First, clear the screen to dark blue.
    screen.fill(BLACK)
    # Display the score and the number of lives at the top of the screen
    font = pygame.font.Font(None, 34)
    # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)
    # --- Update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()