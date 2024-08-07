"""Models module for the Task Manager application.
   Defines the User class used for user authentication and session management."""
from flask_login import UserMixin

class User(UserMixin):
    """ User class for storing user data and managing authentication.
    
    Attributes:
        id (str): Unique identifier for the user.
        username (str): Username of the user.
        password (str): User's password."""
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        """Returns the unique identifier of the user."""
        return self.id
