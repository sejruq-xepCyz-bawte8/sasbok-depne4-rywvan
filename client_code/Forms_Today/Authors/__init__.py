from ._anvil_designer import AuthorsTemplate
from anvil import *
from ...App import NAVIGATION, READER, WORKS
from ...Covers_Builder import fill_panel
from time import sleep

class Authors(AuthorsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    READER.set_back("authors")
    
    self.open_form = NAVIGATION.nav_open_form
    

  def form_show(self, **event):
    
    authors = WORKS.get_chart_data(chart_id = 'authors')
      
    fill_panel(panel_id='authors-panel', works=authors)

  def open_work(self, sender, **event):

    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')

  def b_search_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

