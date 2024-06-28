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


  def tabs_tab_click(self, tab_index, tab_title, **event_args):
    if tab_index == 0:
      self.lp_gui.visible = True
      self.lp_user.visible = False
      self.lp_author.visible = False
    elif tab_index == 1:
      self.lp_gui.visible = False
      self.lp_user.visible = True
      self.lp_author.visible = False
    else:
      self.lp_gui.visible = False
      self.lp_user.visible = False
      self.lp_author.visible = True

  def gui_settings_change(self, handle, **event_args):
    nav_size = self.slider_nav_size.value
    pass
