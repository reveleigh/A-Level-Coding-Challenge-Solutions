def generate_pin_combinations(digits):
    combinations = []

    # Use nested loops to iterate through all of the possible combinations
    for digit1 in digits:
        for digit2 in digits:
            for digit3 in digits:
                for digit4 in digits:
                    # Check if all digits are unique
                    if digit1 != digit2 and digit1 != digit3 and digit1 != digit4 and digit2 != digit3 and digit2 != digit4 and digit3 != digit4:
                        combination = f"{digit1}{digit2}{digit3}{digit4}"
                        combinations.append(combination)

    return combinations

def main():
    # Get input from the user
    user_input = input("Enter four numerical digits (e.g., 1234): ")

    # Check if the input has exactly four digits
    if len(user_input) != 4 or not user_input.isdigit():
        print("Invalid input. Please enter exactly four numerical digits.")
        return

    # Convert the input to a list of digits
    digits = list(user_input)

    # Generate and display unique combinations
    combinations = generate_pin_combinations(digits)

    # Print the combinations
    print("\nAll possible unique combinations:")
    for combination in combinations:
        print(combination)

# Call the main function
main()
