from ._anvil_designer import ProfileTemplate
from anvil import *
from ...App import NAVIGATION

class Profile(ProfileTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.open_form

  def form_show(self, **event):
    pass



