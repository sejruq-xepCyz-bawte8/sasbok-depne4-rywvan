from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, SETTINGS, ASSETS, WORKS


class Settings(SettingsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    self.open_form = NAVIGATION.nav_open_form

    self.settings = SETTINGS.get()
    
    

  def form_show(self, **event):
    self.cover_panel = jQ('#cover')
    example_cover = WORKS.get_example_cover()
    self.cover_panel.append(example_cover)

    self.slider_text_size.value = self.settings['text']
    self.slider_line_size.value = self.settings['line']
    self.slider_nav_size.value = self.settings['navigation']
    self.slider_cover_size.value = self.settings['cover']


  def gui_settings_change(self, handle, **event_args):
    settings = {
      'text':self.slider_text_size.value,
      'line':self.slider_line_size.value,
      'navigation':self.slider_nav_size.value,
      'cover':self.slider_cover_size.value
    }
    SETTINGS.set(data=settings)

