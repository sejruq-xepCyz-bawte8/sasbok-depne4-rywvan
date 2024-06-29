from ._anvil_designer import SettingsTemplate
from anvil import *
from ...App import NAVIGATION, SETTINGS, ASSETS, API, USER


class Settings(SettingsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    self.settings = SETTINGS.get()
    
    self.open_form = NAVIGATION.open_form

  def form_show(self, **event):
    self.info.content = ASSETS.get(file_path='md/settings.md')

    self.slider_text_size.value = self.settings['text']
    self.slider_nav_size.value = self.settings['navigation']


  def gui_settings_change(self, handle, **event_args):
    settings = {
      'text':self.slider_text_size.value,
      'navigation':self.slider_nav_size.value
    }
    SETTINGS.set(data=settings)

