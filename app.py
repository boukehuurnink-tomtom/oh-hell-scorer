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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/new_game', methods=['POST'])
def new_game():
    data = request.json
    players = data.get('players', [])
    
    if len(players) < 3:
        return jsonify({'error': 'Need at least 3 players for Oh Hell'}), 400
    
    if len(players) > 7:
        return jsonify({'error': 'Maximum 7 players for Oh Hell'}), 400
    
    game_id = secrets.token_hex(8)
    games[game_id] = OhHellGame(players)
    session['game_id'] = game_id
    
    game = games[game_id]
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
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({'error': 'No active game'}), 400
    
    data = request.json
    bids = data.get('bids', {})
    tricks = data.get('tricks', {})
    
    try:
        games[game_id].add_round(bids, tricks)
        game = games[game_id]
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
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({'error': 'No active game'}), 400
    
    game = games[game_id]
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

@app.route('/api/reset', methods=['POST'])
def reset():
    game_id = session.get('game_id')
    if game_id and game_id in games:
        del games[game_id]
    session.pop('game_id', None)
    return jsonify({'success': True})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Oh Hell Score Recorder")
    print("="*60)
    print("\nStarting web server...")
    print("Open your browser to: http://127.0.0.1:8888")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    app.run(debug=False, host='127.0.0.1', port=8888)
