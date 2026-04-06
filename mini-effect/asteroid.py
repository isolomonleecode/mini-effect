# ============================================================
# ASTEROID.PY - The Asteroid Game Objects
# ============================================================
#
# This file contains the Asteroid class, which represents the
# floating rocks that the player must avoid or destroy.
#
# KEY CONCEPT: Class Inheritance
# Asteroid "inherits" from CircleShape, just like Player does!
# This means it automatically gets position, velocity, and radius.
# ============================================================

# --------------------------------------------------------
# IMPORTS - Load the tools we need
# --------------------------------------------------------

# Import the CircleShape base class so we can inherit from it
from circleshape import CircleShape

# Import pygame for drawing features
import pygame

# Import constants: LINE_WIDTH for drawing, ASTEROID_MIN_RADIUS for splitting
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS

# Import the event logger to track game events
from logger import log_event

# Import random for generating random angles when asteroids split
import random


# ============================================================
# CLASS: Asteroid
# A floating rock that moves across the screen
# Inherits from CircleShape (gets position, velocity, radius)
# ============================================================
class Asteroid(CircleShape):
    """
    An asteroid that floats through space.

    Inherits from CircleShape, which provides:
    - position (x, y coordinates)
    - velocity (movement speed and direction)
    - radius (size for collision detection and drawing)
    """

    # --------------------------------------------------------
    # METHOD: __init__ (Constructor)
    # Called when we create a new Asteroid object
    # --------------------------------------------------------
    def __init__(self, x, y, radius):
        """
        Create a new Asteroid at position (x, y) with the given size.

        Args:
            x: Starting horizontal position
            y: Starting vertical position
            radius: How big this asteroid is
        """
        # Call the parent class's __init__ method
        # This sets up position, velocity, and radius
        super().__init__(x, y, radius)

    # --------------------------------------------------------
    # METHOD: draw
    # Draw the asteroid as a white circle on the screen
    # --------------------------------------------------------
    def draw(self, screen):
        """
        Draw the asteroid as a white circle outline.

        Args:
            screen: The pygame surface to draw on
        """
        # pygame.draw.circle draws a circle outline
        # Parameters: screen, color, center position, radius, line width
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    # --------------------------------------------------------
    # METHOD: update
    # Move the asteroid each frame based on its velocity
    # --------------------------------------------------------
    def update(self, dt):
        """
        Move the asteroid based on its velocity.

        Args:
            dt: Delta time in seconds (time since last frame)
        """
        # velocity * dt gives us how far to move this frame
        self.position += self.velocity * dt

    # --------------------------------------------------------
    # METHOD: split
    # Destroy this asteroid and spawn two smaller ones
    # --------------------------------------------------------
    def split(self):
        """
        Destroy this asteroid. If it's big enough, spawn two smaller
        asteroids that fly off in different directions.

        Large asteroids split into medium ones.
        Medium asteroids split into small ones.
        Small asteroids just disappear.
        """
        # Step 1: Always destroy this asteroid — it's been hit!
        self.kill()

        # Step 2: If this asteroid is already small, just disappear
        # No new asteroids to spawn
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Step 3: Log that an asteroid split happened
        log_event("asteroid_split")

        # Step 4: Generate ONE random angle between 20 and 50 degrees
        # This determines how far apart the two new asteroids fly
        random_angle = random.uniform(20, 50)

        # Step 5: Create two new velocity vectors by rotating the original
        # The first one rotates in one direction...
        first_split = self.velocity.rotate(random_angle)
        # ...and the second rotates in the OPPOSITE direction
        second_split = self.velocity.rotate(-random_angle)

        # Step 6: Calculate the new, smaller radius
        # Each split makes the asteroid smaller by ASTEROID_MIN_RADIUS
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Step 7: Create two new asteroids at the same position
        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        # Give the first one its new velocity, scaled up by 20% faster
        first_asteroid.velocity = first_split * 1.2

        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        # Give the second one its new velocity, also 20% faster
        second_asteroid.velocity = second_split * 1.2
