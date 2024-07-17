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
    chart:list = READER.get_chart('today')
    chart_name = "днес"
    if len(chart) < 10:
      chart = READER.get_chart('week')
      chart_name = "през седмицата"
    if len(chart) < 10:
      chart = READER.get_chart('month')
      chart_name = "този месец"

    self.liked_title.text(f'Най-харесвани {chart_name}')
    self.readed_title.text(f'Най-четени {chart_name}')

    
    chart_liked = sorted(chart, key=lambda x: x['l'], reverse=True)
    chart_readed = sorted(chart, key=lambda x: x['r'], reverse=True)
    

    fill_panel(panel_id='published', works=last[:10])
    fill_panel(panel_id='readed', works=chart_readed[:10])
    fill_panel(panel_id='liked', works=chart_liked[:10])



  def b_work_click(self, **event):
      open_form('Forms_Reader.Reader')


  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')

