#Cheteme Reader
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

    def update_bookmark(self, page:int=None, time_reading:float=None, readed:bool=False, readed_pages:bool=False, data=None, content=None):
        bookmark = self.bookmarks[self.current_id]
        if page:
          bookmark['page'] = page
        if time_reading:
          bookmark['time_reading'] = time_reading
        if readed:
          bookmark['readed'] = readed
        if readed_pages:
          bookmark['readed_pages'] = readed_pages
        if data:
          bookmark['data'] = data
        if content:
          bookmark['content'] = content
          
        self.bookmarks[self.current_id] = bookmark

  
    def get_bookmark(self, work_id):
        return self.bookmarks.get(work_id)
    
    def delete_bookmark(self, work_id):
        del self.bookmarks[work_id]


    def get_work_render(self, work_id, width, heigth):
      if work_id in self.renders_store:
        render = self.renders_store[work_id]
        if render['width'] == width and render['heigth'] == heigth:
          return render
        else:
          return None
    def set_work_render(self, work_id, width, heigth, paginated, pages):
      render = {
        'width':width,
        'heigth':heigth,
        'paginated':paginated,
        'pages':pages,
        'timestamp': time()
      }
      if len(self.renders_store) > 20:
          sorted_items = sorted(self.renders_store.items(), key=lambda item: item[1]['timestamp'])
          to_clean = [k for k, v in sorted_items[:5]]
          for k in to_clean:
            del self.contents_store[k]

      self.renders_store[work_id] = render
