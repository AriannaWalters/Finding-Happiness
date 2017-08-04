import pygame
# The use of the main function is described in Chapter 9.
import random

# Define some colors as global constants
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

class Block(pygame.sprite.Sprite):
    """ The class is the player-controlled sprite. """
    # -- Methods
    def __init__(self, filename):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load(filename).convert()

        # Set background color to be transparent. Adjust to WHITE if your
        # background is WHITE.
        self.image.set_colorkey(BLACK)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()


""" Main function for the game. """
# Call this function so the Pygame library can initialize itself
pygame.init()
# Set the width and height of the screen [width,height]
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])


# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(50):
    # This represents a block
    block = Block("Main_Character.png")

     #Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)


    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

# Set the title of the window
pygame.display.set_caption("My Game")

# Set positions of graphics
background_position = [0, 0]

# Load and set up graphics.
background_image = pygame.image.load("bottomBackground.jpg").convert()
player_image = pygame.image.load("Main_Character.png").convert()
player_image.set_colorkey(BLACK)


#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)

display_instructions = True
instruction_page = 1


# -------- Instruction Page Loop -----------
while not done and display_instructions:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            instruction_page += 1
            if instruction_page == 3:
                display_instructions = False
    # Set the screen background
    screen.fill(BLACK)

    if instruction_page == 1:
        # Draw instructions, page 1
        # This could also load an image created in another program.
        # That could be both easier and more flexible.

        text = font.render("Click anywhere to see more Instructions", True, WHITE)
        screen.blit(text, [10, 10])

        text = font.render("To move use left and right arrow keys.", True, WHITE)
        screen.blit(text, [10, 40])

    if instruction_page == 2:
        # Draw instructions, page 2
        text = font.render("Use the spacebar to jump, Don't fall!", True, WHITE)
        screen.blit(text, [10, 10])

        text = font.render("Only jump on stable platforms, Try to get to the top!", True, WHITE)
        screen.blit(text, [10, 40])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()


    # -------- Main Program Loop -----------
while not done:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
            # Set the speed based on the key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    block.changespeed(-3, 0)
                elif event.key == pygame.K_RIGHT:
                    block.changespeed(3, 0)
                elif event.key == pygame.K_SPACE:
                    block.changespeed(0, -3)
        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
            # Reset speed when key goes up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    block.changespeed(3, 0)
                elif event.key == pygame.K_RIGHT:
                    block.changespeed(-3, 0)
                elif event.key == pygame.K_SPACE:
                    block.changespeed(0, 3)

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # Copy image to screen:
        screen.blit(background_image, background_position)

        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        player_position = pygame.mouse.get_pos()
        x = player_position[0]
        y = player_position[1]

        # Copy image to screen:
        screen.blit(player_image, [x, y])

        # Draw sprites
        all_sprites_list.draw(screen)

        pygame.display.flip()

        # Limit to 20 frames per second
        clock.tick(60)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
pygame.quit()
