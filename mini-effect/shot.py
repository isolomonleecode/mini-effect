# ============================================================
# SHOT.PY - The Player's Bullets
# ============================================================
#
# This file contains the Shot class, which represents a bullet
# fired by the player's spaceship.
#
# Just like Asteroid and Player, Shot inherits from CircleShape!
# ============================================================

# --------------------------------------------------------
# IMPORTS - Load the tools we need
# --------------------------------------------------------

# Import the CircleShape base class (same as Asteroid does!)
from circleshape import CircleShape

# Import pygame for Vector2 and drawing
import pygame

# Import the constants we need
from constants import LINE_WIDTH, SHOT_RADIUS, PLAYER_SHOOT_SPEED


# ============================================================
# CLASS: Shot
# A bullet fired by the player
# Inherits from CircleShape (gets position, velocity, radius)
# ============================================================
class Shot(CircleShape):
    """
    A shot/bullet fired by the player.

    Inherits from CircleShape, which provides:
    - position (x, y coordinates)
    - velocity (movement speed and direction)
    - radius (size for collision detection)
    """

    # --------------------------------------------------------
    # METHOD: __init__ (Constructor)
    # Called when we create a new Shot object
    # --------------------------------------------------------
    def __init__(self, x, y):
        """
        Create a new Shot at position (x, y).

        Args:
            x: Starting horizontal position
            y: Starting vertical position
        """
        # Call the parent class's __init__ method
        # This sets up position, velocity, and radius using SHOT_RADIUS
        # Notice: we don't pass radius as a parameter — shots always use SHOT_RADIUS!
        super().__init__(x, y, SHOT_RADIUS)

    # --------------------------------------------------------
    # METHOD: draw
    # Draw the shot as a small white circle on the screen
    # --------------------------------------------------------
    def draw(self, screen):
        """
        Draw the shot as a small white circle.

        Args:
            screen: The pygame surface to draw on
        """
        # This is IDENTICAL to how Asteroid draws itself!
        # pygame.draw.circle draws a circle outline
        # Parameters: screen, color, center position, radius, line width
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    # --------------------------------------------------------
    # METHOD: update
    # Move the shot each frame based on its velocity
    # --------------------------------------------------------
    def update(self, dt):
        """
        Move the shot based on its velocity.

        Args:
            dt: Delta time in seconds (time since last frame)
        """
        # This is IDENTICAL to how Asteroid updates itself!
        # velocity * dt gives us how far to move this frame
        self.position += self.velocity * dt
