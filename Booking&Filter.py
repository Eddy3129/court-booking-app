from datetime import datetime, timedelta

class CourtBookingSystem:
    def __init__(self):
        # Initialize 7 days with 8 courts each, with time slots from 8 AM to 10 PM in 1-hour intervals
        self.days = self.initialize_days()

    def initialize_days(self):
        # Create a structure with 7 days, each with 8 courts, each with hourly time slots
        days = {}
        for day in range(7):  # Assume day 0 is Monday, day 6 is Sunday
            days[day] = {court: self.initialize_time_slots() for court in range(8)}
        return days

    def initialize_time_slots(self):
        # Generates availability for each hour from 8:00 to 22:00
        start_time = datetime.strptime("08:00", "%H:%M")
        end_time = datetime.strptime("22:00", "%H:%M")
        time_slots = {}
        
        current_time = start_time
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            time_slots[time_str] = True  # True means available
            current_time += timedelta(hours=1)
        
        return time_slots

    def is_day_full(self, day):
        # Check if all time slots for all courts are booked for a particular day
        for court, times in self.days[day].items():
            if any(times.values()):  # If any time slot is available, day is not full
                return False
        return True

    def book_time_slot(self, day, court, time_slot):
        # Book a specific court at a given time on a specific day if available
        if self.days[day][court][time_slot]:  # Check if time slot is available
            self.days[day][court][time_slot] = False  # Mark as booked
            print(f"Booked court {court + 1} on day {day + 1} at {time_slot}.")
        else:
            print(f"Court {court + 1} on day {day + 1} at {time_slot} is already booked.")

    def available_courts(self, day, time_slot):
        # Get available courts for a specific day and time slot
        available = [court + 1 for court, times in self.days[day].items() if times[time_slot]]
        return available

    def check_full_days(self):
        # Check all days at program start to see if they are fully booked
        full_days = [day + 1 for day in range(7) if self.is_day_full(day)]
        if full_days:
            print(f"Days fully booked: {full_days}")
        else:
            print("No fully booked days.")

def main():
    booking_system = CourtBookingSystem()
    booking_system.check_full_days()

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    while True:
        print("\nOptions:")
        print("1. Check available courts for a day and time slot")
        print("2. Book a court")
        print("3. Check fully booked days")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            # Option to check available courts
            day = int(input("Enter the day (1 for Monday, 7 for Sunday): ")) - 1
            time_slot = input("Enter the time slot (e.g., 08:00 to 21:00): ")
            available_courts = booking_system.available_courts(day, time_slot)
            if available_courts:
                print(f"Available courts on {days_of_week[day]} at {time_slot}: {available_courts}")
            else:
                print(f"No available courts on {days_of_week[day]} at {time_slot}.")
                
        elif choice == '2':
            # Option to book a court
            day = int(input("Enter the day (1 for Monday, 7 for Sunday): ")) - 1
            court = int(input("Enter the court number (1-8): ")) - 1
            time_slot = input("Enter the time slot (e.g., 08:00 to 21:00): ")
            booking_system.book_time_slot(day, court, time_slot)

        elif choice == '3':
            # Option to check fully booked days
            booking_system.check_full_days()

        elif choice == '4':
            print("Exiting the program.")
            break

        else:
            print("Invalid option. Please choose a valid option.")

# Run the program
if __name__ == "__main__":
    main()
