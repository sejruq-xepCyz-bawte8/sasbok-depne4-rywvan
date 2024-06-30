from ._anvil_designer import AuthorsTemplate
from anvil import *
from ...App import NAVIGATION

class Authors(AuthorsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    pass

  def test(self, sender, **event):
    print('nac cl test')

