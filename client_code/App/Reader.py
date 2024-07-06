from anvil_extras.storage import indexed_db
from time import time
from datetime import datetime, timedelta
from anvil_extras.storage import indexed_db

class ReaderClass:
    def __init__(self, fn_api):
        self.bookmarks = indexed_db.create_store('cheteme-bookmarks')
        self.api = fn_api

        self.current_id = None
        self.data = None
        self.content = None

   
        self.works:dict = {}
        self.charts:dict = {}


    def set_current(self, work_id):
        data = self.get_work_data(work_id)
        content = self.get_work_content(work_id)
        if data and content:
            self.current_id = work_id
            self.data = data
            self.content = content
            return True
        else:
            self.current_id = None
            self.data = None
            self.content = None
            return False


    def get_last(self):
        return self.parse_chart(api='get_last')


    def get_authors(self):
        return self.parse_chart(api='get_authors')

    def parse_chart(self, api, info=None, data=None):

        chart_id = api if not info else f'{api}-{info}'

        if self.charts.get(chart_id) and time() - self.charts[chart_id]['timestamp'] < 3600:
            return self.charts[chart_id]['results']
        results, success = self.api(api=api, info=info, data=data)
        if results and success:
            self.charts[chart_id] = {
                'results':results,
                'timestamp':time()
            }
            return results
        else:
            return [] 



    def get_work_data(self, work_id):
        work = self.works.get(work_id)

        if work and work.get('data'):
            return work['data']
        
        work = self.bookmarks.get(work_id)
        if work and work.get('data'):
            return work['data']

        data, success = self.api(api='get_work_data', info=work_id)
        
        if data and success:
            self.works[work_id] = {
                'data':data
            }
            return data
        else:
            return None


    def get_work_content(self, work_id):
        work = self.works.get(work_id)
        if work and work.get('content'):
            return work['content']

        work = self.bookmarks.get(work_id)
        if work and work.get('content'):
            return work['content']
        
        content, success = self.api(api='get_work_content', info=work_id)
        if success:
            if not self.works.get(work_id):
                data, success = self.api(api='get_work_data', info=work_id)
            else:
                data = self.works[work_id]['data']

            self.works[work_id] = {
                'data':data,
                'content':content
            }

            return content
        else:
            return None
        
    def search(self, search, is_author:bool=None):
        data = {
            'search':search,
            'is_author':is_author
        }

        return self.parse_chart(api='search', data=data)

        

    def get_chart(self, time):

        return self.parse_chart(api='get_chart', info=time)


    
