# filter_courts.py

from datetime import datetime, timedelta
from config import VALID_TIME_SLOTS

# 1. Separating Functions and Data:
# The court availability data is managed separately from the functions that manipulate it.
class CourtFilter:
    def __init__(self):
        """Initialize court availability for all days and courts."""
        self.days = self.initialize_days()  # 1. Separating functions and data

    def initialize_days(self):
        """Initialize courts and their time slots for each day."""
        days = {}
        for day in range(7):  # 0: Monday, 6: Sunday
            # 10. List Comprehensions: Initialize each court with available time slots
            days[day] = {court: self.initialize_time_slots() for court in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']}  # 10. List Comprehensions
        return days

    def initialize_time_slots(self):
        """Initialize all time slots as available."""
        time_slots = {}
        for time_str in VALID_TIME_SLOTS:
            time_slots[time_str] = True  # 10. List Comprehensions
        return time_slots

    def is_day_full(self, day):
        """Check if a specific day is fully booked."""
        # 7. Filtering: Check availability across all courts
        for court, times in self.days[day].items():
            if any(times.values()):
                return False
        return True

    def book_time_slot(self, day, court, time_slot):
        """Mark a specific time slot as booked."""
        if court not in self.days[day]:
            print(f"Invalid court name: {court}. Please choose between A-H.")
            return False

        if time_slot not in self.days[day][court]:
            print(f"Invalid time slot: {time_slot}. Please enter time in HH:MM AM/PM format.")
            return False

        if self.days[day][court][time_slot]:  # Check if time slot is available
            self.days[day][court][time_slot] = False  # Mark as booked
            print(f"Booked court {court} on day {day + 1} at {time_slot}.")
            return True
        else:
            print(f"Court {court} on day {day + 1} at {time_slot} is already booked.")
            return False

    def available_courts(self, day, time_slot):
        """Return a list of available courts for a given day and time slot."""
        # 9. Lambdas: Filtering available courts using a lambda function
        available = list(filter(
            lambda court: self.days[day][court].get(time_slot, False),
            self.days[day]
        ))
        return available  # 10. List Comprehensions

    def check_full_days(self):
        """Print and return a list of fully booked days."""
        # 7. Filtering: Identify fully booked days
        full_days = list(filter(
            lambda day: self.is_day_full(day),
            range(7)
        ))
        full_days = list(map(lambda d: d + 1, full_days))  # 9. Lambdas
        if full_days:
            print(f"Days fully booked: {full_days}")
        else:
            print("No fully booked days.")
        return full_days

    def is_time_slot_available(self, day, court, time_slot):
        """Check if a specific time slot is available for a court on a given day."""
        return self.days.get(day, {}).get(court, {}).get(time_slot, False)

    def synchronize_with_bookings(self, bookings):
        """Update court availability based on existing bookings."""
        for booking in bookings:
            if booking.day and booking.court_id and booking.start_time and booking.end_time:
                day_index = self.get_day_index(booking.day)
                court = booking.court_id.upper()
                start_slot = booking.start_time.upper()
                end_slot = booking.end_time.upper()
                if booking.status == 'active':
                    if day_index is not None and court in self.days[day_index]:
                        slots = self.calculate_time_slots(start_slot, end_slot)
                        for slot in slots:
                            if slot in self.days[day_index][court]:
                                self.days[day_index][court][slot] = False  # Mark as unavailable

    def get_day_index(self, day_name):
        """Convert day name to index."""
        days_mapping = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6
        }
        return days_mapping.get(day_name, None)

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
