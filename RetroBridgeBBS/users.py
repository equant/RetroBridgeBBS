import logging

def validate_user(username, password):
    if username == 'gus': 
        if password == 'x':
            logging.info(f"User {username} authenticated")
            return True
    logging.info(f"Invalid login for user {username}")
    return False

class User(object):
    def __init__(self, username):
        self.username = username
        return
