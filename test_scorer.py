#!/usr/bin/env python3
"""
Simple test/demo of the Oh Hell scorer
"""

from oh_hell_scorer import OhHellGame

def test_game():
    """Run a simple test game."""
    print("Running test game...\n")
    
    # Create game with 3 players
    game = OhHellGame(["Alice", "Bob", "Carol"])
    
    # Round 1: Alice nails it, Bob and Carol miss
    game.add_round(
        bids={"Alice": 3, "Bob": 2, "Carol": 1},
        tricks={"Alice": 3, "Bob": 4, "Carol": 0}
    )
    
    print("After Round 1:")
    print(game.get_current_scores())
    # Expected: Alice=13 (10+3), Bob=-2 (off by 2), Carol=-1 (off by 1)
    
    # Round 2: Bob nails it, others miss
    game.add_round(
        bids={"Alice": 2, "Bob": 3, "Carol": 2},
        tricks={"Alice": 1, "Bob": 3, "Carol": 3}
    )
    
    print("\nAfter Round 2:")
    print(game.get_current_scores())
    # Expected: Alice=12 (13-1), Bob=11 (-2+13), Carol=-2 (-1-1)
    
    # Round 3: Everyone nails it!
    game.add_round(
        bids={"Alice": 4, "Bob": 2, "Carol": 1},
        tricks={"Alice": 4, "Bob": 2, "Carol": 1}
    )
    
    print("\nAfter Round 3:")
    print(game.get_current_scores())
    # Expected: Alice=26 (12+14), Bob=23 (11+12), Carol=9 (-2+11)
    
    # Print full scorecard
    game.print_scorecard()

if __name__ == "__main__":
    test_game()
