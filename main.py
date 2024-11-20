# main.py

import os
from bookings import Bookings
from filter_courts import CourtFilter
from datetime import datetime, timedelta
import users  # Importing functional user management
from functools import partial

def main_menu():
    """Display the main menu."""
    print("\n--- Welcome to the Court Booking System ---")
    print("1. Login")
    print("2. Signup")
    print("3. Quit")

def booking_actions_menu():
    """Display the booking management menu."""
    print("\n--- Booking Management ---")
    print("1. View Your Active Bookings")
    print("2. Cancel a Booking")
    print("3. Create a New Booking")
    print("4. Check Court Availability")
    print("5. Logout")

def user_actions(bookings, current_user, court_filter):
    """Handle user actions after login."""
    while True:
        booking_actions_menu()
        choice = users.get_user_input("Enter your choice (1-5): ")  # 4. Passing functions as arguments

        # 3. Creating a list of functions: map user choices to corresponding actions
        booking_actions = [
            lambda: bookings.view_user_bookings(current_user),                         # Option 1
            lambda: cancel_booking_flow(bookings, current_user, court_filter),          # Option 2
            lambda: create_booking_flow(bookings, current_user, court_filter),          # Option 3
            lambda: check_court_availability(court_filter),                            # Option 4
            lambda: print("\nLogging out...")                                           # Option 5
        ]

        if choice in ['1', '2', '3', '4', '5']:
            # 2. Assigning a function to a variable: select the action based on choice
            action_fn = booking_actions[int(choice) - 1]
            action_fn()
            if choice == '5':
                break  # Exit the booking management loop
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")

def cancel_booking_flow(bookings, current_user, court_filter):
    """Handle the cancellation of bookings."""
    while True:
        try:
            booking_id_input = users.get_user_input("Enter Booking ID to cancel (or type 'q' to return): ").strip()  # 4. Passing functions as arguments
            if booking_id_input.lower() == 'q':
                print("Cancellation process aborted.")
                break
            booking_id = int(booking_id_input)
        except ValueError:
            print("Invalid input. Please enter a numeric booking ID or 'q' to quit.")
            continue

        # Attempt to cancel the booking using filtering and lambda
        success = bookings.cancel_user_booking(booking_id, current_user)
        if success:
            # 5. Returning functions: synchronize court availability after cancellation
            court_filter.synchronize_with_bookings(bookings.bookings)
            print(f"Booking ID {booking_id} has been canceled and court availability updated.")
        else:
            print("Booking not found or already canceled.")

        # Ask if the user wants to cancel another booking using filtering
        retry = users.get_user_input("Do you want to cancel another booking? (y/n): ").strip().lower()  # 4. Passing functions as arguments
        if retry != 'y':
            print("Cancellation process completed.")
            break

def create_booking_flow(bookings, current_user, court_filter):
    """Handle the creation of new bookings."""
    while True:
        court_id = users.get_user_input("Enter Court ID (A-H) (or type 'q' to cancel): ").strip().upper()  # 4. Passing functions as arguments
        if court_id.lower() == 'q':
            print("Booking creation canceled.")
            break

        # Validate court_id using list comprehension
        if court_id not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            print("Invalid Court ID. Please enter a letter from A to H.")
            continue

        # Get and validate day number
        while True:
            day_input = users.get_user_input("Enter Day of the Week (1 for Monday, 7 for Sunday) (or type 'q' to cancel): ").strip()  # 4. Passing functions as arguments
            if day_input.lower() == 'q':
                print("Booking creation canceled.")
                return
            try:
                day_num = int(day_input)
                if day_num < 1 or day_num > 7:
                    raise ValueError
                # Map day number to day name
                days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                day = days_of_week[day_num - 1]
                break
            except ValueError:
                print("Invalid day number. Please enter a number between 1 (Monday) and 7 (Sunday), or 'q' to cancel.")

        # Get and validate start time
        while True:
            start_time_input = users.get_user_input("Enter Start Time (HH:MM AM/PM) (or type 'q' to cancel): ").strip().upper()  # 4. Passing functions as arguments
            if start_time_input.lower() == 'q':
                print("Booking creation canceled.")
                return
            try:
                # Normalize time input to ensure it has AM/PM
                if not ("AM" in start_time_input or "PM" in start_time_input):
                    print("Time must include AM or PM.")
                    continue
                # Attempt to parse time
                parsed_start_time = datetime.strptime(start_time_input, "%I:%M %p")
                # Reformat time to standard format
                start_time = parsed_start_time.strftime("%I:%M %p")
                #6) Mapping: Use map to check availability for all courts
                availability = list(map(lambda court: start_time in court_filter.days[day_num - 1][court], court_filter.days[day_num - 1]))
                if not any(availability):
                    print(f"The start time slot '{start_time}' is not available. Please choose a valid 30-minute interval.")
                    continue
                break
            except ValueError:
                print("Invalid time format. Please enter time in HH:MM AM/PM format (e.g., 08:00 AM), or 'q' to cancel.")
                continue

        # Get and validate duration
        while True:
            duration_input = users.get_user_input("Enter Duration in hours (e.g., 1, 1.5) (or type 'q' to cancel): ").strip()  # 4. Passing functions as arguments
            if duration_input.lower() == 'q':
                print("Booking creation canceled.")
                return
            try:
                duration_hours = float(duration_input)
                if duration_hours <= 0:
                    raise ValueError
                if (duration_hours * 2) != int(duration_hours * 2):
                    print("Duration must be in multiples of 30 minutes (e.g., 1, 1.5, 2).")
                    continue
                duration = f"{duration_hours} hour{'s' if duration_hours != 1 else ''}"
                break
            except ValueError:
                print("Invalid duration. Please enter a positive number in 30-minute increments (e.g., 1, 1.5, 2), or 'q' to cancel.")
                continue

        # Calculate end_time based on start_time and duration
        parsed_start_time = datetime.strptime(start_time, "%I:%M %p")
        end_time_dt = parsed_start_time + timedelta(hours=duration_hours)
        end_time = end_time_dt.strftime("%I:%M %p")

        # Check if end_time slot exists
        if not any(end_time in court_filter.days[day_num - 1][court] for court in court_filter.days[day_num - 1]):
            print(f"The end time slot '{end_time}' is outside of operating hours. Please adjust your booking duration.")
            continue

        # Create the booking using filtering and lambda
        success = bookings.create_booking(court_id, day, start_time, end_time, duration_hours, current_user)
        if success:
            print(f"Booking created successfully for Court {court_id} on {day} from {start_time} to {end_time} for {duration}.")
            break
        else:
            retry = users.get_user_input("Failed to create booking. Do you want to try again? (y/n): ").strip().lower()  # 4. Passing functions as arguments
            if retry != 'y':
                print("Booking creation canceled.")
                break

def check_court_availability(court_filter):
    """Check available courts for a specific day and time slot."""
    while True:
        try:
            day_input = users.get_user_input("Enter the day (1 for Monday, 7 for Sunday) (or type 'q' to cancel): ").strip()  # 4. Passing functions as arguments
            if day_input.lower() == 'q':
                print("Court availability check canceled.")
                return
            day_num = int(day_input)
            if day_num < 1 or day_num > 7:
                raise ValueError
            # Map day number to day name
            days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day = days_of_week[day_num - 1]
            day_index = day_num - 1
            break
        except ValueError:
            print("Invalid day number. Please enter a number between 1 (Monday) and 7 (Sunday), or 'q' to cancel.")

    while True:
        time_slot_input = users.get_user_input("Enter the time slot (HH:MM AM/PM) (or type 'q' to cancel): ").strip().upper()  # 4. Passing functions as arguments
        if time_slot_input.lower() == 'q':
            print("Court availability check canceled.")
            return
        try:
            # Normalize time input to ensure it has AM/PM
            if not ("AM" in time_slot_input or "PM" in time_slot_input):
                print("Time must include AM or PM.")
                continue
            # Attempt to parse time
            parsed_time = datetime.strptime(time_slot_input, "%I:%M %p")
            # Reformat time to standard format
            time_slot = parsed_time.strftime("%I:%M %p")
            # Check if the time slot exists in any court for the given day using filtering
            #6) Mapping: Use map to check availability for all courts
            availability_check = list(map(lambda court: time_slot in court_filter.days[day_index][court], court_filter.days[day_index]))
            if not any(availability_check):
                print(f"The time slot '{time_slot}' is not available. Please choose a valid 30-minute interval.")
                continue
            break
        except ValueError:
            print("Invalid time format. Please enter time in HH:MM AM/PM format (e.g., 08:00 AM), or 'q' to cancel.")
            continue

    # 7. Filtering: Get available courts
    available = court_filter.available_courts(day_index, time_slot)
    if available:
        print(f"Available courts on {days_of_week[day_index]} at {time_slot}: {available}")
    else:
        print(f"No available courts on {days_of_week[day_index]} at {time_slot}.")

def main():
    """Main function to run the court booking application."""
    # 1. Separating Functions and Data: Load users separately
    users_data = users.load_users()  # 1. Separating functions and data
    bookings = Bookings()  # 1. Separating functions and data
    court_filter = CourtFilter()

    court_filter.synchronize_with_bookings(bookings.bookings)

    while True:
        main_menu()
        choice = users.get_user_input("Enter your choice (1-3): ").strip()  # 4. Passing functions as arguments

        if choice in ['1', '2', '3']:
            if choice == "1":
                username = users.log_in(users_data)  # 2. Assigning a function to a variable
                if username:
                    user_actions(bookings, username, court_filter)
                    # Reload bookings and court_filter after user actions using reducing
                    bookings = Bookings()
                    court_filter = CourtFilter()
                    court_filter.synchronize_with_bookings(bookings.bookings)
            elif choice == "2":
                users_data = users.sign_up(users_data)  # 2. Assigning a function to a variable
            elif choice == "3":
                users.quit_action()  # 2. Assigning a function to a variable
        else:
            print("\nInvalid option. Try again.")  # 7. Filtering

if __name__ == "__main__":
    main()
