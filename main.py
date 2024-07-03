

# main.py

from operations import square_number


def main():
    # Prompt the user to enter a number with a default value of 3
    input_value = input("Please enter a number (default is 3): ")
    
    # Use the default value if the user does not enter anything
    if not input_value:
        number = 3
    else:
        try:
            number = float(input_value)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            return
    
    # Confirm the entered value
    confirm = input(f"You entered {number}. Is this correct? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Input not confirmed. Exiting program.")
        return
    
    # Call the function from module.py
    result = square_number(number)
    
    # Print the result
    print(f"The square of {number} is {result}")

if __name__ == "__main__":
    main()
