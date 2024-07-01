from anvil_extras.storage import indexed_db
import datetime
from time import time
from ..Helpers import hash_args
from random import randint


class EditorClass:
    def __init__(self, fn_asset_get, fn_user_get):
        #self.production = production
        self.store = indexed_db.create_store('cheteme-editor')
        self.user = fn_user_get()
        self.author_id = self.user.get('author_id') if self.user and self.user.get('is_author') else None
        self.get_asset = fn_asset_get
        self.data_template = self.get_asset('json/work_data.json')
        self.all_work_ids = list(self.store)
        self.current_id = None

    def set_new_work(self):
        if not self.author_id: return None
        
        ctime = time()
        work_id = hash_args(randint(1, 1_000_000), ctime, self.author_id) if self.production else str(ctime)
        data = self.data_template
        now = datetime.datetime.now()
        data['title'] = now.strftime("%d-%b-%Y")
        data['ctime'] = ctime
        data['work_id'] = work_id
        data['author_id'] = self.author_id

        work = {
            'data':data,
            'html':'<p></p>'
        }

        self.save_work(work=work)
        self.set_current_id(work_id)
        return work

    def save_work(self, work:dict):
        work_id = work['data']['work_id']
        work['data']['mtime'] = time()
        self.store[work_id] = work
        self.all_work_ids = list(self.store)

    def get_work(self, work_id:str):
        work = self.store.get(work_id)
        return work
    
    def del_work(self, work_id:str):
        del self.store[work_id]
        self.all_work_ids = list(self.store)

    def set_current_id(self, work_id):
        self.current_id = work_id

    def get_current_id(self):
        return self.current_id
    
    def get_current_work(self):
        work = self.get_work(self.current_id)
        return work
