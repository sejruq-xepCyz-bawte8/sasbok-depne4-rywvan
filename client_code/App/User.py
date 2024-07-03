from anvil_extras.storage import indexed_db

class UserClass:
    def __init__(self):
        self.store = indexed_db.create_store('cheteme-user')
        user:dict = self.store.get('user')
        if user:
            self.is_user = True
            self.user_id = user['user_id']
            self.secret = user['secret']
            self.age = user['age']
            self.is_registred = user['is_registred']
            self.is_author = user['is_author']
            self.author_id = user['author_id']
        else:
            self.is_user = False

        
    def get_user(self):
        return self.user
    
    def check_is_author(self):
        return self.is_author

    def set_user(self, user:dict):
        
        if user and user.get('user_id'):
            self.user = user
            self.is_user = True
            self.user_id = user['user_id']
            self.secret = user['secret']
            self.age = user['age']
            self.is_author = user['is_author']
            self.is_registred = user['is_registred']
            self.author_id = user['author_id']
        
        self.store['user'] = user

    def delete_user(self):
        self.store.clear()