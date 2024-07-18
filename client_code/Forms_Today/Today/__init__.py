from ._anvil_designer import TodayTemplate
from anvil import *
from ...App import NAVIGATION, READER
from ...Covers_Builder import fill_panel
from anvil.js.window import jQuery as jQ
from anvil.js import window

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

    today:list = READER.get_today()
    last_10 = today.get('last_10')
    chart_liked = today.get('chart_liked')
    chart_readed = today.get('chart_readed')
    text_liked = today.get('text_liked')
    text_readed = today.get('text_readed')
  


    fill_panel(panel_id='published', works=last_10)
    fill_panel(panel_id='readed', works=chart_readed)
    fill_panel(panel_id='liked', works=chart_liked)

    
    self.liked_title.text(f'Най-харесвани {text_liked}')
    self.readed_title.text(f'Най-четени {text_readed}')

    




  def b_work_click(self, **event):
      open_form('Forms_Reader.Reader')


  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')

