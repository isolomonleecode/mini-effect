# ============================================================
# ASTEROIDFIELD.PY - Automatic Asteroid Spawner
# ============================================================
#
# This file contains the AsteroidField class, which automatically
# spawns new asteroids at random edges of the screen at regular
# intervals. Think of it as an "asteroid factory" that keeps the
# game challenging by constantly adding new threats!
#
# KEY CONCEPT: Timers and Random Selection
# The AsteroidField uses a timer to decide WHEN to spawn, and
# random selection to decide WHERE and HOW asteroids appear.
# ============================================================

# --------------------------------------------------------
# IMPORTS - Load the tools we need
# --------------------------------------------------------

# Import pygame for sprite and vector features
import pygame

# Import random for generating random values (position, speed, size)
import random

# Import the Asteroid class so we can create new asteroids
from asteroid import Asteroid

# Import all game constants (screen size, spawn rate, etc.)
from constants import *


# ============================================================
# CLASS: AsteroidField
# A hidden manager that spawns asteroids at screen edges
# ============================================================
class AsteroidField(pygame.sprite.Sprite):
    """
    Automatically spawns asteroids at random screen edges.

    This sprite doesn't draw anything — it's invisible!
    Its only job is to create new asteroids on a timer.
    """

    # --------------------------------------------------------
    # CLASS ATTRIBUTE: edges
    # Defines the four screen edges where asteroids can spawn
    # --------------------------------------------------------
    # Each edge is a pair of:
    #   [0] A direction vector (which way the asteroid will face)
    #   [1] A function that calculates the spawn position along that edge
    edges = [
        # LEFT EDGE: asteroids face right (1, 0)
        # Spawn position: x = just off-screen left, y = random vertical position
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        # RIGHT EDGE: asteroids face left (-1, 0)
        # Spawn position: x = just off-screen right, y = random vertical position
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        # TOP EDGE: asteroids face down (0, 1)
        # Spawn position: x = random horizontal position, y = just off-screen top
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        # BOTTOM EDGE: asteroids face up (0, -1)
        # Spawn position: x = random horizontal position, y = just off-screen bottom
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    # --------------------------------------------------------
    # METHOD: __init__ (Constructor)
    # Set up the asteroid field when the game starts
    # --------------------------------------------------------
    def __init__(self):
        """
        Initialize the AsteroidField.
        Sets up the spawn timer to 0 so asteroids start spawning immediately.
        """
        # Register this sprite with its containers (set up in main.py)
        pygame.sprite.Sprite.__init__(self, self.containers)
        # Timer that counts up to decide when to spawn the next asteroid
        self.spawn_timer = 0.0

    # --------------------------------------------------------
    # METHOD: spawn
    # Create a single asteroid with given properties
    # --------------------------------------------------------
    def spawn(self, radius, position, velocity):
        """
        Create a new asteroid at the given position with the given size and speed.

        Args:
            radius: How big the asteroid should be
            position: Where to place it (a pygame.Vector2)
            velocity: How fast and which direction it should move
        """
        # Create the asteroid at the specified position and size
        asteroid = Asteroid(position.x, position.y, radius)
        # Set its velocity so it starts moving
        asteroid.velocity = velocity

    # --------------------------------------------------------
    # METHOD: update
    # Called every frame — checks if it's time to spawn a new asteroid
    # --------------------------------------------------------
    def update(self, dt):
        """
        Check if enough time has passed to spawn a new asteroid.

        Args:
            dt: Delta time in seconds (time since last frame)
        """
        # Count up the timer each frame
        self.spawn_timer += dt

        # Has enough time passed since the last spawn?
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            # Reset the timer so we start counting to the next spawn
            self.spawn_timer = 0

            # --- Pick a random screen edge to spawn from ---
            edge = random.choice(self.edges)

            # --- Pick a random speed between 40 and 100 ---
            speed = random.randint(40, 100)

            # --- Create the velocity: direction * speed ---
            velocity = edge[0] * speed
            # Add a random wobble (-30 to +30 degrees) so they don't fly straight
            velocity = velocity.rotate(random.randint(-30, 30))

            # --- Calculate the spawn position along the chosen edge ---
            # random.uniform(0, 1) gives a random spot along the edge
            position = edge[1](random.uniform(0, 1))

            # --- Pick a random asteroid size (1x, 2x, or 3x the minimum) ---
            kind = random.randint(1, ASTEROID_KINDS)

            # --- Actually create the asteroid! ---
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
