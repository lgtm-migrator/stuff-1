import os

welcome_message = '''
Welcome!
NEW - Create a new user
LOGIN - Log in to an existing account
DELETE - Delete an account
'''


def new_user():
    while True:
        print("Creating New User... ")
        user = input("Username\n> ")
        password = input("Password\n> ")
        password1 = input("Confirm Password\n> ")
        if password == password1:
            print("Account Created Successfully!")
            file = open(user + ".txt", "w")
            file.write(user + ":" + password)
            file.close()
            break
        else:
            print("Passwords don't match!")


def returning_user():
    while True:
        print("Logging in... ")
        user = input("Username\n> ")
        password = input("Password\n> ")
        file = open(user + ".txt", "r")
        data = file.readline()
        file.close()
        if data == user + ":" + password:
            print("Welcome")
            break
        else:
            print("Incorrect Username/Password... Try Again")


def remove_user():
    while True:
        print("You are about to delete a user... This cannot be undone")
        user = input("Username\n> ")
        password = input("Password\n> ")
        file = open(user + ".txt", "r")
        data = file.readline()
        file.close()
        if data == user + ":" + password:
            os.remove(f"{user}.txt")
            print("User Deleted Successfully")
            break
        else:
            print("Invalid Credentials, Quitting...")


if __name__ == "__main__":
    print(welcome_message)
    welcome = input("> ").lower()

while __name__ == "__main__":
    if "new" in welcome:
        new_user()
        break
    elif "login" in welcome:
        returning_user()
        break
    elif "delete" in welcome:
        remove_user()
        break
    else:
        print("Invalid Input... Try Again!")
        break
