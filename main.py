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
    print("3. Check your prefered time slot")
    print("4. Quit")

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
def find_consecutive_slots(court_filter, day, court, start_time, duration):
    """Find consecutive available slots."""
    slots_needed = int(duration * 2)  # Convert hours to 30-min slots
    available_slots = []
    
    current_time = datetime.strptime(start_time, "%I:%M %p")
    
    for _ in range(slots_needed):
        time_str = current_time.strftime("%I:%M %p")
        if time_str not in court_filter.days[day][court]:
            return []
        available_slots.append(time_str)
        current_time += timedelta(minutes=30)
    
    return available_slots

def check_availability_recursive(court_filter, day, preferred_time, preferred_court, duration, 
                               search_window=2, tried_times=None):
    """
    Recursively check availability and suggest alternatives.
    Returns a list of dictionaries containing available slots.
    """
    if tried_times is None:
        tried_times = set()
        print(f"\nChecking availability for Court {preferred_court} at {preferred_time}...")
    
    # Base case: if we've searched beyond our window
    time_dt = datetime.strptime(preferred_time, "%I:%M %p")
    if any(abs((datetime.strptime(t, "%I:%M %p") - time_dt).total_seconds() / 3600) > search_window 
           for t in tried_times):
        return []
    
    # Add current time to tried times
    tried_times.add(preferred_time)
    
    # Check if preferred slot is available
    slots = find_consecutive_slots(court_filter, day, preferred_court, preferred_time, duration)
    results = []
    
    if slots:
        results.append({
            'court': preferred_court,
            'time': preferred_time,
            'slots': slots,
            'type': 'preferred' if preferred_time == slots[0] else 'alternative'
        })
    
    # Check other courts at same time
    available_courts = [c for c in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] 
                       if c != preferred_court and preferred_time in court_filter.days[day][c]]
    
    for court in available_courts:
        alt_slots = find_consecutive_slots(court_filter, day, court, preferred_time, duration)
        if alt_slots:
            results.append({
                'court': court,
                'time': preferred_time,
                'slots': alt_slots,
                'type': 'alternative'
            })
    
    # Calculate next times to check (both earlier and later)
    next_time_later = (time_dt + timedelta(minutes=30)).strftime("%I:%M %p")
    next_time_earlier = (time_dt - timedelta(minutes=30)).strftime("%I:%M %p")
    
    # Recursively check both directions
    for next_time in [next_time_later, next_time_earlier]:
        if next_time not in tried_times:
            results.extend(check_availability_recursive(
                court_filter, day, next_time, preferred_court, duration, 
                search_window, tried_times))
    
    return results

def display_availability_results(results):
    """Display availability results in a user-friendly format."""
    if not results:
        print("\nNo available slots found within the search window.")
        return
        
    # Sort results by time and preference
    results.sort(key=lambda x: (
        datetime.strptime(x['time'], "%I:%M %p"),
        0 if x['type'] == 'preferred' else 1
    ))
    
    print("\nAvailable slots found:")
    print("----------------------")
    
    for i, result in enumerate(results, 1):
        slot_times = ' → '.join(result['slots'])
        status = "PREFERRED" if result['type'] == 'preferred' else "ALTERNATIVE"
        print(f"\n{i}. Court {result['court']} - {status}")
        print(f"   Start: {result['time']}")
        print(f"   Slots: {slot_times}")

def check_court_availability(court_filter):
    """Handle the court availability check with recursive search."""
    while True:
        try:
            day_input = users.get_user_input("Enter day (1-7, where 1 is Monday): ").strip()
            if day_input.lower() == 'q':
                return
            day_num = int(day_input)
            if day_num < 1 or day_num > 7:
                raise ValueError
            day_index = day_num - 1
            break
        except ValueError:
            print("Invalid day number. Please enter a number between 1 and 7.")

    while True:
        time_input = users.get_user_input("Enter preferred time (e.g., 2:00 PM): ").strip().upper()
        if time_input.lower() == 'q':
            return
        try:
            if not ("AM" in time_input or "PM" in time_input):
                print("Time must include AM or PM.")
                continue
            parsed_time = datetime.strptime(time_input, "%I:%M %p")
            preferred_time = parsed_time.strftime("%I:%M %p")
            break
        except ValueError:
            print("Invalid time format. Please enter time in HH:MM AM/PM format (e.g., 2:00 PM).")

    while True:
        court_id = users.get_user_input("Enter preferred court (A-H): ").strip().upper()
        if court_id.lower() == 'q':
            return
        if court_id not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            print("Invalid Court ID. Please enter a letter from A to H.")
            continue
        break

    while True:
        duration_input = users.get_user_input("Enter duration in hours (0.5 for 30 mins, 1 for 1 hour, etc.): ").strip()
        if duration_input.lower() == 'q':
            return
        try:
            duration_hours = float(duration_input)
            if duration_hours <= 0:
                raise ValueError
            if (duration_hours * 2) != int(duration_hours * 2):
                print("Duration must be in multiples of 30 minutes (e.g., 0.5, 1, 1.5).")
                continue
            break
        except ValueError:
            print("Invalid duration. Please enter a positive number in 30-minute increments.")

    # Call the recursive availability check
    results = check_availability_recursive(
        court_filter,
        day_index,
        preferred_time,
        court_id,
        duration_hours
    )
    
    # Display the results
    display_availability_results(results)

def main():
    """Main function to run the court booking application."""
    # 1. Separating Functions and Data: Load users separately
    users_data = users.load_users()  # 1. Separating functions and data
    bookings = Bookings()  # 1. Separating functions and data
    court_filter = CourtFilter()

    court_filter.synchronize_with_bookings(bookings.bookings)

    while True:
        main_menu()
        choice = users.get_user_input("Enter your choice (1-4): ").strip()  # 4. Passing functions as arguments

        if choice in ['1', '2', '3', '4']:
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
                check_court_availability(court_filter)  # 2. Assigning a function to a variable
            elif choice == "4":
                users.quit_action()  # 2. Assigning a function to a variable
            
        else:
            print("\nInvalid option. Try again.")  # 7. Filtering

if __name__ == "__main__":
    main()
