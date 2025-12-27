#!/bin/bash

# Start a test game
echo "Starting test game..."

# Add players
curl -s -X POST http://127.0.0.1:8888/api/add_player \
  -H "Content-Type: application/json" \
  -d '{"player_name":"Alice"}' | python3 -m json.tool

curl -s -X POST http://127.0.0.1:8888/api/add_player \
  -H "Content-Type: application/json" \
  -d '{"player_name":"Bob"}' | python3 -m json.tool

curl -s -X POST http://127.0.0.1:8888/api/add_player \
  -H "Content-Type: application/json" \
  -d '{"player_name":"Carol"}' | python3 -m json.tool

# Start game
echo -e "\nStarting game..."
curl -s -X POST http://127.0.0.1:8888/api/start_game \
  -H "Content-Type: application/json" \
  -d '{"max_cards":5}' | python3 -m json.tool

# Add a round
echo -e "\nAdding round..."
curl -s -X POST http://127.0.0.1:8888/api/add_round \
  -H "Content-Type: application/json" \
  -d '{"bids":{"Alice":1,"Bob":0,"Carol":0},"tricks":{"Alice":1,"Bob":0,"Carol":0}}' | python3 -m json.tool

# Check game state
echo -e "\nGame state:"
curl -s http://127.0.0.1:8888/api/game_state | python3 -m json.tool

