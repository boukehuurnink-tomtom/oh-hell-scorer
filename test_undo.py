#!/usr/bin/env python3
"""
Test undo functionality
"""

from oh_hell_scorer import OhHellGame

def test_undo():
    """Test the undo feature."""
    print("Testing undo feature...\n")
    
    # Create game with 3 players, max 5 rounds
    game = OhHellGame(["Alice", "Bob", "Carol"], max_rounds=5)
    print(f"Game created with max {game.max_rounds} rounds")
    print(f"Total rounds in sequence: {len(game.round_sequence)}\n")
    
    # Add first round
    game.add_round(
        bids={"Alice": 1, "Bob": 0, "Carol": 1},
        tricks={"Alice": 1, "Bob": 0, "Carol": 0}
    )
    print("Round 1 added:")
    print(f"  Scores: {game.get_current_scores()}")
    print(f"  Current round: {game.current_round_num}")
    print(f"  Dealer: {game.get_current_dealer()}\n")
    
    # Add second round
    game.add_round(
        bids={"Alice": 1, "Bob": 0, "Carol": 0},
        tricks={"Alice": 1, "Bob": 0, "Carol": 1}
    )
    print("Round 2 added:")
    print(f"  Scores: {game.get_current_scores()}")
    print(f"  Current round: {game.current_round_num}")
    print(f"  Dealer: {game.get_current_dealer()}\n")
    
    # Undo the last round
    print("Undoing last round...")
    last_round = game.undo_last_round()
    print(f"  Undone round data: {last_round}")
    print(f"  Scores after undo: {game.get_current_scores()}")
    print(f"  Current round: {game.current_round_num}")
    print(f"  Dealer: {game.get_current_dealer()}\n")
    
    # Re-add round with corrected data
    print("Re-adding round 2 with corrected scores...")
    game.add_round(
        bids={"Alice": 0, "Bob": 1, "Carol": 0},  # Total = 1, not 2
        tricks={"Alice": 1, "Bob": 1, "Carol": 0}
    )
    print(f"  Scores: {game.get_current_scores()}")
    print(f"  Current round: {game.current_round_num}\n")
    
    print("✓ Undo test complete!")

if __name__ == "__main__":
    test_undo()
