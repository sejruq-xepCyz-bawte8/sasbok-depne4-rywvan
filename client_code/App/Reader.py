
from anvil_extras.storage import indexed_db


class ReaderClass:
    def __init__(self, fn_api):
        self.store = indexed_db.create_store('cheteme-reader')
        self.api = fn_api
        self.last = []
        self.authors = []
        self.update_last()
        self.update_authors()

        self.current_id = None
        self.data = None
        self.content = None

    def set_current(self, work_id):
        work = self.store.get(work_id)
        if work:
            self.work_id = work_id
            self.data = work['data']
            self.content = work['content']
            return True
        
        data = self.get_work_data(work_id)
        content = self.get_work_content(work_id)

        if data and content:
            self.work_id = work_id
            self.data = data
            self.content = content
            return True
        else:
            self.work_id = None
            self.data = None
            self.content = None
            return False



    def update_last(self):
        results, success = self.api(api='get_last')
        print('reader:', results)
        self.last = results

    def update_authors(self):
        results, success = self.api(api='get_authors')
        self.authors = results

    def get_work_data(self, work_id):
        print('reader get_work_data:', work_id)
        data, success = self.api(api='get_work_data', info=work_id)
        
        if success:
            return data
        else:
            return None

    def get_work_content(self, work_id):
        content, success = self.api(api='get_work_content', info=work_id)
        if success:
            return content
        else:
            return None
        
    def search(self, search, is_author:bool=None):
        data = {
            'search':search,
            'is_author':is_author
        }
        content, success = self.api(api='search', data=data)
        if success:
            return content
        else:
            return None