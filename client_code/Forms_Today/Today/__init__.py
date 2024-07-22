from ._anvil_designer import TodayTemplate
from anvil import *
from ...App import NAVIGATION, READER, USER, API
from ...Covers_Builder import fill_panel
from anvil.js.window import jQuery as jQ
from anvil.js import window
from anvil_extras import non_blocking
import anvil.server


class Today(TodayTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)

    self.open_form = NAVIGATION.nav_open_form

    READER.set_back("today")


  def form_show(self, **event):
    self.uri = get_url_hash()
    
    if self.uri and len(self.uri) > 3:
      window.history.replaceState('null', '', '/')
      work = READER.get_work_data(work_id=self.uri)
      if work:
        current = READER.set_current(work['work_id'])
        if current:
            open_form('Forms_Reader.Reader')

            

    self.liked_title = jQ('#liked_title')
    self.readed_title = jQ('#readed_title')

    today, success = API.request(api='get_home')
    if not success:
      today, success = API.request(api='get_home')
       
    self.last_10 = today.get('last_10')
    self.chart_liked = today.get('chart_liked')
    self.chart_readed = today.get('chart_readed')
    self.text_liked = today.get('text_liked')
    self.text_readed = today.get('text_readed')
  

    self.liked_title.text(f'Най-харесвани {self.text_liked}')
    self.readed_title.text(f'Най-четени {self.text_readed}')

    #self.deferred_last = non_blocking.defer(self.fill_last, 0)
    #self.deferred_readed = non_blocking.defer(self.fill_readed, 0)
    #self.deferred_liked = non_blocking.defer(self.fill_liked, 0)   

    fill_panel(panel_id='published', works=self.last_10)
    fill_panel(panel_id='readed', works=self.chart_readed)
    fill_panel(panel_id='liked', works=self.chart_liked)
    

  def fill_last(self):
      fill_panel(panel_id='published', works=self.last_10)

  def fill_readed(self):
      fill_panel(panel_id='readed', works=self.chart_readed)

  def fill_liked(self):
      fill_panel(panel_id='liked', works=self.chart_liked)


  def b_work_click(self, **event):
      open_form('Forms_Reader.Reader')


  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')

