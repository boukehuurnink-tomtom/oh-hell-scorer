# Oh Hell - Complete Game Rules

## Overview
Oh Hell (also called "Up and Down the River" or "Nomination Whist") is a trick-taking card game for 3-7 players.

## Setup
- **Deck**: Standard 52-card deck
- **Players**: 3-7 (optimal with 4-5 players)
- **Objective**: Score points by accurately bidding the number of tricks you'll win

## Game Structure

### Number of Rounds
The game consists of multiple rounds with increasing then decreasing hand sizes:
- Start with 1 card per player
- Increase by 1 each round up to maximum
- Maximum = (52 ÷ number of players) - 1
- Then decrease back down to 1 card

Example with 4 players:
- Max cards = (52 ÷ 4) - 1 = 12
- Rounds: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1
- Total: 23 rounds

### Each Round

1. **Deal Cards**
   - Dealer gives each player the appropriate number of cards
   - Dealer rotates clockwise each round

2. **Determine Trump**
   - Flip the top card of the remaining deck face-up
   - Its suit becomes the Trump suit for this round
   - If all cards are dealt (rare), play with no trump

3. **Bidding Phase**
   - Starting left of dealer, each player bids how many tricks they expect to win
   - Bids can be from 0 (zero) to the number of cards dealt
   - **DEALER BIDS LAST**
   - **"Screw the Dealer" Rule**: The dealer CANNOT bid a number that would make the total of all bids equal the number of tricks available
     - Example: 4-card round, first 3 players bid 2, 1, 0 (total = 3)
     - Dealer CANNOT bid 1 (which would make total = 4 cards)
     - This ensures at least one player MUST fail their bid

4. **Playing Phase**
   - Player left of dealer leads first trick
   - Standard trick-taking rules:
     - Must follow suit if able
     - If can't follow suit, may play any card (including trump)
     - Highest card of led suit wins UNLESS trump was played
     - Highest trump card wins the trick
   - Winner of each trick leads the next trick

5. **Scoring**
   - **Made Bid Exactly**: 5 + (number of tricks bid)
     - Bid 0, won 0: 5 points
     - Bid 3, won 3: 8 points
   - **Failed Bid**: -(absolute difference)
     - Bid 2, won 4: -2 points
     - Bid 3, won 0: -3 points

## Strategy Tips
- Early rounds (1-2 cards): Very unpredictable
- Middle rounds: Easier to control your tricks
- Bidding zero can be strategic but risky
- As dealer, calculate what you CAN'T bid before bidding
- Trump cards are powerful but limited

## Winning
Player with the highest total score after all rounds wins!

## Variations

### Scoring Variations
1. **This app uses**: Made = 5 + bid, Failed = -difference
2. **Alternative**: Made = 10 + bid, Failed = -difference
3. **Another variant**: Made = 10 + (bid × 2), Failed = 0
4. **British variant**: Made = (bid × 2) + 10, Failed = -5

### Rule Variations
1. **No "screw the dealer"**: Dealer can bid anything
2. **Fixed rounds**: Play only ascending OR descending, not both
3. **Exact 52 deal**: Calculate rounds so last round uses all 52 cards
4. **Blind bidding**: All players bid simultaneously

This app implements the standard rules with "screw the dealer" and the most common scoring system.
