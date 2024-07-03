import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from anvil_extras.storage import indexed_db

class UserClass:
    def __init__(self):
        self.store = indexed_db.create_store('cheteme-user')
        self.user:dict = self.store.get('user')
        self.is_author = self.user['is_author']
        #if user:
        #    self.is_user = True
        #    self.user_id = user['user_id']
        #    self.secret = user['secret']
        #    self.age = user['age']
        #    self.is_registred = user['is_registred']
        #    self.is_author = user['is_author']
        #    self.author_id = user['author_id']
        #    self.author_uri = user['author_uri']
        #else:
        #    self.is_user = False

        
    def get_user(self):
        return self.user
    


    def check_is_author(self):
        return self.is_author

    def set_user(self, user:dict):
        
        #if user and user.get('user_id'):
            #self.user = user
            #self.is_user = True
            #self.user_id = user['user_id']
            #self.secret = user['secret']
            #self.age = user['age']
            #self.is_author = user['is_author']
            #self.is_registred = user['is_registred']
            #self.author_id = user['author_id']
            #self.author_uri = user['author_uri']
        if user:
            self.store['user'] = user
            return True
        else:
            return False

    def delete_user(self):
        self.store.clear()