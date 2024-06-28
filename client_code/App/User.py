from anvil_extras.storage import indexed_db

class UserClass:
    def __init__(self):

        self.store = indexed_db.create_store('cheteme-user')
        user = self.store.get('user')
        self.user:dict = None
        self.is_user:bool = None
        self.user_id:str = None
        self.secret:str = None
        self.age:int = None
        self.is_author:int = None
        self.set_user(user)
        
    def get_user(self):
        return self.user
    
    def set_user(self, user:dict):
        if user and user.get('user_id'):
            self.user = user
            self.is_user = True if user else False
            self.user_id = user.get('user_id') if user else None
            self.secret = user.get('secret') if user else None
            self.age = user.get('age') if user else None
            self.is_author = user.get('is_author') if user else None
            self.store['user'] = user
