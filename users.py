# users.py

import os
import csv
from functools import partial

# File to store usernames and passwords
FILE_PATH = "data/users.csv"

# 1. Separating Functions and Data:
# The data (usernames and passwords) is stored in a CSV file, separate from the functions
# that manipulate this data.

# Function to load users from the CSV file
def load_users():
    """Load users from the CSV file."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", newline='') as file:
            reader = csv.DictReader(file)
            # 10. List Comprehension: Creating a dictionary of users
            users = {row['username'].strip().upper(): row['password'].strip() for row in reader if row['username'].strip()}  # 10. List Comprehension
            return users
    return {}

# Function to save a new user to the CSV file
def save_user(username, password):
    """Save a new user to the CSV file."""
    with open(FILE_PATH, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username.upper(), password])  # 10. List Comprehension

# 4. Passing Functions as Arguments:
def get_user_input(prompt):
    """Get input from the user."""
    return input(prompt)

# Sign up a new user
def sign_up(users):
    """Register a new user."""
    username = get_user_input("\nEnter a new username: ").strip().upper()
    if username in users:
        print("\nUsername already exists. Please try a different username.")
    else:
        password = get_user_input("\nEnter a password: ").strip()
        save_user(username, password)
        users = {**users, username: password}  # 8. Reducing
        print("\nSign up successful!")
    return users

# Log in an existing user
def log_in(users):
    """Authenticate an existing user."""
    username = get_user_input("\nEnter your username: ").strip().upper()
    if username not in users:
        print("\nUsername does not exist. Please try again.")
        return None  # 11. Recursion not used here
    else:
        password = get_user_input("\nEnter your password: ").strip()
        if users[username] == password:
            print("\nPassword is correct. You are logged in!")
            return username  # 5. Returning functions not used here
        else:
            print("\nPassword is incorrect.")
            return None

# 6. Mapping: User choice is mapped to a function in the `actions` dictionary.
def quit_action():
    """Exit the application."""
    print("\nGoodbye!")
    exit(0)

def login_action(users):
    """Assign login function."""
    return log_in(users)

def signup_action(users):
    """Assign signup function."""
    return sign_up(users)

# 2. Assigning a Function to a Variable:
actions = {
    "1": login_action,
    "2": signup_action,
    "3": quit_action
}

def handle_action(choice, users):
    """Handle user action based on choice."""
    action_fn = actions.get(choice)
    if action_fn:
        if choice == "3":
            action_fn()  # Call the quit action and break
        elif choice in ["1", "2"]:
            result = action_fn(users)  # Call login or signup
            if choice == "2":
                users = result  # Update users after signup
            return users
    else:
        print("\nInvalid option. Try again.")
    return users
