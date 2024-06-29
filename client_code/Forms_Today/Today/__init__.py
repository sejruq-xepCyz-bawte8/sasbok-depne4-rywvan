from ._anvil_designer import TodayTemplate
from anvil import *
from ...App import NAVIGATION

class Today(TodayTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.open_form

  def form_show(self, **event):
    pass

  def test(self, sender, **event):
    print('nac cl test')

