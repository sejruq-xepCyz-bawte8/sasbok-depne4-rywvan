from anvil_extras.storage import indexed_db
from time import time, sleep
from anvil_extras import non_blocking


class ReaderClass:
    def __init__(self, fn_api):
        self.bookmarks = indexed_db.create_store('cheteme-bookmarks')
        self.api = fn_api

        #current
        self.current_id = None

        #state and back
        self.filters:set = {'публикувани'}
        self.back = 'today'

        self.renders_store = indexed_db.create_store('cheteme-renders')


    def set_current(self, work_id):
        self.current_id = work_id
        return work_id



    def get_work_social_(self, work_id):
        social, success = self.api(api='get_work_social', info=work_id)
        if success:
            return social
        else:
            return None
          

    #memory for the filter
    def set_filters(self, filters:set):
        self.filters = filters
    def get_filters(self):
        return self.filters
    

    #for back in the interface mem for previos page
    def set_back(self, back):
        self.back = back
    def get_back(self):
        return self.back
    

    def save_bookmark(self, page:int, time_reading:float=0, readed:bool=False, readed_pages:bool=False, data=None, content=None):
        self.bookmarks[self.current_id] = {
            'data':data,
            'content':content,
            'page':page,
            'time_reading':time_reading,
            'readed':readed,
            'readed_pages':readed_pages,
            'timestamp': time()
        }

    def get_bookmark(self, work_id):
        return self.bookmarks.get(work_id)
    
    def delete_bookmark(self, work_id):
        del self.bookmarks[work_id]



