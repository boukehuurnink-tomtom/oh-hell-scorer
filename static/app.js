// Game State
const gameState = {
    players: [],
    currentRound: 1,
    handSize: 0,
    dealer: '',
    totalRounds: 0,
    maxCards: 0
};

const MIN_PLAYERS = 3;
const MAX_PLAYERS = 7;

// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('player-name-input');
    if (input) {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') addPlayer();
        });
    }
    
    // Try to restore game state on page load
    restoreGameState();
});

// Save game state to localStorage
function saveGameState() {
    localStorage.setItem('ohHellGameState', JSON.stringify(gameState));
}

// Restore game state from localStorage
async function restoreGameState() {
    try {
        const data = await fetchApi('/api/game_state');
        
        if (data.players && data.players.length > 0) {
            // Server has an active game
            gameState.players = data.players;
            gameState.currentRound = data.current_round;
            gameState.handSize = data.hand_size;
            gameState.dealer = data.dealer;
            gameState.totalRounds = data.total_rounds;
            gameState.maxCards = data.max_cards;
            
            if (data.hand_size !== null) {
                // Game is active, show game screen
                switchScreen('setup-screen', 'game-screen');
                setupRoundInputs();
                updateGameInfo();
                updateScorecard();
            } else if (data.rounds && data.rounds.length > 0) {
                // Game is complete, show game screen with results
                switchScreen('setup-screen', 'game-screen');
                updateScorecard();
            }
        }
    } catch (error) {
        console.log('No active game to restore');
    }
}

// Setup Screen Functions
function addPlayer() {
    const input = document.getElementById('player-name-input');
    const name = input.value.trim();
    
    if (!name) return;
    
    if (gameState.players.includes(name)) {
        alert('Player already added');
        return;
    }
    
    if (gameState.players.length >= MAX_PLAYERS) {
        alert(`Maximum ${MAX_PLAYERS} players allowed`);
        return;
    }
    
    gameState.players.push(name);
    updatePlayerList();
    input.value = '';
    input.focus();
}

function removePlayer(name) {
    gameState.players = gameState.players.filter(p => p !== name);
    updatePlayerList();
}

function updatePlayerList() {
    const list = document.getElementById('player-list');
    list.innerHTML = gameState.players
        .map(name => `<span class="player-tag">${escapeHtml(name)}<button onclick="removePlayer('${escapeHtml(name)}')">×</button></span>`)
        .join('');
    
    document.getElementById('start-game-btn').disabled = gameState.players.length < MIN_PLAYERS;
}

function escapeHtml(text) {
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return text.replace(/[&<>"']/g, m => map[m]);
}

async function startGame() {
    if (gameState.players.length < MIN_PLAYERS) {
        alert(`Need at least ${MIN_PLAYERS} players for Oh Hell`);
        return;
    }
    
    try {
        const data = await fetchApi('/api/new_game', { players: gameState.players });
        
        gameState.handSize = data.hand_size;
        gameState.dealer = data.dealer;
        gameState.totalRounds = data.total_rounds;
        gameState.maxCards = data.max_cards;
        
        switchScreen('setup-screen', 'game-screen');
        setupRoundInputs();
        updateGameInfo();
        updateScorecard();
    } catch (error) {
        alert('Error starting game: ' + error.message);
    }
}

// Utility Functions
async function fetchApi(url, body = null) {
    const options = {
        method: body ? 'POST' : 'GET',
        headers: { 'Content-Type': 'application/json' }
    };
    if (body) options.body = JSON.stringify(body);
    
    const response = await fetch(url, options);
    const data = await response.json();
    
    if (!response.ok) {
        throw new Error(data.error || 'Request failed');
    }
    return data;
}

function switchScreen(fromId, toId) {
    document.getElementById(fromId).classList.remove('active');
    document.getElementById(toId).classList.add('active');
}

function getSafeId(playerName) {
    return playerName.replace(/\s/g, '-');
}

// Game Screen Functions
function updateGameInfo() {
    document.getElementById('round-number').textContent = gameState.currentRound;
    document.getElementById('hand-size').textContent = gameState.handSize;
    document.getElementById('dealer-name').textContent = gameState.dealer;
    document.getElementById('total-rounds').textContent = gameState.totalRounds;
    document.getElementById('bid-max').textContent = gameState.handSize;
    
    // Highlight dealer
    gameState.players.forEach(player => {
        const safeId = getSafeId(player);
        const bidInput = document.getElementById(`bid-${safeId}`);
        if (bidInput?.previousElementSibling) {
            bidInput.previousElementSibling.innerHTML = player === gameState.dealer
                ? `${escapeHtml(player)} <span class="dealer-badge">(DEALER)</span>`
                : escapeHtml(player);
        }
    });
}

function setupRoundInputs() {
    const bidInputs = document.getElementById('bid-inputs');
    const trickInputs = document.getElementById('trick-inputs');
    
    bidInputs.innerHTML = gameState.players.map(player => createInputRow(player, 'bid')).join('');
    trickInputs.innerHTML = gameState.players.map(player => createInputRow(player, 'trick')).join('');
    
    // Add validation to prevent "screw the dealer"
    gameState.players.forEach(player => {
        const bidInput = document.getElementById(`bid-${getSafeId(player)}`);
        bidInput?.addEventListener('input', checkDealerRule);
    });
}

function createInputRow(player, type) {
    const safeId = getSafeId(player);
    return `
        <div class="input-row">
            <label>${escapeHtml(player)}</label>
            <input type="number" id="${type}-${safeId}" min="0" max="${gameState.handSize}" placeholder="0-${gameState.handSize}" />
        </div>
    `;
}

function checkDealerRule() {
    const { totalBids, allFilled } = calculateTotalBids();
    const warning = document.getElementById('dealer-warning');
    
    if (allFilled && totalBids === gameState.handSize) {
        warning.style.display = 'block';
        warning.textContent = `⚠️ Total bids cannot equal ${gameState.handSize}! Dealer ${gameState.dealer} must bid differently.`;
    } else {
        warning.style.display = 'none';
    }
}

function calculateTotalBids() {
    let totalBids = 0;
    let allFilled = true;
    
    gameState.players.forEach(player => {
        const value = document.getElementById(`bid-${getSafeId(player)}`).value;
        if (value === '') {
            allFilled = false;
        } else {
            totalBids += parseInt(value);
        }
    });
    
    return { totalBids, allFilled };
}

async function submitRound() {
    const { bids, tricks } = collectRoundData();
    
    if (!bids || !tricks) return; // Validation failed
    
    try {
        const data = await fetchApi('/api/add_round', { bids, tricks });
        
        if (data.game_complete) {
            handleGameComplete();
        } else {
            handleNextRound(data);
        }
        
        updateScorecard();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function collectRoundData() {
    const bids = {};
    const tricks = {};
    
    // Collect bids and tricks
    for (const player of gameState.players) {
        const safeId = getSafeId(player);
        const bidValue = document.getElementById(`bid-${safeId}`).value;
        const trickValue = document.getElementById(`trick-${safeId}`).value;
        
        if (bidValue === '' || trickValue === '') {
            alert('Please enter all bids and tricks');
            return {};
        }
        
        bids[player] = parseInt(bidValue);
        tricks[player] = parseInt(trickValue);
    }
    
    // Validate tricks
    const totalTricks = Object.values(tricks).reduce((sum, val) => sum + val, 0);
    if (totalTricks !== gameState.handSize) {
        alert(`Total tricks must equal ${gameState.handSize}. Currently: ${totalTricks}`);
        return {};
    }
    
    return { bids, tricks };
}

function handleGameComplete() {
    alert('Game Complete! Check the final scores below.');
    document.getElementById('round-info').innerHTML = '<h2>Game Complete!</h2>';
    document.querySelector('.card:has(#bid-inputs)').style.display = 'none';
    document.querySelector('.card:has(#trick-inputs)').style.display = 'none';
    document.querySelector('.btn-primary').style.display = 'none';
}

function handleNextRound(data) {
    gameState.currentRound++;
    gameState.handSize = data.hand_size;
    gameState.dealer = data.dealer;
    
    clearInputs();
    updateGameInfo();
    focusFirstInput();
}

function clearInputs() {
    gameState.players.forEach(player => {
        const safeId = getSafeId(player);
        const bidInput = document.getElementById(`bid-${safeId}`);
        const trickInput = document.getElementById(`trick-${safeId}`);
        
        if (bidInput) {
            bidInput.value = '';
            bidInput.max = gameState.handSize;
            bidInput.placeholder = `0-${gameState.handSize}`;
        }
        if (trickInput) {
            trickInput.value = '';
            trickInput.max = gameState.handSize;
            trickInput.placeholder = `0-${gameState.handSize}`;
        }
    });
}

function focusFirstInput() {
    const firstInput = document.getElementById(`bid-${getSafeId(gameState.players[0])}`);
    firstInput?.focus();
}

async function updateScorecard() {
    try {
        const data = await fetchApi('/api/game_state');
        
        if (!data.rounds || data.rounds.length === 0) {
            document.getElementById('scorecard-table').innerHTML = '<p>No rounds played yet</p>';
            return;
        }
        
        document.getElementById('scorecard-table').innerHTML = buildScorecardTable(data);
    } catch (error) {
        console.error('Error updating scorecard:', error);
    }
}

function buildScorecardTable(data) {
    const header = buildTableHeader(data.players);
    const body = buildTableBody(data);
    return `<table><thead>${header}</thead><tbody>${body}</tbody></table>`;
}

function buildTableHeader(players) {
    const playerHeaders = players.map(p => `<th>${escapeHtml(p)}</th>`).join('');
    return `<tr><th>Round</th>${playerHeaders}</tr>`;
}

function buildTableBody(data) {
    const rounds = data.rounds.map(round => buildRoundRows(round, data.players)).join('');
    const totals = buildTotalRow(data.players, data.scores);
    return rounds + totals;
}

function buildRoundRows(round, players) {
    const bidRow = buildRow(`R${round.round_num} (${round.hand_size} cards)`, players, 
        p => round.bids[p] + (p === round.dealer ? ' 🂠' : ''), 
        p => p === round.dealer);
    const wonRow = buildRow('<em>Won</em>', players, p => round.tricks[p]);
    const scoreRow = buildRow('<em>Score</em>', players, 
        p => formatScore(round.round_scores[p]), 
        null, 
        p => round.round_scores[p] >= 0 ? 'positive-score' : 'negative-score');
    return bidRow + wonRow + scoreRow;
}

function buildRow(label, players, valueFunc, highlightFunc = null, classFunc = null) {
    const cells = players.map(player => {
        const value = valueFunc(player);
        const highlight = highlightFunc?.(player) ? ' class="dealer-cell"' : '';
        const cssClass = classFunc?.(player) ? ` class="${classFunc(player)}"` : '';
        return `<td${highlight}${cssClass}>${value}</td>`;
    }).join('');
    return `<tr><td><strong>${label}</strong></td>${cells}</tr>`;
}

function buildTotalRow(players, scores) {
    const cells = players.map(player => {
        const score = scores[player];
        const cssClass = score >= 0 ? 'positive-score' : 'negative-score';
        return `<td class="${cssClass}">${score}</td>`;
    }).join('');
    return `<tr class="total-row"><td><strong>TOTAL</strong></td>${cells}</tr>`;
}

function formatScore(score) {
    return score > 0 ? `+${score}` : score;
}

async function resetGame() {
    if (!confirm('Start a new game? Current game will be lost.')) return;
    
    try {
        await fetchApi('/api/reset', {});
        
        // Clear local game state
        gameState.players = [];
        gameState.currentRound = 1;
        gameState.handSize = 0;
        gameState.dealer = '';
        gameState.totalRounds = 0;
        gameState.maxCards = 0;
        
        // Show setup screen again
        switchScreen('game-screen', 'setup-screen');
        document.getElementById('player-list').innerHTML = '';
        document.getElementById('player-name-input').value = '';
        document.getElementById('start-game-btn').disabled = true;
        
        // Show the input cards again in case they were hidden (game complete)
        const bidCard = document.querySelector('.card:has(#bid-inputs)');
        const trickCard = document.querySelector('.card:has(#trick-inputs)');
        const submitBtn = document.querySelector('.btn-primary');
        if (bidCard) bidCard.style.display = '';
        if (trickCard) trickCard.style.display = '';
        if (submitBtn) submitBtn.style.display = '';
    } catch (error) {
        console.error('Error resetting game:', error);
    }
}
