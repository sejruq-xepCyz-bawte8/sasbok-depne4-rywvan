from anvil_extras.storage import indexed_db
from time import time, sleep
from anvil_extras import non_blocking


class ReaderClass:
    def __init__(self, fn_api):
        self.bookmarks = indexed_db.create_store('cheteme-bookmarks')
        self.api = fn_api

        #current
        self.current_id = None
        self.data = None
        self.content = None


        #state and back
        self.filters:set = {'публикувани'}
        self.back = 'today'
   
        #cache
        self.works:dict = {}
        self.charts:dict = {}

        self.freq = {
            'get_chart_today': 2, #600
            'get_chart_week': 3600,
            'get_chart_month': 7200,
            'search': 3600,
        }

        self.beats_update = non_blocking.repeat(self.update_charts, 60)
        self.bookmarks_update = non_blocking.defer(self.update_bookmarks, 0)


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
        if not data and not info:
            chart_id = api
        elif not data and info:   
            chart_id = f'{api}{info}'
        elif api=='search':
            is_author = 1 if data['is_author'] else 0
            chart_id = f"{api}{data['search'].strip()}{is_author}"
    
        else:
            return []


        freq = self.freq.get(chart_id)
        if not freq: freq = 3600

        chart = self.charts.get(chart_id)

        if chart:
            delta = time() - chart['timestamp']
            if delta < freq:
                return chart['results']
        
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
            self.works[work_id] = {'data':data}
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

        if work:
            work['content'] = content
            self.works[work_id] = work
        
        if success:
            return content
        else:
            return None
        

    def get_work_social(self, work_id):
        work = self.works.get(work_id)
        if work and work.get('social') and work.get('stimestamp'):
            if time() - work['stimestamp'] < 600: #10 min cache
                return work['social']

        social, success = self.api(api='get_work_social', info=work_id)

        if work:
            work['social'] = social
            work['stimestamp'] = time()
            self.works[work_id] = work
        
        if success:
            return social
        else:
            return None


    def search(self, search, is_author:bool=None):
        data = {
            'search':search,
            'is_author':is_author
        }
        #results, success = self.api(api='search', data=data)
        #return results
        return self.parse_chart(api='search', data=data)

        

    def get_chart(self, time):
        #check bookmarks for new vers
        chart = self.parse_chart(api='get_chart', info=time)
        return chart

    def update_charts(self):
     
        self.parse_chart(api='get_last')
        self.parse_chart(api='get_chart', info='month')
        self.parse_chart(api='get_chart', info='week')
        self.parse_chart(api='get_chart', info='today')
       
        
    def update_bookmarks(self):
        bookmark_ids = list(self.bookmarks)
        for work_id in bookmark_ids:
            work_b = self.bookmarks.get(work_id)
            data, success_d = self.api(api='get_work_data', info=work_id)
            if data and data['ver'] > work_b['data']['ver']:
                work_b['data'] = data
                content, success_c = self.api(api='get_work_content', info=work_id)
                if content:
                    work_b['content'] = content
                work_b['timestamp'] = time()
                self.bookmarks[work_id] = work_b

            sleep(2)


    def set_filters(self, filters:set):
        self.filters = filters
    def get_filters(self):
        return self.filters
    
    def set_back(self, back):
        self.back = back
    def get_back(self):
        return self.back
    

    def save_bookmark(self, page:int, time_reading:float=0, readed:bool=False, readed_pages:bool=False):
        self.bookmarks[self.current_id] = {
            'data':self.data,
            'content':self.content,
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