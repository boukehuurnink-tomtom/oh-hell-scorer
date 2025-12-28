"""
Game State Persistence Module
Stores active game state to survive app restarts
"""
import json
import os
from typing import Dict, Any

GAME_STATE_FILE = 'current_game.json'

def save_game_state(game_data: Dict[str, Any]) -> None:
    """Save current game state to file."""
    try:
        with open(GAME_STATE_FILE, 'w') as f:
            json.dump(game_data, f, indent=2)
    except IOError as e:
        print(f"Error saving game state: {e}")

def load_game_state() -> Dict[str, Any] | None:
    """Load current game state from file."""
    if not os.path.exists(GAME_STATE_FILE):
        return None
    
    try:
        with open(GAME_STATE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading game state: {e}")
        return None

def clear_game_state() -> None:
    """Clear the current game state file."""
    try:
        if os.path.exists(GAME_STATE_FILE):
            os.remove(GAME_STATE_FILE)
    except IOError as e:
        print(f"Error clearing game state: {e}")
