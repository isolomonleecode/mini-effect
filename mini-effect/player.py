# ============================================================
# PLAYER.PY - The Player Spaceship
# ============================================================
#
# This file contains the Player class, which is the spaceship
# that the user controls in the game.
#
# KEY CONCEPT: Class Inheritance
# Player "inherits" from CircleShape, which means it automatically
# gets all the attributes and methods from CircleShape (like
# position, velocity, radius) plus its own special ones!
# ============================================================

# --------------------------------------------------------
# IMPORTS - Load the tools we need
# --------------------------------------------------------

# Import the CircleShape base class so we can inherit from it
from circleshape import CircleShape

# Import game constants we'll need
# PLAYER_RADIUS: How big the player ship is
# LINE_WIDTH: How thick the ship's lines should be
from constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
)

# Import pygame for game features (Vector2, drawing, etc.)
import pygame

# Import the Shot class so we can create bullets
from shot import Shot


# ============================================================
# CLASS: Player
# The spaceship that the player controls
# Inherits from CircleShape (gets position, velocity, radius, etc.)
# ============================================================
class Player(CircleShape):
    """
    The player's spaceship in the game.

    Inherits from CircleShape, which provides:
    - position (x, y coordinates)
    - velocity (movement speed and direction)
    - radius (size for collision detection)

    Adds:
    - rotation (which direction the ship is facing)
    - triangle() method (calculates ship shape points)
    - draw() method (draws the ship on screen)
    """

    # --------------------------------------------------------
    # METHOD: __init__ (Constructor)
    # Called when we create a new Player object
    # --------------------------------------------------------
    def __init__(self, x, y):
        """
        Create a new Player at position (x, y).

        Args:
            x: Starting horizontal position (left to right)
            y: Starting vertical position (top to bottom)
        """
        # Call the parent class's __init__ method
        # This sets up position, velocity, and radius using
        # the PLAYER_RADIUS constant we imported
        super().__init__(x, y, PLAYER_RADIUS)

        # Set the initial rotation to 0 (facing upward)
        # Rotation is measured in degrees:
        # 0 = up, 90 = right, 180 = down, 270 = left
        self.rotation = 0

        # Track how long until the player can shoot again
        # Starts at 0 so the player can shoot immediately
        self.shoot_timer = 0

    # --------------------------------------------------------
    # METHOD: triangle
    # Calculate the three points to draw a triangle (the ship shape)
    # --------------------------------------------------------
    def triangle(self):
        """
        Calculate the three corner points of the triangle ship.

        The ship is a triangle that points in the direction it's facing.
        This method uses trigonometry to calculate where those three
        corners should be based on the ship's position and rotation.

        Returns:
            A list of 3 pygame.Vector2 points [a, b, c]:
            - a: The tip of the triangle (front of ship)
            - b: Bottom-left corner
            - c: Bottom-right corner
        """
        # Create a vector pointing "up" (0, 1 in pygame is actually down,
        # so we use rotation to point it correctly)
        # pygame.Vector2(x, y) creates a 2D vector
        # The .rotate() method rotates the vector by our rotation angle

        # "forward" points from center toward the ship's nose
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # "right" is perpendicular to forward, used to calculate
        # the bottom corners of the triangle
        # We divide by 1.5 to make the triangle not too wide
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        # Point A: The tip of the triangle (front of ship)
        # Add forward vector * radius to move from center to the tip
        a = self.position + forward * self.radius

        # Point B: Bottom-left corner
        # Move backward from center (-forward * radius) then left (-right)
        b = self.position - forward * self.radius - right

        # Point C: Bottom-right corner
        # Move backward from center (-forward * radius) then right (+right)
        c = self.position - forward * self.radius + right

        # Return all three points as a list
        return [a, b, c]

    # --------------------------------------------------------
    # METHOD: draw
    # Draw the player ship on the screen
    # --------------------------------------------------------
    def draw(self, screen):
        """
        Draw the player ship as a white triangle on the screen.

        This "overrides" the placeholder draw() method from CircleShape.
        When we call player.draw(screen), Python uses THIS version
        instead of the parent's empty version.

        Args:
            screen: The pygame surface to draw on (the game window)
        """
        # Get the three points of our triangle
        points = self.triangle()

        # pygame.draw.polygon draws a filled-in shape with straight lines
        # Parameters:
        # 1. screen - where to draw (the game window)
        # 2. "white" - the color (white)
        # 3. points - the three corner positions from triangle()
        # 4. LINE_WIDTH - how thick the outline should be
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    # --------------------------------------------------------
    # METHOD: rotate
    # Change the ship's facing direction
    # --------------------------------------------------------
    def rotate(self, dt):
        """
        Rotate the ship by a small amount based on time.

        Args:
            dt: Delta time in seconds - how long the current frame takes.
                Positive values rotate clockwise, negative rotates counter-clockwise.
        """
        # Add or subtract from the rotation angle
        # Multiply by PLAYER_TURN_SPEED to control how fast it rotates
        # Multiply by dt so rotation is smooth regardless of frame rate
        self.rotation += PLAYER_TURN_SPEED * dt

    # --------------------------------------------------------
    # METHOD: update
    # Check for key presses and update ship rotation
    # Called every frame from the game loop
    # --------------------------------------------------------
    def update(self, dt):
        """
        Check for player input and update the ship's state.

        Args:
            dt: Delta time in seconds (time since last frame)
        """
        # Decrease the shoot timer each frame (counts down over time)
        self.shoot_timer -= dt

        # pygame.key.get_pressed() returns a dictionary of all keys
        # Each key is mapped to True if it's currently held down, False otherwise
        keys = pygame.key.get_pressed()

        # Check if the A key is pressed (rotate left/counter-clockwise)
        if keys[pygame.K_a]:
            # Pass NEGATIVE dt to rotate counter-clockwise (left)
            self.rotate(-dt)

        # Check if the D key is pressed (rotate right/clockwise)
        if keys[pygame.K_d]:
            # Pass POSITIVE dt to rotate clockwise (right)
            self.rotate(dt)

        # Check if the W key is pressed (move forward)
        if keys[pygame.K_w]:
            # Pass NEGATIVE dt to move forward
            self.move(dt)

        # Check if the S key is pressed (move backward)
        if keys[pygame.K_s]:
            # Pass POSITIVE dt to move backward
            self.move(-dt)

        # Check if the Space key is pressed (shoot)
        if keys[pygame.K_SPACE]:
            # Pass SHOOT to fire
            self.shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        # If the timer is greater than 0, the weapon is still cooling down
        if self.shoot_timer > 0:
            return  # Don't shoot yet!

        # Set the timer so the player can't shoot again until it counts down
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        # Create bullet at player's position
        shot = Shot(self.position.x, self.position.y)
        # Get direction player faces
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Make it fly that way
        shot.velocity = forward * PLAYER_SHOOT_SPEED
