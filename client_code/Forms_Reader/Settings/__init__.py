from ._anvil_designer import SettingsTemplate
from anvil import *
from ...App import NAVIGATION, SETTINGS, ASSETS


class Settings(SettingsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    self.settings = SETTINGS.get()
    
    self.open_form = NAVIGATION.open_form

  def form_show(self, **event):
    self.rt_settings_info.content = ASSETS.get(file_path='md/settings.md')
    self.rt_user_info.content = ASSETS.get(file_path='md/settings_user.md')
    self.rt_author_info.content = ASSETS.get(file_path='md/settings_author.md')
    self.slider_text_size.value = self.settings['text']
    self.slider_nav_size.value = self.settings['navigation']


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
    settings = {
      'text':self.slider_text_size.value,
      'navigation':self.slider_nav_size.value
    }
    SETTINGS.set(data=settings)

  def b_code_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
   
    
