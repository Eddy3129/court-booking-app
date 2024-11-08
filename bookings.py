# bookings.py

import os
import csv
from collections import namedtuple
from functools import reduce
from datetime import datetime, timedelta

# File path to store bookings
BOOKINGS_FILE_PATH = "data/bookings.csv"

# Define the Booking namedtuple with end_time
Booking = namedtuple('Booking', ['booking_id', 'court_id', 'day', 'start_time', 'end_time', 'duration', 'status', 'username'])

# 1. Separating Functions and Data:
# The bookings data is stored separately from the functions that manipulate this data.
class Bookings:
    def __init__(self, file_path=BOOKINGS_FILE_PATH):
        """Initialize the Bookings class with the given file path."""
        self.file_path = file_path
        self.bookings = self.load_bookings()  # 1. Separating functions and data

    def load_bookings(self):
        """Load bookings from the bookings.csv file."""
        bookings = []
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", newline='') as file:
                reader = csv.DictReader(file)
                # 7. Filtering: Only valid and complete booking entries are loaded
                bookings = [
                    Booking(
                        booking_id=int(row['booking_id']),
                        court_id=row['court_id'].strip().upper(),
                        day=row['day'].strip().capitalize(),
                        start_time=row['start_time'].strip().upper(),
                        end_time=row['end_time'].strip().upper(),
                        duration=row['duration'].strip(),
                        status=row['status'].strip().lower(),
                        username=row['username'].strip().capitalize() if row['username'].strip() else None
                    )
                    for row in reader
                    if row['booking_id'].strip() and row['court_id'].strip() and row['day'].strip()
                       and row['start_time'].strip() and row['end_time'].strip()
                ]  # 10. List Comprehensions
        return bookings

    def save_bookings(self):
        """Save all bookings to the bookings.csv file."""
        with open(self.file_path, "w", newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['booking_id', 'court_id', 'day', 'start_time', 'end_time', 'duration', 'status', 'username'])
            # Write each booking
            for booking in self.bookings:
                writer.writerow([
                    booking.booking_id,
                    booking.court_id,
                    booking.day,
                    booking.start_time,
                    booking.end_time,
                    booking.duration,
                    booking.status,
                    booking.username if booking.username else ""
                ])  # 10. List Comprehensions

    def view_user_bookings(self, current_user):
        """Display active bookings for the current user."""
        # 7. Filtering: Only active bookings for the current user are displayed
        user_bookings = list(filter(lambda b: b.username and b.username.lower() == current_user.lower() and b.status == 'active', self.bookings))
        if not user_bookings:
            print("No active bookings found for your account.")
        else:
            print("\nYour Active Bookings:")
            # 10. List Comprehensions: Iterating through user bookings
            [print(f"Booking ID: {booking.booking_id}, Court: {booking.court_id}, Day: {booking.day}, Start Time: {booking.start_time}, End Time: {booking.end_time}, Duration: {booking.duration}") for booking in user_bookings]

    def cancel_user_booking(self, booking_id, current_user):
        """Cancel a booking by booking_id for the current user."""
        # 5. Returning functions: Check if the booking exists and is active
        booking_exists = any(
            booking.booking_id == booking_id and booking.status == 'active' and booking.username and booking.username.lower() == current_user.lower()
            for booking in self.bookings
        )
        if not booking_exists:
            print(f"Booking ID {booking_id} is either not active, does not exist, or does not belong to you.")
            return False

        # 9. Lambdas: Update the booking status using a lambda function
        self.bookings = list(map(
            lambda booking: booking._replace(status="canceled") if booking.booking_id == booking_id and booking.username and booking.username.lower() == current_user.lower() else booking,
            self.bookings
        ))  # 10. List Comprehensions
        print(f"Booking ID {booking_id} has been canceled.")
        self.save_bookings()  # 2. Assigning a function to a variable: save_bookings is called
        return True

    def create_booking(self, court_id, day, start_time, end_time, duration_hours, current_user):
        """Create a new booking for the current user."""
        # Validate court_id
        if court_id.upper() not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            print("Invalid court ID. Please choose between A-H.")
            return False

        # Validate time format
        try:
            datetime.strptime(start_time.upper(), "%I:%M %p")
            datetime.strptime(end_time.upper(), "%I:%M %p")
        except ValueError:
            print("Invalid time format. Please enter time in HH:MM AM/PM format.")
            return False

        # Validate day
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if day.capitalize() not in valid_days:
            print("Invalid day. Please enter a valid day of the week (Monday-Sunday).")
            return False

        # Validate duration: must be positive and multiple of 0.5
        if duration_hours <= 0 or (duration_hours * 2) != int(duration_hours * 2):
            print("Invalid duration. Please enter a positive number in 30-minute increments (e.g., 1, 1.5, 2).")
            return False

        # Check for overlapping bookings using filtering and lambdas
        overlapping = any(
            set(self.calculate_time_slots(start_time, end_time)).intersection(set(self.calculate_time_slots(booking.start_time, booking.end_time)))
            for booking in self.bookings if booking.court_id == court_id.upper() and booking.status == 'active'
        )
        if overlapping:
            print("Cannot create booking due to overlapping time slots.")
            return False

        # Assign a unique booking_id using reducing
        new_booking_id = reduce(lambda acc, b: max(acc, b.booking_id), self.bookings, 0) + 1  # 8. Reducing

        # Create the new booking
        new_booking = Booking(
            booking_id=new_booking_id,
            court_id=court_id.upper(),
            day=day.capitalize(),
            start_time=start_time.upper(),
            end_time=end_time.upper(),
            duration=f"{duration_hours} hour{'s' if duration_hours != 1 else ''}",
            status="active",
            username=current_user.capitalize()
        )
        self.bookings.append(new_booking)
        self.save_bookings()
        print(f"Booking ID {new_booking_id} has been created successfully.")
        return True

    def calculate_time_slots(self, start_time, end_time):
        """Calculate all 30-minute time slots between start_time and end_time."""
        start_dt = datetime.strptime(start_time, "%I:%M %p")
        end_dt = datetime.strptime(end_time, "%I:%M %p")
        slots = []
        while start_dt < end_dt:
            slot_time = start_dt.strftime("%I:%M %p")
            slots.append(slot_time)
            start_dt += timedelta(minutes=30)
        return slots
