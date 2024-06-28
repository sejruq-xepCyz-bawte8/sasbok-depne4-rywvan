from ._anvil_designer import SettingsTemplate
from anvil import *
from ...App import NAVIGATION

class Settings(SettingsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.open_form

  def form_show(self, **event):
    pass

  def test(self, sender, **event):
    print('nac cl test')

  def tabs_tab_click(self, tab_index, tab_title, **event_args):
    """This method is called when a tab is clicked"""
    pass

