from ._anvil_designer import ChartsTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, READER, WORKS

class Charts(ChartsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    self.charts_panel = jQ('#charts-panel')
    print('цхартс')

  def b_search_click(self, sender, **event):
    self.charts_panel.html('')
    search = self.search_for.text
    found = READER.search(search)
    
    for work in found:
      work_id = work['work_id']
      
      data = READER.get_work_data(work_id)
      
      cover = WORKS.make_cover(data)
      self.charts_panel.append(cover)

  def search_for_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass

