#!/usr/bin/env python3
"""
Oh Hell Score Recorder - Web App
"""

from flask import Flask, render_template, request, jsonify, session
import secrets
from oh_hell_scorer import OhHellGame
import game_history
import game_state

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store games in memory (in production, use a database)
games = {}

MIN_PLAYERS = 3
MAX_PLAYERS = 7

# Load persisted game on startup
def load_persisted_game():
    """Load game state from disk on app startup."""
    saved_state = game_state.load_game_state()
    if saved_state:
        game_id = saved_state.get('game_id')
        if game_id:
            # Recreate the game object
            game = OhHellGame(saved_state['players'], saved_state.get('max_cards'))
            # Restore rounds
            for round_data in saved_state.get('rounds', []):
                game.add_round(round_data['bids'], round_data['tricks'])
            games[game_id] = game
            print(f"Restored game {game_id} with {len(saved_state.get('rounds', []))} rounds")

# Load on startup
load_persisted_game()


@app.route('/')
def index():
    """Render the main game page."""
    return render_template('index.html')


@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Create a new game with the specified players."""
    players = request.json.get('players', [])
    max_cards = request.json.get('max_cards', None)
    
    if error := _validate_player_count(players):
        return jsonify({'error': error}), 400
    
    game_id = _create_game(players, max_cards)
    game = games[game_id]
    
    # Save initial game state
    _save_current_game_state(game_id, game)
    
    return jsonify({
        'game_id': game_id,
        'players': players,
        'max_cards': game.max_cards,
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
        game_complete = hand_size is None
        
        # Save game state after each round
        game_id = session.get('game_id')
        if game_id and not game_complete:
            _save_current_game_state(game_id, game)
        
        # If game is complete, save to history and clear current state
        if game_complete:
            game_data = {
                'players': game.players,
                'scores': game.get_current_scores(),
                'rounds': game.rounds,
                'max_cards': game.max_cards
            }
            history_id = game_history.save_completed_game(game_data)
            game_state.clear_game_state()
        
        return jsonify({
            'success': True,
            'scores': game.get_current_scores(),
            'rounds': game.rounds,
            'hand_size': hand_size,
            'dealer': game.get_current_dealer() if hand_size else None,
            'game_complete': game_complete
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/game_state', methods=['GET'])
def get_game_state():
    """Get the current state of the active game."""
    # First check if there's a game in memory
    game_id = session.get('game_id')
    
    # If no game in session, try to restore from disk
    if not game_id or game_id not in games:
        saved_state = game_state.load_game_state()
        if saved_state:
            game_id = saved_state.get('game_id')
            # Recreate the game object if not in memory
            if game_id and game_id not in games:
                game = OhHellGame(saved_state['players'], saved_state.get('max_cards'))
                # Restore rounds
                for round_data in saved_state.get('rounds', []):
                    game.add_round(round_data['bids'], round_data['tricks'])
                games[game_id] = game
                session['game_id'] = game_id
    
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
        
        # Save game state after undo
        game_id = session.get('game_id')
        if game_id:
            _save_current_game_state(game_id, game)
        
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
    # Clear persisted game state
    game_state.clear_game_state()
    return jsonify({'success': True})


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get list of completed games."""
    history = game_history.load_game_history()
    return jsonify({'games': history})


@app.route('/api/history/<game_id>', methods=['GET'])
def get_history_game(game_id):
    """Get a specific game from history."""
    game = game_history.get_game_by_id(game_id)
    if game:
        return jsonify(game)
    return jsonify({'error': 'Game not found'}), 404


@app.route('/api/history/<game_id>', methods=['DELETE'])
def delete_history_game(game_id):
    """Delete a game from history."""
    if game_history.delete_game(game_id):
        return jsonify({'success': True})
    return jsonify({'error': 'Game not found'}), 404


def _validate_player_count(players):
    """Validate that player count is within acceptable range."""
    if len(players) < MIN_PLAYERS:
        return f'Need at least {MIN_PLAYERS} players for Oh Hell'
    if len(players) > MAX_PLAYERS:
        return f'Maximum {MAX_PLAYERS} players for Oh Hell'
    return None


def _create_game(players, max_cards=None):
    """Create a new game and store it in the session."""
    game_id = secrets.token_hex(8)
    games[game_id] = OhHellGame(players, max_cards)
    session['game_id'] = game_id
    return game_id


def _get_current_game():
    """Retrieve the current game from the session or return error."""
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({'error': 'No active game'}), 400
    return games[game_id]


def _save_current_game_state(game_id, game):
    """Save the current game state to disk."""
    state_data = {
        'game_id': game_id,
        'players': game.players,
        'max_cards': game.max_cards,
        'rounds': game.rounds
    }
    game_state.save_game_state(state_data)


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
