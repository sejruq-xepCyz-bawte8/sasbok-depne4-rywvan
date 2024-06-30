from ._anvil_designer import GenresTemplate
from anvil import *
from ...App import NAVIGATION, EDITOR

class Genres(GenresTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.work = EDITOR.get_current_work()
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    pass



