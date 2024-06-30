from ._anvil_designer import ReaderTemplate
from anvil import *
from ...App import NAVIGATION

class Reader(ReaderTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    NAVIGATION.set(nav_bar='reader')
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    pass



