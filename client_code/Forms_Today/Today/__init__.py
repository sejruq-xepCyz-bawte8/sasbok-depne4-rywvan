#Cheteme Today Form
from ._anvil_designer import TodayTemplate
from anvil import *
from ...App import NAVIGATION, READER, WORKS
from ...Covers_Builder import fill_panel
from anvil.js.window import jQuery as jQ
from anvil.js import window
from anvil_extras import non_blocking



class Today(TodayTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    self.today = []
    self.open_form = NAVIGATION.nav_open_form
    READER.set_back("today")


  def form_show(self, **event):
    #open with link
    self.uri = get_url_hash()
    if self.uri and len(self.uri) > 3:
      window.history.replaceState('null', '', '/')
      work = WORKS.get_work_data(work_id=self.uri)
      if work:
        current = READER.set_current(work['work_id'])
        if current:
            open_form('Forms_Reader.Reader')

    #make today page      
    self.liked_title = jQ('#liked_title')
    self.readed_title = jQ('#readed_title')
    self.paint_today()
    #make page with updates
    today_defer_update = non_blocking.defer(self.paint_today, 2)
    today_repeat_updates = non_blocking.repeat(self.paint_today, 30)
  
  def paint_today(self):
    new_today = WORKS.get_chart_data(chart_id = 'home')
    if new_today != self.today:
      self.today = new_today
      last = non_blocking.defer(self.fill_last, 0)
      readed = non_blocking.defer(self.fill_readed, 0)
      liked = non_blocking.defer(self.fill_liked, 0)   

  def fill_last(self):
      last = self.today.get('last_10')
      fill_panel(panel_id='published', works=last)

  def fill_readed(self):
      text_readed = self.today.get('text_readed')
      self.readed_title.text(f'Най-четени {text_readed}')
      chart_readed = self.today.get('chart_readed')
      fill_panel(panel_id='readed', works=chart_readed)

  def fill_liked(self):
      text_liked = self.today.get('text_liked')
      self.liked_title.text(f'Най-харесвани {text_liked}')
      liked = self.today.get('chart_liked')
      fill_panel(panel_id='liked', works=liked)


  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')

