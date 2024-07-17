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

    last:list = READER.get_last()
    fill_panel(panel_id='published', works=last[:10])

    chart_today:list = READER.get_chart('today')
    
    chart_liked = [c for c in chart_today if c['l'] > 0]
    chart_readed = [c for c in chart_today if c['r'] > 0]
    text_liked = 'днес'
    text_readed = 'днес'

    if len(chart_liked) < 2 or len(chart_readed) < 2:
      chart_week:list = READER.get_chart('week')

    if len(chart_liked) < 2:
      chart_liked = [c for c in chart_week if c['l'] > 0]
      text_liked = 'през седмицата'


    if len(chart_readed) < 2:
      chart_readed = [c for c in chart_week if c['r'] > 0]
      text_readed = 'през седмицата'


    if len(chart_liked) < 2 or len(chart_readed) < 2:
      chart_month:list = READER.get_chart('month')


    if len(chart_liked) < 2:
      chart_liked = [c for c in chart_month if c['l'] > 0]
      text_liked = 'през месеца'


    if len(chart_readed) < 2:
      chart_readed = [c for c in chart_month if c['r'] > 0]
      text_readed = 'през месеца'


    chart_liked = sorted(chart_liked, key=lambda x: x['l'], reverse=True)
    chart_readed = sorted(chart_readed, key=lambda x: x['r'], reverse=True)


    self.liked_title.text(f'Най-харесвани {text_liked}')
    self.readed_title.text(f'Най-четени {text_readed}')

    
  
    fill_panel(panel_id='readed', works=chart_readed[:10])
    fill_panel(panel_id='liked', works=chart_liked[:10])



  def b_work_click(self, **event):
      open_form('Forms_Reader.Reader')


  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')

