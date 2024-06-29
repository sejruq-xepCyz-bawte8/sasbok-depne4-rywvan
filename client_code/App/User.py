from anvil_extras.storage import indexed_db

class UserClass:
    def __init__(self):

        self.store = indexed_db.create_store('cheteme-user')
        user = self.store.get('user')
        self.user:dict = None
        self.is_user:bool = None

        #db
        self.user_id:str = None
        self.secret:str = None
        self.age:int = None
        self.code:str = None
        self.is_author:int = None
        self.is_registred:int = None
        self.author_id:int = None

        self.set_user(user)
        
    def get_user(self):
        return self.user
    
    def check_is_author(self):
        return self.is_author

    def set_user(self, user:dict):
        if user and user.get('user_id'):
            self.user = user
            self.is_user = True

            self.user_id = user.get('user_id')
            self.secret = user.get('secret')
            self.age = user.get('age')
            self.is_author = user.get('is_author')
            self.is_registred = user.get('is_registred')
            self.author_id = user.get('author_id')

            self.store['user'] = user

    def delete_user(self):
        self.store.clear()