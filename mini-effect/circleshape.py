# ============================================================
# CIRCLESHAPE.PY - Base Class for Game Objects
# ============================================================
#
# This is a "base class" - it's a template that other classes
# (like Player) will inherit from. Think of it like a blueprint
# that other classes can expand upon.
#
# KEY CONCEPT: Inheritance
# When a class "inherits" from another, it gets all the methods
# and attributes of the parent class, then can add its own.
# ============================================================

# Step 1: Import pygame so we can use its features
import pygame

# Step 2: Import the LINE_WIDTH constant we defined earlier
# (We're not using it in this file yet, but Player will!)
from constants import LINE_WIDTH

import logger


# ============================================================
# CLASS: CircleShape
# A template for objects in the game that have a circular shape
# ============================================================
class CircleShape(pygame.sprite.Sprite):
    """
    Base class for all circular game objects.

    Attributes:
        position: A 2D vector (x, y) telling where the object is on screen
        velocity: A 2D vector telling how fast and which direction it moves
        radius: How big the object is (used for collisions and drawing)
    """

    # --------------------------------------------------------
    # METHOD: __init__ (Constructor)
    # Called when we create a new object of this class
    # --------------------------------------------------------
    def __init__(self, x, y, radius):
        """
        Initialize a new CircleShape object.

        Args:
            x: Starting horizontal position
            y: Starting vertical position
            radius: Size of the object
        """
        # pygame.sprite.Sprite is a built-in pygame class for game objects
        # that can be grouped together. The super() line calls the parent
        # class's __init__ method.

        # This if statement handles pygame's sprite container system
        # Don't worry too much about this - it's boilerplate code!
        if hasattr(self, "containers"):
            super().__init__(self.containers)  # Call parent with containers
        else:
            super().__init__()  # Call parent without containers

        # pygame.Vector2 creates a 2D vector (like an arrow with direction and length)
        # We use vectors to track position and velocity

        # Store the position as a vector (x, y coordinates)
        self.position = pygame.Vector2(x, y)

        # Start with zero velocity (not moving initially)
        # Later, we'll change this to make objects move!
        self.velocity = pygame.Vector2(0, 0)

        # Store the radius (size) of this object
        self.radius = radius

    # --------------------------------------------------------
    # METHOD: draw
    # Draw the object on the screen
    # --------------------------------------------------------
    def draw(self, screen):
        """
        Draw this object. This is a "placeholder" method that
        will be overridden by child classes (like Player).

        Args:
            screen: The pygame surface to draw on
        """
        # We use 'pass' here because this is just a placeholder.
        # The 'pass' statement means "do nothing"
        # Each child class (like Player) will override this with
        # its own drawing code!
        pass

    # --------------------------------------------------------
    # METHOD: update
    # Update the object's state (position, etc.)
    # --------------------------------------------------------
    def update(self, dt):
        """
        Update the object's state each frame.
        This is called every frame (usually 60 times per second).

        Args:
            dt: Delta time - the time since the last frame
                This helps us move objects smoothly regardless of
                how fast the computer is!
        """
        # Placeholder - child classes will override this
        pass

    # --------------------------------------------------------
    # METHOD: collides_with
    # Check if this shape collides with another shape
    # --------------------------------------------------------
    def collides_with(self, other):
        """
        Check if this circle collides with another circle.

        Two circles collide when the distance between their centers
        is less than the sum of their radii.

        Args:
            other: Another CircleShape object to check against

        Returns:
            True if the circles overlap (collide), False otherwise
        """
        # Get the distance between the centers of both circles
        distance = self.position.distance_to(other.position)

        # They collide if distance is less than the sum of their radii
        return distance < self.radius + other.radius
