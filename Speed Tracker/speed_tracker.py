def is_valid_number_plate(plate):
    # Check if the given number plate follows the specified format.
    # Valid format: Two letters, two numbers, a space, and three letters.
    if (
        len(plate) == 8
        and plate[:2].isalpha()
        and plate[2:4].isdigit()
        and plate[4] == ' '
        and plate[5:8].isalpha()
    ):
        return True
    return False

#Function to check plate
def check_number_plate(plate):
    # Check and print whether the given number plate is valid.
    if is_valid_number_plate(plate):
        print("Valid number plate.")
    else:
        print("Invalid number plate.")

def calculate_speed(time1, time2, distance):
    # Calculate the speed in miles per hour based on the given time and distance.
    speed_mph = distance / ((time2 - time1) / 3600)  # speed = distance/time (in hours)
    return round(speed_mph, 2)

def process_speed_data(speed_data):
    # Process speed data for each vehicle, checking number plates and identifying speeding cars.
    speeding_cars = []
    invalid_number_plates = []

    for data in speed_data:
        time1, time2, plate = data
        speed = calculate_speed(time1, time2, 1)
        
        print(f"Number Plate: {plate}")
        check_number_plate(plate)
        if not is_valid_number_plate(plate):
            invalid_number_plates.append(plate)
        
        print(f"Calculated Speed: {speed} mph")
        if speed > 70:
            print("Speeding: Above 70 mph\n")
            speeding_cars.append((plate, speed))
        else:
            print("Not Speeding: Below or equal to 70 mph\n")

    return speeding_cars, invalid_number_plates

# Example usage assuming first camera marks the beginning of timer
speed_data = [(0, 62, "AB12 ERT"), (0, 60, "XY45 DCS"), (0, 90, "ZZ99 999")]

speeding_cars, invalid_number_plates = process_speed_data(speed_data)

print("Speeding cars:", speeding_cars)
print("Invalid number plates:", invalid_number_plates)
