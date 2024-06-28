from anvil_extras.storage import indexed_db

class UserClass:
    def __init__(self):

        self.store = indexed_db.create_store('cheteme-user')
        user = self.store.get('user')
        self.is_user = True if user else False
        self.user_id = user.get('user_id') if user else None
        self.secret = user.get('secret') if user else None
        self.age = user.get('age') if user else None
        self.is_author = user.get('is_author') if user else None
        