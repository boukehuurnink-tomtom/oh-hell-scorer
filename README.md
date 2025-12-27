# Oh Hell Score Recorder 🃏

A beautiful web app for tracking scores in the card game "Oh Hell" (also known as "Up and Down the River" or "Nomination Whist").

## Oh Hell Rules

### Game Overview
- **Players**: 3-7 players with a standard 52-card deck
- **Rounds**: Variable hand sizes - starts at 1 card, increases to maximum, then decreases back to 1
- **Maximum cards**: Depends on number of players (52 ÷ players - 1)

### Round Structure
Each round:
1. **Deal** the appropriate number of cards
2. **Flip** top card of remaining deck to determine **Trump Suit**
3. **Bidding Phase**: Each player bids how many tricks they'll win (0 to hand size)
   - **Important**: The DEALER bids LAST
   - **"Screw the Dealer" Rule**: Dealer CANNOT bid a number that makes total bids = total tricks
   - This ensures someone MUST fail!
4. **Playing Phase**: Standard trick-taking (must follow suit, trump wins, etc.)

### Scoring (this app's variant)
- **Made bid exactly**: Score = 5 + number of tricks bid
- **Failed bid**: Score = -(absolute difference between bid and actual)

Example: Bid 3, won 3 → +8 points | Bid 2, won 4 → -2 points

## Features Implemented

✅ **3-7 player support** with validation  
✅ **Configurable max cards** - choose max cards per hand (5, 7, 10, 12) or use default based on players  
✅ **Round progression** - automatically goes up then down  
✅ **Dealer rotation** - dealer changes each round  
✅ **"Screw the dealer" rule** - prevents total bids = total tricks  
✅ **Trump suit tracking** - record trump for each round  
✅ **Bid validation** - bids must be 0 to hand size  
✅ **Trick validation** - total tricks must equal hand size  
✅ **Auto-complete detection** - knows when game ends  
✅ **Visual dealer indicator** - highlights current dealer  
✅ **Live warnings** - alerts if dealer rule violated  
✅ **Game state persistence** - survives browser refresh (session-based)  
✅ **Undo last round** - fix mistakes by undoing and re-entering the last round

## Quick Start

1. **Install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install flask
   ```

2. **Run the app:**
   ```bash
   ./run.sh
   ```
   Or manually:
   ```bash
   source venv/bin/activate
   python3 app.py
   ```

3. **Open your browser to:** http://localhost:5000

## How to Use

1. **Setup**: Enter player names and click "Add Player" for each
2. **Choose Max Cards**: Select maximum cards per hand (optional) or use default
3. **Start Game**: Click "Start Game" when all players are added
4. **Each Round**:
   - Enter each player's bid (predicted tricks)
   - Enter actual tricks won
   - Click "Submit Round"
5. **View Scores**: Scorecard updates automatically showing all rounds and totals
6. **Fix Mistakes**: Click "Undo Last Round" to correct errors (form pre-fills with previous values)
7. **Game Persistence**: Your game is automatically saved - refresh the page anytime and continue where you left off
8. **New Game**: Click "New Game" button to start fresh (this will clear the current game)

## Example Scoring

```
Round 1:
- Alice bids 3, wins 3 → Score: 5 + 3 = 8
- Bob bids 2, wins 4 → Score: -(4 - 2) = -2

Round 2:
- Alice bids 2, wins 1 → Score: -(2 - 1) = -1 (Total: 7)
- Bob bids 3, wins 3 → Score: 5 + 3 = 8 (Total: 6)
```

## Features

✨ Beautiful, modern web interface  
📱 Mobile-friendly responsive design  
🎯 Real-time score calculation  
📊 Live scorecard with complete game history  
🎨 Color-coded positive/negative scores  
💾 Automatic game state persistence  
⏪ Undo functionality for fixing mistakes  
⚙️ Configurable max cards per hand  
🔄 Easy game reset to start new games
