// Initialize the balance to £1.00
let balance = 1.00;

// Define an array of symbols for the fruit machine
const symbols = ['cherry', 'bell', 'lemon', 'orange', 'star', 'skull'];

// Function to handle spinning the fruit machine
function spin() {
    // Get references to the slot images
    const slot1 = document.getElementById('slot1');
    const slot2 = document.getElementById('slot2');
    const slot3 = document.getElementById('slot3');

    // Check if balance is sufficient for play
    if (balance < 0.20) {
        // If balance is insufficient, end the game with a message
        gameOver("You have run out of money");
        return;
    }

    // Subtract 20p from balance for each play
    balance -= 0.20;

    // Randomly select symbols for each slot
    const symbol1 = symbols[Math.floor(Math.random() * symbols.length)];
    const symbol2 = symbols[Math.floor(Math.random() * symbols.length)];
    const symbol3 = symbols[Math.floor(Math.random() * symbols.length)];

    // Display the selected symbols in the slots
    slot1.src = `${symbol1}.png`;
    slot2.src = `${symbol2}.png`;
    slot3.src = `${symbol3}.png`;

    // Check for winning combinations and adjust balance accordingly
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

    // Update the balance display
    document.getElementById('balance').textContent = `Balance: £${balance.toFixed(2)}`;
}

// Function to handle quitting the game
function quit() {
    if (balance < 0.20) {
        // If balance is insufficient, end the game with a message
        gameOver("You have run out of money");
    } else {
        // If the user decides to quit, end the game with a cash out message
        gameOver(`You cashed out: £${balance.toFixed(2)}`);
    }
}

// Function to handle the end of the game
function gameOver(message) {
    // Hide the play section and show the game over section
    const playDiv = document.getElementById('play');
    const gameOverDiv = document.getElementById('gameOver');
    playDiv.style.display = 'none';
    gameOverDiv.style.display = 'block';

    // Update the heading to indicate game over
    const h1 = document.querySelector('h1');
    h1.textContent = "Game Over";

    // Display the game over message
    const messagePara = document.getElementById('message');
    messagePara.textContent = message;

    // Set up the play again button to reset the game
    const playAgainButton = document.getElementById('playAgain');
    playAgainButton.onclick = resetGame;
}

// Function to reset the game state
function resetGame() {
    // Reset the balance to £1.00
    balance = 1.00;
    // Update the balance display
    document.getElementById('balance').textContent = `Balance: £${balance.toFixed(2)}`;

    // Show the play section and hide the game over section
    const playDiv = document.getElementById('play');
    const gameOverDiv = document.getElementById('gameOver');
    playDiv.style.display = 'block';
    gameOverDiv.style.display = 'none';

    // Update the heading to indicate the game has started
    const h1 = document.querySelector('h1');
    h1.textContent = "Fruit Machine";
}
