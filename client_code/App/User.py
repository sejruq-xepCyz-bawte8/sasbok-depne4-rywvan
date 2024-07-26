#Cheteme User
from anvil_extras.storage import indexed_db

class UserClass:
    def __init__(self):
        self.store = indexed_db.create_store('cheteme-user')
        self.user:dict = self.store.get('user')
        self.is_author = self.user['is_author']
        
    def get_user(self):
        self.user = self.store.get('user')
        return self.user
    

    def check_is_author(self):
        return self.is_author

    def set_user(self, user:dict):
        
        if user:
            self.store['user'] = user
            return True
        else:
            return False

    def delete_user(self):
        self.store.clear()