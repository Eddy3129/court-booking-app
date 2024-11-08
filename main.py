# main.py

# Importing necessary functions from other modules
from users import load_users, login_action,signup_action,quit_action
from manage_booking import (
    load_bookings,
    save_bookings,
    view_user_bookings,
    cancel_user_booking,
)
from functools import reduce

def main_menu():
    print("\n--- Welcome to the Court Booking System ---")
    print("1. Login")
    print("2. Signup")
    print("3. Quit")
    
def get_user_input(prompt):
    return input(prompt)

def booking_actions_menu():
    print("\n--- Booking Management ---")
    print("1. View Your Active Bookings")
    print("2. Cancel a Booking")
    print("3. Logout")

# 3. Create a list of functions and use that list: Define booking-related actions as a list of lambda functions.
def user_actions(bookings, current_user):
    while True:
        booking_actions_menu()
        choice = input("Enter your choice (1-3): ")

        # Define a list of booking actions corresponding to user choices.
        booking_actions = [
            lambda: view_user_bookings(bookings, current_user),  # Option 1
            lambda: cancel_booking_flow(bookings, current_user),  # Option 2
            lambda: print("\nLogging out...")                     # Option 3
        ]

        if choice in ['1', '2', '3']:
            # Convert choice to zero-based index to access the corresponding function.
            action_index = int(choice) - 1
            action_fn = booking_actions[action_index]
            action_fn()
            if choice == '3':
                break  # Exit the booking management loop.
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
    return bookings

# Helper functions to handle specific booking actions.
def cancel_booking_flow(bookings, current_user):
    try:
        booking_id = int(input("Enter Booking ID to cancel: "))
        bookings = cancel_user_booking(bookings, booking_id, current_user)
        save_bookings(bookings)
    except ValueError:
        print("Invalid input. Please enter a numeric booking ID.")

def main():
    # 1. Separating functions and data: Load users and bookings data from external files.
    users = load_users()
    bookings = load_bookings()
    
    # 3. Creating a List of Functions: 
    # Here, we use a dictionary to map actions to functions, similar to a list of functions
    # but organized by action names for direct retrieval.
    
    # Create a dictionary of available actions
    actions = {
        "1": login_action,
        "2": signup_action,
        "3": quit_action
    }

    while True:
        main_menu()
        # 6. Mapping: User choice is mapped to a function in the `actions` dictionary.
        choice = get_user_input("Enter your choice (1, 2, or 3): ")
        # Retrieve and execute the function based on the user's choice
        action_fn = actions.get(choice)  # 2. Assigning function to variable
        
        if action_fn:
            if choice == "3":
                action_fn()  # Call the quit action and break
                break
            elif choice == "1":
                username = action_fn(users)  # Call the login action with users as argument
                if username:
                    bookings = user_actions(bookings, username)
            else:
                action_fn(users)  # Call signup with users as argument
        else:
            print("\nInvalid option. Try again.")

if __name__ == "__main__":
    main()
