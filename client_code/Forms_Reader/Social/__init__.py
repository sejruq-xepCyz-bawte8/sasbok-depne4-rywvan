from ._anvil_designer import SocialTemplate
from anvil import *
from ...App import NAVIGATION

class Social(SocialTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.open_form = NAVIGATION.open_form

  def form_show(self, **event):
    pass



