# ============================================================
# LOGGER.PY - Game State and Event Tracking
# ============================================================
#
# This file provides two functions that record what happens
# during gameplay to JSONL files (one JSON object per line).
#
# - log_state(): Records a snapshot of all game objects ~once/second
# - log_event(): Records specific events (hits, splits, etc.)
#
# These logs are used for debugging, replay analysis, and grading.
# ============================================================

# Import inspect to access the caller's local variables
import inspect

# Import json to serialize game data
import json

# Import math for rounding time values
import math

# Import datetime to track when things happen
from datetime import datetime

# Make these two functions available when other files do: from logger import *
__all__ = ["log_state", "log_event"]

# --------------------------------------------------------
# Internal Configuration
# --------------------------------------------------------

# How many frames per second the game runs at
_FPS = 60

# Stop logging after this many seconds (saves disk space)
_MAX_SECONDS = 16

# Maximum number of sprites to log per group (prevents huge log files)
_SPRITE_SAMPLE_LIMIT = 10

# --------------------------------------------------------
# Internal State (tracks logging progress)
# --------------------------------------------------------

# Counts how many frames have passed
_frame_count = 0

# Flags to track whether each log file has been created yet
_state_log_initialized = False
_event_log_initialized = False

# Records when the game started (used to calculate elapsed time)
_start_time = datetime.now()


# ============================================================
# FUNCTION: log_state
# Records a snapshot of all game objects to game_state.jsonl
# Called every frame, but only writes ~once per second
# ============================================================
def log_state():
    """
    Record the current state of all game objects (position, velocity, etc.)
    to a file. Writes approximately once per second for the first 16 seconds.
    """
    global _frame_count, _state_log_initialized

    # Stop logging after _MAX_SECONDS to avoid filling up disk space
    if _frame_count > _FPS * _MAX_SECONDS:
        return

    # Count this frame
    _frame_count += 1
    # Only write once per second (every _FPS frames)
    if _frame_count % _FPS != 0:
        return

    # Record the current time
    now = datetime.now()

    # Get the local variables from the function that called us (main.py's main())
    # This lets us find game objects without them being passed as parameters
    frame = inspect.currentframe()
    if frame is None:
        return

    frame_back = frame.f_back
    if frame_back is None:
        return

    local_vars = frame_back.f_locals.copy()

    screen_size = []
    game_state = {}

    # Look through all local variables for game-relevant data
    for key, value in local_vars.items():
        # Check if this is the pygame screen (has get_size method)
        if "pygame" in str(type(value)) and hasattr(value, "get_size"):
            screen_size = value.get_size()

        # Check if this is a pygame sprite Group (holds game objects)
        if hasattr(value, "__class__") and "Group" in value.__class__.__name__:
            sprites_data = []

            # Loop through each sprite in the group (up to the sample limit)
            for i, sprite in enumerate(value):
                if i >= _SPRITE_SAMPLE_LIMIT:
                    break

                sprite_info = {"type": sprite.__class__.__name__}

                # Record position if the sprite has one
                if hasattr(sprite, "position"):
                    sprite_info["pos"] = [
                        round(sprite.position.x, 2),
                        round(sprite.position.y, 2),
                    ]

                # Record velocity if the sprite has one
                if hasattr(sprite, "velocity"):
                    sprite_info["vel"] = [
                        round(sprite.velocity.x, 2),
                        round(sprite.velocity.y, 2),
                    ]

                # Record radius (size) if the sprite has one
                if hasattr(sprite, "radius"):
                    sprite_info["rad"] = sprite.radius

                # Record rotation angle if the sprite has one
                if hasattr(sprite, "rotation"):
                    sprite_info["rot"] = round(sprite.rotation, 2)

                sprites_data.append(sprite_info)

            game_state[key] = {"count": len(value), "sprites": sprites_data}

        # Also handle individual sprite objects (not in groups)
        if len(game_state) == 0 and hasattr(value, "position"):
            sprite_info = {"type": value.__class__.__name__}

            sprite_info["pos"] = [
                round(value.position.x, 2),
                round(value.position.y, 2),
            ]

            if hasattr(value, "velocity"):
                sprite_info["vel"] = [
                    round(value.velocity.x, 2),
                    round(value.velocity.y, 2),
                ]

            if hasattr(value, "radius"):
                sprite_info["rad"] = value.radius

            if hasattr(value, "rotation"):
                sprite_info["rot"] = round(value.rotation, 2)

            game_state[key] = sprite_info

    # Build the log entry with timestamp and game data
    entry = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "screen_size": screen_size,
        **game_state,
    }

    # Write to file: create new file on first call, append after that
    mode = "w" if not _state_log_initialized else "a"
    with open("game_state.jsonl", mode) as f:
        f.write(json.dumps(entry) + "\n")

    _state_log_initialized = True


# ============================================================
# FUNCTION: log_event
# Records a specific game event to game_events.jsonl
# ============================================================
def log_event(event_type, **details):
    """
    Record a specific game event (like "player_hit" or "asteroid_split")
    to a file with a timestamp.

    Args:
        event_type: A string describing what happened (e.g., "asteroid_shot")
        **details: Any extra information about the event
    """
    global _event_log_initialized

    now = datetime.now()

    # Build the event record with timestamp and event info
    event = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "type": event_type,
        **details,
    }

    # Write to file: create new file on first call, append after that
    mode = "w" if not _event_log_initialized else "a"
    with open("game_events.jsonl", mode) as f:
        f.write(json.dumps(event) + "\n")

    _event_log_initialized = True
