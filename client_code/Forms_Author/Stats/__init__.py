from ._anvil_designer import StatsTemplate
from anvil import *
from ...App import NAVIGATION

class Stats(StatsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    pass


