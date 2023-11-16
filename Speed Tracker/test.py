def is_valid_number_plate(plate):
    # Check if the given number plate follows the specified format.
    # Valid format: Two letters, two numbers, a space, and three letters.
    if (
        len(plate) == 8
        and plate[0:2].isalpha()
        and plate[2:4].isdigit()
        and plate[4] == ' '
        and plate[5:8].isalpha()
    ):
        return True
    return False

def check_number_plate(plate):
    # Check and print whether the given number plate is valid.
    if is_valid_number_plate(plate):
        print("Valid number plate.")
    else:
        print("Invalid number plate.")

check_number_plate("ab12 ert")