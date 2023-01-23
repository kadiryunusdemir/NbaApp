from flask import current_app
from flask_login import UserMixin

# Flask-Login assumes that there will be a unique string value for identifying each user.
# In most cases, this will be the string value of the database id number for a user. 
# In our example, we will use the username for this purpose. 
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active

def get_user(user_id):
    password = current_app.config["PASSWORDS"].get(user_id)
    user = User(user_id, password) if password else None
    if user is not None:
        user.is_admin = user.username in current_app.config["ADMIN_USERS"]
    return user