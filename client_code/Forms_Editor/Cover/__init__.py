from ._anvil_designer import CoverTemplate
from anvil import *
from ...App import NAVIGATION, EDITOR

class Cover(CoverTemplate):
  def __init__(self, work_id, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.work = EDITOR.get_current_work()
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    pass





  def sidebar_toggle(self, sender, **event):
    self.sidebar.toggle()