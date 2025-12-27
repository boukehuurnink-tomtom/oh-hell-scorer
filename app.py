#!/usr/bin/env python3
"""
Oh Hell Score Recorder - Web App
"""

from flask import Flask, render_template, request, jsonify, session
import secrets
from oh_hell_scorer import OhHellGame

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store games in memory (in production, use a database)
games = {}

MIN_PLAYERS = 3
MAX_PLAYERS = 7


@app.route('/')
def index():
    """Render the main game page."""
    return render_template('index.html')


@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Create a new game with the specified players."""
    players = request.json.get('players', [])
    max_rounds = request.json.get('max_rounds', None)
    
    if error := _validate_player_count(players):
        return jsonify({'error': error}), 400
    
    game_id = _create_game(players, max_rounds)
    game = games[game_id]
    
    return jsonify({
        'game_id': game_id,
        'players': players,
        'max_cards': game.max_cards,
        'max_rounds': game.max_rounds,
        'total_rounds': len(game.round_sequence),
        'hand_size': game.get_current_hand_size(),
        'dealer': game.get_current_dealer()
    })


@app.route('/api/add_round', methods=['POST'])
def add_round():
    """Add a completed round to the current game."""
    game = _get_current_game()
    if isinstance(game, tuple):  # Error response
        return game
    
    data = request.json
    bids = data.get('bids', {})
    tricks = data.get('tricks', {})
    
    try:
        game.add_round(bids, tricks)
        hand_size = game.get_current_hand_size()
        
        return jsonify({
            'success': True,
            'scores': game.get_current_scores(),
            'rounds': game.rounds,
            'hand_size': hand_size,
            'dealer': game.get_current_dealer() if hand_size else None,
            'game_complete': hand_size is None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/game_state', methods=['GET'])
def game_state():
    """Get the current state of the active game."""
    game = _get_current_game()
    if isinstance(game, tuple):  # Error response
        return game
    
    hand_size = game.get_current_hand_size()
    
    return jsonify({
        'players': game.players,
        'scores': game.get_current_scores(),
        'rounds': game.rounds,
        'current_round': game.current_round_num,
        'hand_size': hand_size,
        'dealer': game.get_current_dealer() if hand_size else None,
        'max_cards': game.max_cards,
        'max_rounds': game.max_rounds,
        'total_rounds': len(game.round_sequence),
        'game_complete': hand_size is None
    })


@app.route('/api/undo_round', methods=['POST'])
def undo_round():
    """Undo the last round."""
    game = _get_current_game()
    if isinstance(game, tuple):  # Error response
        return game
    
    try:
        last_round = game.undo_last_round()
        hand_size = game.get_current_hand_size()
        
        return jsonify({
            'success': True,
            'last_round': last_round,
            'scores': game.get_current_scores(),
            'rounds': game.rounds,
            'hand_size': hand_size,
            'dealer': game.get_current_dealer() if hand_size else None,
            'current_round': game.current_round_num
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset the current game."""
    game_id = session.get('game_id')
    if game_id and game_id in games:
        del games[game_id]
    session.pop('game_id', None)
    return jsonify({'success': True})


def _validate_player_count(players):
    """Validate that player count is within acceptable range."""
    if len(players) < MIN_PLAYERS:
        return f'Need at least {MIN_PLAYERS} players for Oh Hell'
    if len(players) > MAX_PLAYERS:
        return f'Maximum {MAX_PLAYERS} players for Oh Hell'
    return None


def _create_game(players, max_rounds=None):
    """Create a new game and store it in the session."""
    game_id = secrets.token_hex(8)
    games[game_id] = OhHellGame(players, max_rounds)
    session['game_id'] = game_id
    return game_id


def _get_current_game():
    """Retrieve the current game from the session or return error."""
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({'error': 'No active game'}), 400
    return games[game_id]


def _print_startup_message():
    """Print server startup information."""
    print("\n" + "=" * 60)
    print("Oh Hell Score Recorder")
    print("=" * 60)
    print("\nStarting web server...")
    print("Open your browser to: http://127.0.0.1:8888")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    _print_startup_message()
    app.run(debug=False, host='127.0.0.1', port=8888)
