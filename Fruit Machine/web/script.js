let balance = 1.00;
const symbols = ['cherry', 'bell', 'lemon', 'orange', 'star', 'skull'];

function spin() {
    const slot1 = document.getElementById('slot1');
    const slot2 = document.getElementById('slot2');
    const slot3 = document.getElementById('slot3');

    // Check if balance is sufficient for play
    if (balance < 0.20) {
        gameOver("You have run out of money");
        return;
    }

    // Subtract 20p from balance for each play
    balance -= 0.20;

    // Randomly select symbols
    const symbol1 = symbols[Math.floor(Math.random() * symbols.length)];
    const symbol2 = symbols[Math.floor(Math.random() * symbols.length)];
    const symbol3 = symbols[Math.floor(Math.random() * symbols.length)];

    // Display symbols
    slot1.src = `${symbol1}.png`;
    slot2.src = `${symbol2}.png`;
    slot3.src = `${symbol3}.png`;

    // Check winnings
    if (symbol1 === symbol2 && symbol2 === symbol3) {
        if (symbol1 === 'bell') {
            balance += 5.00;
        } else {
            balance += 1.00;
        }
    } else if (symbol1 === symbol2 || symbol1 === symbol3 || symbol2 === symbol3) {
        balance += 0.50;
    } else if (symbol1 === 'skull' && symbol2 === 'skull' && symbol3 === 'skull') {
        balance = 0.00;
    } else if (symbol1 === 'skull' && symbol2 === 'skull') {
        balance -= 1.00;
    }

    // Update balance
    document.getElementById('balance').textContent = `Balance: £${balance.toFixed(2)}`;
}

function quit() {
    if (balance < 0.20) {
        gameOver("You have run out of money");
    } else {
        gameOver(`You cashed out: £${balance.toFixed(2)}`);
    }
}

function gameOver(message) {
    const playDiv = document.getElementById('play');
    const gameOverDiv = document.getElementById('gameOver');
    playDiv.style.display = 'none';
    gameOverDiv.style.display = 'block';

    const h1 = document.querySelector('h1');
    h1.textContent = "Game Over";

    const messagePara = document.getElementById('message');
    messagePara.textContent = message;

    const playAgainButton = document.getElementById('playAgain');
    playAgainButton.onclick = resetGame;
}

function resetGame() {
    balance = 1.00;
    document.getElementById('balance').textContent = `Balance: £${balance.toFixed(2)}`;

    const playDiv = document.getElementById('play');
    const gameOverDiv = document.getElementById('gameOver');
    playDiv.style.display = 'block';
    gameOverDiv.style.display = 'none';

    const h1 = document.querySelector('h1');
    h1.textContent = "Fruit Machine";
}
