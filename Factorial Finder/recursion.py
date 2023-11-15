# Recursive function to calculate factorial
def factorial_recursive(n):
    # Base case: If n is 0, return 1 (factorial of 0 is 1)
    if n == 0:
        return 1
    else:
        # Recursive case: n * factorial_recursive(n - 1)
        # Multiply n by the factorial of (n-1) using recursion
        return n * factorial_recursive(n - 1)

# Test the recursion implementation
n = 5
# Display the result of the factorial calculation using recursion
print(f"The factorial of {n} using recursion is: {factorial_recursive(n)}")
