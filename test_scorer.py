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
    print(f"Game starts with {game.get_current_hand_size()} card(s) per player\n")
    
    # Round 1 (1 card): Dealer is Alice. Bids can't total 1.
    game.add_round(
        bids={"Alice": 1, "Bob": 0, "Carol": 1},  # Total = 2, not 1
        tricks={"Alice": 1, "Bob": 0, "Carol": 0}
    )
    
    print("After Round 1 (1 card):")
    print(game.get_current_scores())
    # Expected: Alice=6 (5+1), Bob=5 (5+0), Carol=-1 (bid 1, won 0)
    
    # Round 2 (2 cards): Dealer is Bob. Bids can't total 2.
    game.add_round(
        bids={"Alice": 1, "Bob": 0, "Carol": 0},  # Total = 1, not 2
        tricks={"Alice": 1, "Bob": 0, "Carol": 1}
    )
    
    print("\nAfter Round 2 (2 cards):")
    print(game.get_current_scores())
    
    # Round 3 (3 cards): Dealer is Carol. Bids can't total 3.
    game.add_round(
        bids={"Alice": 1, "Bob": 1, "Carol": 0},  # Total = 2, not 3
        tricks={"Alice": 1, "Bob": 1, "Carol": 1}
    )
    
    print("\nAfter Round 3 (3 cards):")
    print(game.get_current_scores())
    # Expected: All get +11 points
    
    # Print full scorecard
    game.print_scorecard()

if __name__ == "__main__":
    test_game()
