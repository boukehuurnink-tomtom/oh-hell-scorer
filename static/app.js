let players = [];
let currentRound = 1;
let handSize = 0;
let dealer = '';
let totalRounds = 0;
let maxCards = 0;

// Setup Screen Functions
function addPlayer() {
    const input = document.getElementById('player-name-input');
    const name = input.value.trim();
    
    if (name && !players.includes(name)) {
        if (players.length >= 7) {
            alert('Maximum 7 players allowed');
            return;
        }
        players.push(name);
        updatePlayerList();
        input.value = '';
        input.focus();
    }
}

// Allow Enter key to add player
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('player-name-input');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addPlayer();
            }
        });
    }
});

function removePlayer(name) {
    players = players.filter(p => p !== name);
    updatePlayerList();
}

function updatePlayerList() {
    const list = document.getElementById('player-list');
    list.innerHTML = players.map(name => 
        `<span class="player-tag">${name}<button onclick="removePlayer('${name}')">×</button></span>`
    ).join('');
    
    document.getElementById('start-game-btn').disabled = players.length < 3;
}

async function startGame() {
    if (players.length < 3) {
        alert('Need at least 3 players for Oh Hell');
        return;
    }
    
    try {
        const response = await fetch('/api/new_game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ players })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            handSize = data.hand_size;
            dealer = data.dealer;
            totalRounds = data.total_rounds;
            maxCards = data.max_cards;
            
            document.getElementById('setup-screen').classList.remove('active');
            document.getElementById('game-screen').classList.add('active');
            setupRoundInputs();
            updateGameInfo();
            updateScorecard();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error starting game: ' + error.message);
    }
}

// Game Screen Functions
function updateGameInfo() {
    document.getElementById('round-number').textContent = currentRound;
    document.getElementById('hand-size').textContent = handSize;
    document.getElementById('dealer-name').textContent = dealer;
    document.getElementById('total-rounds').textContent = totalRounds;
    document.getElementById('bid-max').textContent = handSize;
    
    // Highlight dealer
    players.forEach(player => {
        const safeId = player.replace(/\s/g, '-');
        const bidInput = document.getElementById(`bid-${safeId}`);
        if (bidInput && bidInput.previousElementSibling) {
            if (player === dealer) {
                bidInput.previousElementSibling.innerHTML = `${player} <span class="dealer-badge">(DEALER)</span>`;
            } else {
                bidInput.previousElementSibling.textContent = player;
            }
        }
    });
}

function setupRoundInputs() {
    const bidInputs = document.getElementById('bid-inputs');
    const trickInputs = document.getElementById('trick-inputs');
    
    bidInputs.innerHTML = players.map(player => {
        const safeId = player.replace(/\s/g, '-');
        return `
            <div class="input-row">
                <label>${player}</label>
                <input type="number" id="bid-${safeId}" min="0" max="${handSize}" placeholder="0-${handSize}" />
            </div>
        `;
    }).join('');
    
    trickInputs.innerHTML = players.map(player => {
        const safeId = player.replace(/\s/g, '-');
        return `
            <div class="input-row">
                <label>${player}</label>
                <input type="number" id="trick-${safeId}" min="0" max="${handSize}" placeholder="0-${handSize}" />
            </div>
        `;
    }).join('');
    
    // Add validation to prevent "screw the dealer"
    players.forEach(player => {
        const safeId = player.replace(/\s/g, '-');
        const bidInput = document.getElementById(`bid-${safeId}`);
        if (bidInput) {
            bidInput.addEventListener('input', checkDealerRule);
        }
    });
}

function checkDealerRule() {
    // Warn if total bids would equal hand size (screw the dealer)
    let totalBids = 0;
    let allFilled = true;
    
    players.forEach(player => {
        const safeId = player.replace(/\s/g, '-');
        const value = document.getElementById(`bid-${safeId}`).value;
        if (value === '') {
            allFilled = false;
        } else {
            totalBids += parseInt(value);
        }
    });
    
    const warning = document.getElementById('dealer-warning');
    if (allFilled && totalBids === handSize) {
        warning.style.display = 'block';
        warning.textContent = `⚠️ Total bids cannot equal ${handSize}! Dealer ${dealer} must bid differently.`;
    } else {
        warning.style.display = 'none';
    }
}

async function submitRound() {
    const bids = {};
    const tricks = {};
    
    // Collect bids and tricks
    for (const player of players) {
        const safeId = player.replace(/\s/g, '-');
        const bidValue = document.getElementById(`bid-${safeId}`).value;
        const trickValue = document.getElementById(`trick-${safeId}`).value;
        
        if (bidValue === '' || trickValue === '') {
            alert('Please enter all bids and tricks');
            return;
        }
        
        bids[player] = parseInt(bidValue);
        tricks[player] = parseInt(trickValue);
    }
    
    // Validate individual trick values
    for (const player of players) {
        const trickValue = tricks[player];
        if (trickValue < 0 || trickValue > handSize) {
            alert(`${player}'s tricks must be between 0 and ${handSize}`);
            return;
        }
    }
    
    // Validate tricks total
    const totalTricks = Object.values(tricks).reduce((a, b) => a + b, 0);
    if (totalTricks !== handSize) {
        alert(`Total tricks must equal ${handSize}. Currently: ${totalTricks}`);
        return;
    }
    
    try {
        const response = await fetch('/api/add_round', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ bids, tricks })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            if (data.game_complete) {
                alert('Game Complete! Check the final scores below.');
                document.getElementById('round-info').innerHTML = '<h2>Game Complete!</h2>';
                document.querySelector('.card:has(#bid-inputs)').style.display = 'none';
                document.querySelector('.card:has(#trick-inputs)').style.display = 'none';
                document.querySelector('.btn-primary').style.display = 'none';
            } else {
                currentRound++;
                handSize = data.hand_size;
                dealer = data.dealer;
                
                // Clear inputs
                players.forEach(player => {
                    const safeId = player.replace(/\s/g, '-');
                    document.getElementById(`bid-${safeId}`).value = '';
                    document.getElementById(`trick-${safeId}`).value = '';
                    document.getElementById(`bid-${safeId}`).max = handSize;
                    document.getElementById(`bid-${safeId}`).placeholder = `0-${handSize}`;
                    document.getElementById(`trick-${safeId}`).max = handSize;
                    document.getElementById(`trick-${safeId}`).placeholder = `0-${handSize}`;
                });
                
                updateGameInfo();
                
                // Focus first input
                const firstPlayer = players[0].replace(/\s/g, '-');
                document.getElementById(`bid-${firstPlayer}`).focus();
            }
            
            updateScorecard();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error submitting round: ' + error.message);
    }
}

async function updateScorecard() {
    try {
        const response = await fetch('/api/game_state');
        const data = await response.json();
        
        if (!data.rounds || data.rounds.length === 0) {
            document.getElementById('scorecard-table').innerHTML = '<p>No rounds played yet</p>';
            return;
        }
        
        let html = '<table><thead><tr><th>Round</th>';
        data.players.forEach(player => {
            html += `<th>${player}</th>`;
        });
        html += '</tr></thead><tbody>';
        
        // Each round
        data.rounds.forEach((round, index) => {
            // Bid row
            html += `<tr><td><strong>R${round.round_num} (${round.hand_size} cards)</strong></td>`;
            data.players.forEach(player => {
                const isDealer = player === round.dealer;
                html += `<td${isDealer ? ' class="dealer-cell"' : ''}>${round.bids[player]}${isDealer ? ' 🂠' : ''}</td>`;
            });
            html += '</tr>';
            
            // Tricks row
            html += `<tr><td><em>Won</em></td>`;
            data.players.forEach(player => {
                html += `<td>${round.tricks[player]}</td>`;
            });
            html += '</tr>';
            
            // Score row
            html += `<tr><td><em>Score</em></td>`;
            data.players.forEach(player => {
                const score = round.round_scores[player];
                const className = score >= 0 ? 'positive-score' : 'negative-score';
                html += `<td class="${className}">${score > 0 ? '+' : ''}${score}</td>`;
            });
            html += '</tr>';
        });
        
        // Total row
        html += '<tr class="total-row"><td><strong>TOTAL</strong></td>';
        data.players.forEach(player => {
            const score = data.scores[player];
            const className = score >= 0 ? 'positive-score' : 'negative-score';
            html += `<td class="${className}">${score}</td>`;
        });
        html += '</tr>';
        
        html += '</tbody></table>';
        document.getElementById('scorecard-table').innerHTML = html;
        
    } catch (error) {
        console.error('Error updating scorecard:', error);
    }
}

async function resetGame() {
    if (confirm('Start a new game? Current game will be lost.')) {
        await fetch('/api/reset', { method: 'POST' });
        players = [];
        currentRound = 1;
        document.getElementById('game-screen').classList.remove('active');
        document.getElementById('setup-screen').classList.add('active');
        document.getElementById('player-list').innerHTML = '';
        document.getElementById('player-name-input').value = '';
        document.getElementById('start-game-btn').disabled = true;
    }
}
