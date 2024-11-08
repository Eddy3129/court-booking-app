# users.py

import os

# File to store usernames and passwords
USERS_FILE_PATH = "data/users.txt"

# 1. Separating Functions and Data:
# The data (usernames and passwords) is stored in a file, separate from the functions
# that manipulate this data. Functions such as `load_users` and `save_user` are used 
# to interact with the file data.

# Function to load users from the file
def load_users():
    # 7. Filtering: Only non-empty lines are processed when loading users.
    if os.path.exists(USERS_FILE_PATH):
        with open(USERS_FILE_PATH, "r") as file:
            users = {line.split(",")[0]: line.strip().split(",")[1] for line in file if line.strip()}
            return users
    return {}

# Function to save a new user to the file
def save_user(username, password):
    with open(USERS_FILE_PATH, "a") as file:
        file.write(f"{username},{password}\n")


# 4. Passing Functions as Arguments: The `get_user_input` function handles input prompts.
def sign_up(users):
    username = input("\nEnter a new username: ")
    if username in users:
        print("\nUsername already exists. Please try a different username.")
    else:
        password = input("\nEnter a password: ")
        save_user(username, password)
        users = {**users, username: password}
        print("\nSign up successful!")
    return users

# Log in an existing user
def log_in(users):
    username = input("\nEnter your username: ")
    if username not in users:
        print("\nUsername does not exist. Please try again.")
        return None
    else:
        password = input("\nEnter your password: ")
        if users[username] == password:
            print("\nPassword is correct. You are logged in!")
            return username
        else:
            print("\nPassword is incorrect.")
            return None
        
# 2. Assigning a Function to a Variable: The actions dictionary assigns specific functions to keys for easier access.
def login_action(users):
    return log_in(users)

def signup_action(users):
    sign_up(users)

def quit_action():
    print("\nGoodbye!")
