#Cheteme Form Author Reader
from ._anvil_designer import AuthorCoverTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from anvil.js.window import document
from anvil_extras import non_blocking
from ...App import NAVIGATION, API, USER, READER, WORKS

from time import time

#get_author_published

class AuthorCover(AuthorCoverTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.nav_open_form

    api = 'get_author_published'
    self.work_id = READER.current_id
    self.work_data =  WORKS.get_work_data(self.work_id)
    self.author_id = self.work_data['author_id']
    
    self.published_works, _ = API.request(api=api, info=self.author_id)
    
    self.bookmark = READER.get_bookmark(READER.current_id)



  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')


  def parse_works(self):
    self.panel.html('')
    for work in self.published_works:
      work_id = work['work_id']
      data = WORKS.get_work_data(work_id=work_id)
      if data:
        cover = WORKS.make_cover(work_id)
        self.panel.append(cover)

  def form_show(self, **event):
    #Sidebars
    self.toc = []
    self.sidebar_toc = jQ('#reader-sidebar-toc')
    self.sidebar_toc.toggle()
    self.sidebar_social = jQ('#reader-sidebar-social')
    self.sidebar_social.toggle()
    
    self.panel = jQ('#published-panel')
    jQ('#title').text(self.work_data['title'])
    self.parse_works()

    #back = jQ('#today')
    #back.attr('id', READER.get_back())

    self.bookmark_icon = jQ('#bookmark')
    if self.bookmark:
       self.bookmark_icon.addClass('active')

    self.scroling_pages_info = None




    #build panels
    toc = non_blocking.defer(self.build_toc, 0)
    social = non_blocking.defer(self.build_social, 0)
 


  def bookmark_click(self, sender, *event):
    READER.save_bookmark(page=1, time_reading=1, readed=True, readed_pages=1)
    self.bookmark_icon.toggleClass('active')
    if self.bookmark:
      READER.delete_bookmark(READER.current_id)
    

  def toc_click(self, sender, *event):
    self.sidebar_social.hide()
    self.sidebar_toc.toggle()

  #no full check for readed for author as works
  def social_click(self, sender, *event):
    self.sidebar_toc.hide()
    self.sidebar_social.toggle()


  def build_toc(self):
    for t in self.toc:
      link = Link()
      text = t['text'] if t['h'] == 1 else f"  {t['text']}"
      if len(text) > 20 : text = text[:19] + "+"
      pagen = str(t['page'])
      dots = '.' * (24 - len(text) - len(pagen))
      link.text = '{}{}{}'.format(text, dots, pagen)
      link.font = 'Courier New, monospace'
      link.page = t['page']
      link.add_event_handler('click', self.toc_h1_click)
      self.add_component(link, slot='toc')

    self.add_component(Spacer(), slot='toc')
    words = Label(text=f"{self.work_data['words']} думи")
    words.font = 'Courier New, monospace'
    self.add_component(words, slot='toc')


  def toc_h1_click(self, **event):
    pass


  def build_social(self):
    social, success = API.request(api='get_work_social', info=self.work_id)
    if social and success:
      for comment in social['comments']:
        label = Label(text=comment)
        self.add_component(label, slot='social-comments')
      self.l_likes.text = social.get('liked')
      self.tb_comment.text = social.get('me')
      if social.get('me_liked'):
         self.engage_liked.icon = "fa:heart"



  def engage(self, engage:str=None, **event):
     if event['sender'] == self.engage_liked:
        engage = 'engage_liked'
     elif event['sender'] == self.engage_comment:
        engage = 'engage_comment'
  
     data = {
        'genre':READER.data['genres'][2],
        'comment':self.tb_comment.text,
        'author_id': READER.data['author_id'],
        'age': READER.data['age']
     }
     eresult, success = API.request(api=engage, info=READER.current_id, data=data)
     

     if success == 200 and engage == 'engage_liked':
        self.engage_liked.icon = "fa:heart"
     elif success == 200 and engage == 'engage_comment':
        self.engage_comment.icon = "fa:comment"
