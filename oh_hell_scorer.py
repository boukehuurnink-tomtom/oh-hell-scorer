#!/usr/bin/env python3
"""
Oh Hell Score Recorder
Tracks bids and actual tricks for the Oh Hell card game and calculates scores.
"""

class OhHellGame:
    def __init__(self, player_names, max_rounds=None):
        """Initialize a new Oh Hell game with player names and optional max rounds."""
        self.players = player_names
        self.rounds = []
        self.scores = {player: 0 for player in player_names}
        self.num_players = len(player_names)
        self.max_cards = (52 // self.num_players) - 1
        self.current_round_num = 1
        self.dealer_index = 0
        self.max_rounds = max_rounds  # User-specified maximum rounds
        self.round_sequence = self._generate_round_sequence()
    
    def _generate_round_sequence(self):
        """Generate the sequence of cards per round (up and down)."""
        ascending = list(range(1, self.max_cards + 1))
        descending = list(range(self.max_cards - 1, 0, -1))
        full_sequence = ascending + descending
        
        # Limit to max_rounds if specified
        if self.max_rounds and self.max_rounds < len(full_sequence):
            return full_sequence[:self.max_rounds]
        return full_sequence
    
    def get_current_hand_size(self):
        """Get the number of cards for the current round."""
        round_index = self.current_round_num - 1
        return self.round_sequence[round_index] if round_index < len(self.round_sequence) else None
    
    def get_current_dealer(self):
        """Get the current dealer's name."""
        return self.players[self.dealer_index]
    
    def add_round(self, bids, tricks, trump_suit=None):
        """
        Add a round with bids and actual tricks won.
        
        Args:
            bids: dict mapping player name to bid
            tricks: dict mapping player name to actual tricks won
            trump_suit: optional trump suit for the round (not used for scoring)
        """
        self._validate_players(bids, tricks)
        hand_size = self._validate_game_active()
        self._validate_bids(bids, hand_size)
        self._validate_tricks(tricks, hand_size)
        self._validate_dealer_rule(bids, hand_size)
        
        round_scores = self._calculate_round_scores(bids, tricks)
        self._record_round(hand_size, bids, tricks, round_scores)
        self._advance_to_next_round()
    
    def _validate_players(self, bids, tricks):
        """Ensure all players have bids and tricks."""
        if set(bids.keys()) != set(self.players) or set(tricks.keys()) != set(self.players):
            raise ValueError("All players must have bids and tricks")
    
    def _validate_game_active(self):
        """Check if game is still active and return current hand size."""
        hand_size = self.get_current_hand_size()
        if hand_size is None:
            raise ValueError("Game is complete")
        return hand_size
    
    def _validate_bids(self, bids, hand_size):
        """Validate that all bids are within valid range."""
        for player, bid in bids.items():
            if not 0 <= bid <= hand_size:
                raise ValueError(f"Bid for {player} must be between 0 and {hand_size}")
    
    def _validate_tricks(self, tricks, hand_size):
        """Validate that tricks are within range and sum to hand size."""
        for player, trick in tricks.items():
            if not 0 <= trick <= hand_size:
                raise ValueError(f"Tricks for {player} must be between 0 and {hand_size}")
        
        total_tricks = sum(tricks.values())
        if total_tricks != hand_size:
            raise ValueError(f"Total tricks must equal {hand_size}, got {total_tricks}")
    
    def _validate_dealer_rule(self, bids, hand_size):
        """Check 'screw the dealer' rule - total bids cannot equal hand size."""
        total_bids = sum(bids.values())
        if total_bids == hand_size:
            dealer = self.get_current_dealer()
            raise ValueError(f"Invalid: Total bids cannot equal {hand_size} (Dealer {dealer} must bid differently)")
    
    def _calculate_round_scores(self, bids, tricks):
        """Calculate scores for all players in the round."""
        round_scores = {}
        for player in self.players:
            bid = bids[player]
            actual = tricks[player]
            round_scores[player] = self._calculate_player_score(bid, actual)
            self.scores[player] += round_scores[player]
        return round_scores
    
    @staticmethod
    def _calculate_player_score(bid, actual):
        """Calculate score for a single player: 5 + actual if correct, -difference otherwise."""
        return 5 + actual if bid == actual else -abs(bid - actual)
    
    def _record_round(self, hand_size, bids, tricks, round_scores):
        """Record the round data."""
        self.rounds.append({
            'round_num': self.current_round_num,
            'hand_size': hand_size,
            'dealer': self.get_current_dealer(),
            'bids': bids.copy(),
            'tricks': tricks.copy(),
            'round_scores': round_scores
        })
    
    def _advance_to_next_round(self):
        """Move to the next round and rotate dealer."""
        self.current_round_num += 1
        self.dealer_index = (self.dealer_index + 1) % self.num_players
    
    def undo_last_round(self):
        """Undo the last round and restore previous state."""
        if not self.rounds:
            raise ValueError("No rounds to undo")
        
        # Get the last round
        last_round = self.rounds.pop()
        
        # Revert scores
        for player in self.players:
            self.scores[player] -= last_round['round_scores'][player]
        
        # Go back one round
        self.current_round_num -= 1
        
        # Rotate dealer backwards
        self.dealer_index = (self.dealer_index - 1) % self.num_players
        
        return last_round  # Return the undone round for potential re-editing
    
    def get_current_scores(self):
        """Return current cumulative scores."""
        return self.scores.copy()
    
    def print_scorecard(self):
        """Print a formatted scorecard."""
        self._print_header()
        self._print_rounds()
        self._print_final_scores()
    
    def _print_header(self):
        """Print scorecard header."""
        print("\n" + "=" * 80)
        print("OH HELL SCORECARD")
        print("=" * 80)
        print(f"{'Round':<8}" + "".join(f"{p:<15}" for p in self.players))
        print("-" * 80)
    
    def _print_rounds(self):
        """Print all rounds with bids, tricks, and scores."""
        for i, round_data in enumerate(self.rounds, 1):
            self._print_round(i, round_data)
    
    def _print_round(self, round_num, round_data):
        """Print a single round's data."""
        print(f"R{round_num} Bid:  " + "".join(f"{round_data['bids'][p]:<15}" for p in self.players))
        print(f"R{round_num} Won:  " + "".join(f"{round_data['tricks'][p]:<15}" for p in self.players))
        print(f"R{round_num} Pts:  " + "".join(f"{round_data['round_scores'][p]:+<15}" for p in self.players))
        
        running_totals = self._calculate_running_totals(round_num)
        print(f"Total:    " + "".join(f"{running_totals[p]:<15}" for p in self.players))
        print("-" * 80)
    
    def _calculate_running_totals(self, up_to_round):
        """Calculate running totals up to a specific round."""
        return {
            player: sum(self.rounds[j]['round_scores'][player] for j in range(up_to_round))
            for player in self.players
        }
    
    def _print_final_scores(self):
        """Print final scores."""
        print(f"\n{'FINAL SCORES':<8}")
        for player in self.players:
            print(f"{player}: {self.scores[player]}")
        print("=" * 80 + "\n")


def main():
    """Interactive Oh Hell score recorder."""
    print("Welcome to Oh Hell Score Recorder!")
    print("="*80)
    
    # Get player names
    num_players = int(input("\nHow many players? "))
    players = []
    for i in range(num_players):
        name = input(f"Player {i+1} name: ").strip()
        players.append(name)
    
    game = OhHellGame(players)
    
    print(f"\nStarting game with players: {', '.join(players)}")
    print("\nEnter bids and tricks for each round. Type 'done' when finished.")
    
    round_num = 1
    while True:
        print(f"\n--- Round {round_num} ---")
        
        # Check if user wants to finish
        continue_game = input("Enter round data? (y/n or 'score' to see scorecard): ").strip().lower()
        if continue_game == 'n' or continue_game == 'done':
            break
        elif continue_game == 'score' or continue_game == 's':
            game.print_scorecard()
            continue
        
        # Get bids
        print("\nEnter bids:")
        bids = {}
        for player in players:
            bid = int(input(f"  {player}'s bid: "))
            bids[player] = bid
        
        # Get tricks
        print("\nEnter actual tricks won:")
        tricks = {}
        for player in players:
            actual = int(input(f"  {player} won: "))
            tricks[player] = actual
        
        # Add round and show current scores
        game.add_round(bids, tricks)
        print("\nCurrent scores:")
        for player, score in game.get_current_scores().items():
            print(f"  {player}: {score}")
        
        round_num += 1
    
    # Final scorecard
    game.print_scorecard()


if __name__ == "__main__":
    main()
