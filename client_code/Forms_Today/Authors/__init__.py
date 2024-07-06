from ._anvil_designer import AuthorsTemplate
from anvil import *
from ...App import NAVIGATION, READER
from ...Covers_Builder import fill_panel

class Authors(AuthorsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.nav_open_form
    

  def form_show(self, **event):
    fill_panel(panel_id='authors-panel', works=READER.authors)

  def open_work(self, sender, **event):
    print(sender.attr('id'))
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')

  def b_search_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

