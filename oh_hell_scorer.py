#!/usr/bin/env python3
"""
Oh Hell Score Recorder
Tracks bids and actual tricks for the Oh Hell card game and calculates scores.
"""

class OhHellGame:
    def __init__(self, player_names):
        """Initialize a new Oh Hell game with player names."""
        self.players = player_names
        self.rounds = []
        self.scores = {player: 0 for player in player_names}
        self.num_players = len(player_names)
        self.max_cards = (52 // self.num_players) - 1
        self.current_round_num = 1
        self.dealer_index = 0
        self.round_sequence = self._generate_round_sequence()
    
    def _generate_round_sequence(self):
        """Generate the sequence of cards per round (up and down)."""
        sequence = list(range(1, self.max_cards + 1))
        sequence.extend(range(self.max_cards - 1, 0, -1))
        return sequence
    
    def get_current_hand_size(self):
        """Get the number of cards for the current round."""
        if self.current_round_num - 1 < len(self.round_sequence):
            return self.round_sequence[self.current_round_num - 1]
        return None
    
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
        if set(bids.keys()) != set(self.players) or set(tricks.keys()) != set(self.players):
            raise ValueError("All players must have bids and tricks")
        
        hand_size = self.get_current_hand_size()
        if hand_size is None:
            raise ValueError("Game is complete")
        
        # Validate bids
        for player, bid in bids.items():
            if bid < 0 or bid > hand_size:
                raise ValueError(f"Bid for {player} must be between 0 and {hand_size}")
        
        # Validate tricks
        for player, trick in tricks.items():
            if trick < 0 or trick > hand_size:
                raise ValueError(f"Tricks for {player} must be between 0 and {hand_size}")
        
        # Validate total tricks equals hand size
        if sum(tricks.values()) != hand_size:
            raise ValueError(f"Total tricks must equal {hand_size}, got {sum(tricks.values())}")
        
        # Check "screw the dealer" rule
        dealer = self.get_current_dealer()
        total_bids = sum(bids.values())
        if total_bids == hand_size:
            raise ValueError(f"Invalid: Total bids cannot equal {hand_size} (Dealer {dealer} must bid differently)")
        
        round_scores = {}
        for player in self.players:
            bid = bids[player]
            actual = tricks[player]
            
            # Calculate score: if bid matches actual, score = 10 + actual
            # Otherwise, score = -(absolute difference)
            if bid == actual:
                score = 10 + actual
            else:
                score = -abs(bid - actual)
            
            round_scores[player] = score
            self.scores[player] += score
        
        self.rounds.append({
            'round_num': self.current_round_num,
            'hand_size': hand_size,
            'dealer': dealer,
            'bids': bids.copy(),
            'tricks': tricks.copy(),
            'round_scores': round_scores
        })
        
        # Move to next round
        self.current_round_num += 1
        self.dealer_index = (self.dealer_index + 1) % self.num_players
    
    def get_current_scores(self):
        """Return current cumulative scores."""
        return self.scores.copy()
    
    def print_scorecard(self):
        """Print a formatted scorecard."""
        print("\n" + "="*80)
        print("OH HELL SCORECARD")
        print("="*80)
        
        # Header
        header = f"{'Round':<8}"
        for player in self.players:
            header += f"{player:<15}"
        print(header)
        print("-"*80)
        
        # Each round
        for i, round_data in enumerate(self.rounds, 1):
            # Bid row
            bid_row = f"R{i} Bid:  "
            for player in self.players:
                bid_row += f"{round_data['bids'][player]:<15}"
            print(bid_row)
            
            # Tricks row
            tricks_row = f"R{i} Won:  "
            for player in self.players:
                tricks_row += f"{round_data['tricks'][player]:<15}"
            print(tricks_row)
            
            # Score row
            score_row = f"R{i} Pts:  "
            for player in self.players:
                score = round_data['round_scores'][player]
                score_row += f"{score:+<15}"
            print(score_row)
            
            # Cumulative after this round
            cumulative_row = f"Total:    "
            running_totals = {p: 0 for p in self.players}
            for j in range(i):
                for player in self.players:
                    running_totals[player] += self.rounds[j]['round_scores'][player]
            
            for player in self.players:
                cumulative_row += f"{running_totals[player]:<15}"
            print(cumulative_row)
            print("-"*80)
        
        # Final scores
        print(f"\n{'FINAL SCORES':<8}")
        for player in self.players:
            print(f"{player}: {self.scores[player]}")
        print("="*80 + "\n")


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
