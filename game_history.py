"""
Game History Storage Module
Stores completed games for later retrieval
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any

HISTORY_FILE = 'game_history.json'

def save_completed_game(game_data: Dict[str, Any]) -> str:
    """Save a completed game to history."""
    history = load_game_history()
    
    # Add metadata
    game_record = {
        'id': datetime.now().isoformat(),
        'completed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'players': game_data['players'],
        'final_scores': game_data['scores'],
        'rounds': game_data['rounds'],
        'max_cards': game_data.get('max_cards'),
        'total_rounds': len(game_data['rounds']),
        'winner': _get_winner(game_data['scores'])
    }
    
    history.insert(0, game_record)  # Most recent first
    
    # Keep last 100 games
    history = history[:100]
    
    _save_history(history)
    return game_record['id']

def load_game_history() -> List[Dict[str, Any]]:
    """Load all game history."""
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def get_game_by_id(game_id: str) -> Dict[str, Any] | None:
    """Get a specific game from history."""
    history = load_game_history()
    for game in history:
        if game['id'] == game_id:
            return game
    return None

def delete_game(game_id: str) -> bool:
    """Delete a game from history."""
    history = load_game_history()
    original_length = len(history)
    history = [g for g in history if g['id'] != game_id]
    
    if len(history) < original_length:
        _save_history(history)
        return True
    return False

def _get_winner(scores: Dict[str, int]) -> str:
    """Determine the winner (highest score)."""
    if not scores:
        return "Unknown"
    return max(scores.items(), key=lambda x: x[1])[0]

def _save_history(history: List[Dict[str, Any]]):
    """Save history to file."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)
