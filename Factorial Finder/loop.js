// Function to calculate factorial using a loop
function factorialLoop(n) {
    // Initialise the result to 1, as the factorial of 0 is 1
    let result = 1;
    
    // Loop from 1 to n (inclusive)
    for (let i = 1; i <= n; i++) {
        // Multiply the current result by the current value of i
        result *= i;
    }
    
    // Return the final result
    return result;
}

// Test the loop implementation
let n = 5;
// Display the result of the factorial calculation using the loop
console.log(`The factorial of ${n} using loop is: ${factorialLoop(n)}`);
