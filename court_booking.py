import os

# File to store usernames and passwords
FILE_PATH = "users.txt"

# 1. Separating Functions and Data:
# The data (usernames and passwords) is stored in a file, separate from the functions
# that manipulate this data. Functions such as `load_users` and `save_user` are used 
# to interact with the file data.

# Function to load users from the file
def load_users():
    # 7. Filtering: Only non-empty lines are processed when loading users.
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            users = {line.split(",")[0]: line.strip().split(",")[1] for line in file if line.strip()}  # 10. List Comprehension
            return users
    return {}

# Function to save a new user to the file
def save_user(username, password):
    with open(FILE_PATH, "a") as file:
        file.write(f"{username},{password}\n")

# 4. Passing Functions as Arguments: The `get_user_input` function handles input prompts.
def get_user_input(prompt):
    return input(prompt)

# Sign up a new user
def sign_up(users):
    username = input("\nEnter a new username: ")
    if username in users:
        print("\nUsername already exists. Please try a different username.")
    else:
        password = input("\nEnter a password: ")
        save_user(username, password)
        users[username] = password  # Update the users dictionary immediately
        print("\nSign up successful!") 
        
# Log in an existing user
def log_in(users):
    username = input("\nEnter your username: ")
    if username not in users:
        print("\nUsername does not exist. Please try again.")
        return False  # Return False if login fails
    else:
        password = input("\nEnter your password: ")
        if users[username] == password:
            print("\nPassword is correct. You are logged in!")  # Added blank lines
            return True  # Return True to indicate successful login
        else:
            print("\nPassword is incorrect.")  # Added blank lines
            return False  # Return False if login fails

# 2. Assigning a Function to a Variable: The actions dictionary assigns specific functions to keys for easier access.
def login_action(users):
    return log_in(users)

def signup_action(users):
    sign_up(users)

def quit_action():
    print("\nGoodbye!")

# Main function
def main():
    # Load existing users
    users = load_users()
    
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
        # Display menu options
        print("\nChoose an option:")  # Added blank lines
        print("1. Login")
        print("2. Signup")
        print("3. Quit")
        
        # 6. Mapping: User choice is mapped to a function in the `actions` dictionary.
        choice = get_user_input("Enter your choice (1, 2, or 3): ")
        
        # Retrieve and execute the function based on the user's choice
        action_fn = actions.get(choice)  # 2. Assigning function to variable
        if action_fn:
            if choice == "3":
                action_fn()  # Call the quit action and break
                break
            elif choice == "1":
                if action_fn(users):  # Call the login action with users as argument
                    break  # End the loop after successful login
            else:
                action_fn(users)  # Call signup with users as argument
        else:
            print("\nInvalid option. Try again.")

if __name__ == "__main__":
    main()