# bookings.py

"""
Functional Programming Concepts Demonstrated:
1. Separating functions and data 
4. Passing functions as arguments 
6. Mapping 
7. Filtering 
8. Reducing
9. Lambdas
"""

import os
import csv
from collections import namedtuple
from functools import reduce

BOOKINGS_FILE_PATH = "data/bookings.csv"

# Define the immutable Booking namedtuple
Booking = namedtuple('Booking', ['booking_id', 'court_id', 'time', 'duration', 'status', 'username'])

# 1. Separating functions and data: Booking data is stored externally in a CSV file, and functions manipulate this data.
def load_bookings():
    """
    Load bookings from the BOOKINGS_FILE_PATH.
    Returns a list of Booking namedtuples.
    """
    bookings = []
    if os.path.exists(BOOKINGS_FILE_PATH):
        with open(BOOKINGS_FILE_PATH, "r", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                booking = Booking(
                    booking_id=int(row['booking_id']),
                    court_id=row['court_id'],
                    time=row['time'],
                    duration=row['duration'],
                    status=row['status'],
                    username=row['username']
                )
                bookings.append(booking)
    return bookings

def save_bookings(bookings):
    """
    Save all bookings to the BOOKINGS_FILE_PATH.
    """
    with open(BOOKINGS_FILE_PATH, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['booking_id', 'court_id', 'time', 'duration', 'status', 'username'])
        for booking in bookings:
            writer.writerow([
                booking.booking_id,
                booking.court_id,
                booking.time,
                booking.duration,
                booking.status,
                booking.username
            ])

# 8. Reducing: Group bookings by their status ('active' or 'canceled').
def group_by_status(bookings):
    """
    Group bookings by their status using reduce.
    Returns a dictionary with status as key and list of bookings as value.
    """
    def reducer(acc, booking):
        acc[booking.status].append(booking)
        return acc

    initial_acc = {'active': [], 'canceled': []}
    return reduce(reducer, bookings, initial_acc)

# 7. Filtering: Select bookings that are active and belong to the current user.
def view_user_bookings(bookings, current_user):
    """
    View active bookings associated with the current_user.
    """
    # 9. Lambdas: Define a lambda function to filter bookings.
    user_bookings = list(filter(lambda b: b.username == current_user and b.status == 'active', bookings))
    if not user_bookings:
        print("No active bookings found for your account.")
    else:
        print("\nYour Active Bookings:")
        # 6. Mapping: Iterate over filtered bookings to display them.
        for booking in user_bookings:
            print(f"Booking ID: {booking.booking_id}, Court: {booking.court_id}, Time: {booking.time}, Duration: {booking.duration}")

# 4. Passing functions as arguments: Use map with a lambda to update booking status.
def cancel_user_booking(bookings, booking_id, current_user):
    """
    Cancel a booking by booking_id for the current_user.
    Returns the updated bookings list.
    """
    # 7. Filtering: Check if the booking exists, is active, and belongs to the user.
    booking_exists = any(
        booking.booking_id == booking_id and booking.status == 'active' and booking.username == current_user
        for booking in bookings
    )
    if not booking_exists:
        print(f"Booking ID {booking_id} is either not active, does not exist, or does not belong to you.")
        return bookings

    # 6. Mapping: Use map to create updated bookings with the specified booking canceled.
    updated_bookings = list(map(
        lambda booking: booking._replace(status="canceled") if booking.booking_id == booking_id and booking.username == current_user else booking,
        bookings
    ))
    print(f"Booking ID {booking_id} has been canceled.")
    return updated_bookings




