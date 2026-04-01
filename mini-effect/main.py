# ============================================================
# MAIN.PY - The Main Game Loop
# ============================================================
#
# This is where the game starts! This file contains the main()
# function that sets up the game and runs the game loop.
#
# KEY CONCEPT: The Game Loop
# Games work by running a "loop" very fast (usually 60 times per
# second). Each time through the loop:
# 1. Check for user input (key presses, mouse clicks)
# 2. Update game state (move objects, check collisions)
# 3. Draw everything on screen
# 4. Show the new frame to the player
# ============================================================

# --------------------------------------------------------
# IMPORTS - Load the tools and files we need
# --------------------------------------------------------

# Import pygame library - gives us game development features
import pygame

# Import all constants from our constants file
# The * means "import everything"
from constants import *

# Import a logger that tracks game state (helps with debugging)
from logger import log_state

# Import our Player class from the player.py file
from player import Player


# --------------------------------------------------------
# STARTUP - Print game information
# --------------------------------------------------------

# This runs when the script first loads, before the game starts
# It prints information to help us know the game is starting
print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")


# --------------------------------------------------------
# FUNCTION: main
# The main game function - everything starts here!
# --------------------------------------------------------
def main():
    """
    Set up and run the game.

    This function:
    1. Initializes pygame
    2. Creates the game window
    3. Creates the player
    4. Runs the game loop until the player closes the window
    """

    # Initialize pygame - this MUST be called before using pygame features
    # It sets up all the internal systems pygame needs to work
    pygame.init()

    # Create a clock to control how fast the game runs
    # Think of it like a stopwatch that helps us keep time
    clock = pygame.time.Clock()

    # Create the game window (the "screen")
    # set_mode returns a Surface object we can draw on
    # (SCREEN_WIDTH, SCREEN_HEIGHT) is the window size in pixels
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a Player object in the center of the screen
    # SCREEN_WIDTH / 2 gives us the middle horizontally
    # SCREEN_HEIGHT / 2 gives us the middle vertically
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Delta time - tracks how long each frame takes
    # We initialize it to 0 for the first frame
    dt = 0

    # --------------------------------------------------------
    # THE GAME LOOP - This runs over and over until the game closes
    # --------------------------------------------------------
    while True:
        """
        The Game Loop
        
        This loop runs ~60 times per second (60 FPS).
        Each iteration is one "frame" of the game.
        """

        # Track game state for debugging
        # This logs information that helps us see what's happening
        log_state()

        # --------------------------------------------------------
        # EVENT HANDLING - Check for user input
        # --------------------------------------------------------
        # pygame.event.get() returns a list of all events that happened
        # since the last frame (key presses, mouse clicks, window close, etc.)
        for event in pygame.event.get():
            # Check each event
            if event.type == pygame.QUIT:
                # If the user clicked the X button on the window,
                # we exit the game loop
                return  # This exits the main() function, ending the game

        # --------------------------------------------------------
        # UPDATE - Update game state
        # --------------------------------------------------------
        # clock.tick(60) limits the game to 60 frames per second
        # It returns how long the frame took in milliseconds
        # We divide by 1000 to convert to seconds
        # dt (delta time) helps us move things smoothly regardless of
        # the computer's speed
        dt = clock.tick(60) / 1000

        # --------------------------------------------------------
        # UPDATE - Move the player based on key presses
        # --------------------------------------------------------
        player.update(dt)

        # --------------------------------------------------------
        # DRAW - Render graphics
        # --------------------------------------------------------
        # Step 1: Clear the screen by filling it with black
        # This erases the previous frame so we can draw the new one
        screen.fill("black")

        # Step 2: Draw the player ship on the screen
        # We call the player's draw method and pass it the screen
        # This draws the white triangle at the player's position
        player.draw(screen)

        # Step 3: Update the display
        # pygame.display.flip() shows everything we just drew
        # Without this, we wouldn't see anything!
        pygame.display.flip()

        # The loop then repeats, starting with checking events again


# --------------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------------
# This special line checks if we're running THIS file directly
# (vs importing it from another file)
# If we're running it directly, we start the game!
if __name__ == "__main__":
    main()
