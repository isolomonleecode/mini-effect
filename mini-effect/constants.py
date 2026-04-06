# ============================================================
# CONSTANTS.PY - Game Configuration Values
# ============================================================
#
# This file stores values that stay the same throughout the game.
# We call these "constants" because they never change while the
# game is running.
#
# By putting them here, we can easily change them in one place
# instead of hunting through multiple files!
# ============================================================

# The width of the game window in pixels
# Think of it like the horizontal size of your TV screen
SCREEN_WIDTH = 1280

# The height of the game window in pixels
# Think of it like the vertical size of your TV screen
SCREEN_HEIGHT = 720

# The radius (size) of the player's spaceship
# We use this to determine how big the hitbox is and how big to draw the ship
# A radius of 20 means the ship is 40 pixels wide total (20 on each side)
PLAYER_RADIUS = 20

# The thickness of the lines that draw the player ship
# Higher number = thicker lines
LINE_WIDTH = 2

# The player's turn speed'
PLAYER_TURN_SPEED = 300

# The player's speed
PLAYER_SPEED = 200


ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500

PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3
