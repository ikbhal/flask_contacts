import string
from random import random


class User:
    def __init__(self, id, name, email, password, is_verified=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.is_verified = is_verified

class Contact:
    def __init__(self, id, user_id, name, mobile):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.mobile = mobile

class VerificationPin:
    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin

# List to store users
users = []

# List to store contacts
contacts = []

# List to store verification pins
verification_pins = []

def generate_verification_pin():
    # Generate a 6-digit random pin
    pin = ''.join(random.choices(string.digits, k=6))
    return pin

# User registration API endpoint
def register_user(name, email, password):
    # Check if email is already registered
    for user in users:
        if user.email == email:
            return None

    # Generate a unique user ID
    user_id = len(users)

    # Create a new user instance
    user = User(user_id, name, email, password)

    # Generate a verification pin
    pin = generate_verification_pin()

    # Create a new verification pin instance
    verification_pin = VerificationPin(user_id, pin)

    # Add the user and verification pin to the respective lists
    users.append(user)
    verification_pins.append(verification_pin)

    # Send email verification to the user's email address (implementation omitted)

    # Return the newly created user
    return user

# User login function
def login_user(email, password):
    # Find the user with matching email and password
    for user in users:
        if user.email == email and user.password == password:
            return user

    # Return None if no matching user found
    return None

# Function to retrieve contacts for a given user
def get_user_contacts(user_id):
    # Filter contacts based on user ID
    user_contacts = [contact for contact in contacts if contact.user_id == user_id]
    return user_contacts

# Function to add a contact for a given user
def add_user_contact(user_id, name, mobile):
    # Generate a unique contact ID
    contact_id = len(contacts)

    # Create a new contact instance
    contact = Contact(contact_id, user_id, name, mobile)

    # Add the contact to the list of contacts
    contacts.append(contact)

    # Return the newly created contact
    return contact

# Function to delete a contact for a given user
def delete_user_contact(user_id, contact_id):
    # Find the contact with matching user ID and contact ID
    for contact in contacts:
        if contact.user_id == user_id and contact.id == contact_id:
            contacts.remove(contact)
            return True

    # Return False if no matching contact found
    return False
