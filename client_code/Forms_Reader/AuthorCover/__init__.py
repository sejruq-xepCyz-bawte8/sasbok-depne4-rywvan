from ._anvil_designer import AuthorCoverTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, API, USER, READER, WORKS

#get_author_published

class AuthorCover(AuthorCoverTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.nav_open_form

    api = 'get_author_published'
    
    self.author_id = READER.data['author_id']
    self.published_works, _ = API.request(api=api, info=self.author_id)
    
  def form_show(self, **event):
    self.panel = jQ('#published-panel')
    jQ('#title').text(READER.data['title'])
    self.parse_works()
    
    
    

  def parse_works(self):
    self.panel.html('')
    for work in self.published_works:
      work_id = work['work_id']
      data = READER.get_work_data(work_id=work_id)
      if data:
        cover = WORKS.make_cover(data)
        self.panel.append(cover)

  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')


  def bookmark_click(self, sender, *event):
    READER.save_bookmark(page=1, time_reading=1, readed=True, readed_pages=1)
    self.bookmark_icon.toggleClass('active')
    if self.bookmark:
      READER.delete_bookmark(READER.current_id)