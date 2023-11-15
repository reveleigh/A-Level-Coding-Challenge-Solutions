// Recursive function to calculate factorial
function factorialRecursive(n) {
    // Base case: If n is 0, return 1 (factorial of 0 is 1)
    if (n === 0) {
        return 1;
    } else {
        // Recursive case: n * factorialRecursive(n - 1)
        // Multiply n by the factorial of (n-1) using recursion
        return n * factorialRecursive(n - 1);
    }
}

// Test the recursion implementation
let n = 5;
// Display the result of the factorial calculation using recursion
console.log(`The factorial of ${n} using recursion is: ${factorialRecursive(n)}`);
