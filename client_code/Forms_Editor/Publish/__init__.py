from ._anvil_designer import PublishTemplate
from anvil import *
from ...App import NAVIGATION, EDITOR

class Publish(PublishTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    

    self.work = EDITOR.get_current_work()
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    pass



  def save_buffer(self):
    EDITOR.save_work(self.work)
    self.info.addClass('saved')
  
  def sidebar_toggle(self, sender, **event):
    self.sidebar.toggle()