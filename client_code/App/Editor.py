import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from anvil_extras.storage import indexed_db
import datetime
from time import time
from ..Helpers import hash_args
from random import randint


class EditorClass:
    def __init__(self, fn_asset_get, fn_user_get):
        #self.production = production
        self.store = indexed_db.create_store('cheteme-editor')
        self.get_asset = fn_asset_get
        self.get_user = fn_user_get
        self.data_template = self.get_asset('json/work_data.json')
        
        #current
        self.data = None
        self.content = None
        self.work_id = None

    def get_draft_ids(self):
        return list(self.store)

    def get_work_data(self, work_id:str):
        work = self.store.get(work_id)
        if work:
            return work['data']
        else:
            return None

    def set_new_work(self):
        user = self.get_user()
        if not user['author_id']:
            return False
        
        ctime = time()
        try:
            work_id = hash_args(randint(1, 1_000_000), ctime, self.author_id)
        except:
            work_id = str(ctime)

        data = self.data_template
        now = datetime.datetime.now()
        data['title'] = now.strftime("%d-%b-%Y")
        data['ctime'] = ctime
        data['work_id'] = work_id
        data['author_id'] = user['author_id']

        self.store[work_id] = {
            'data':data,
            'content':'{}'
        }

        self.set_current(work_id)

        return True

    def save_work(self):
        if self.work_id and self.data and self.content:
            self.data['mtime'] = time()
            self.store[self.work_id] = {
                'data':self.data,
                'content': self.content}
            return True
        else:
            return False

    
    def del_work(self, work_id:str):
        del self.store[work_id]
       

    def set_current(self, work_id):
        work = self.store.get(work_id)
        if work:
            self.work_id = work_id
            self.data = work['data']
            self.content = work['content']
            return True
        else:
            self.work_id = None
            self.data = None
            self.content = None
            return False


    def set_profile_work(self):
        user = self.get_user()
        if not user['author_id']: return False

        if self.store.get(user['author_id']):
            return self.set_current(work_id=user['author_id'])
        else:
            ctime = time()
            data = self.data_template
            data['title'] = "Автор"
            data['ctime'] = ctime
            data['work_id'] = user['author_id']
            data['author_id'] = user['author_id']
            data['uri'] = user['author_uri']
            self.store[user['author_id']] = {
                'data':data,
                'content':'{}'
            }

            self.set_current(user['author_id'])

            return True