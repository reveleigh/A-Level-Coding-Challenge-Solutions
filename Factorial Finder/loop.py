# Function to calculate factorial using a loop
def factorial_loop(n):
    # Initialise the result to 1, as the factorial of 0 is 1
    result = 1
    
    # Loop from 1 to n (inclusive)
    for i in range(1, n + 1):
        # Multiply the current result by the current value of i
        result *= i
    
    # Return the final result
    return result

# Test the loop implementation
n = 5
# Display the result of the factorial calculation using the loop
print(f"The factorial of {n} using loop is: {factorial_loop(n)}")
