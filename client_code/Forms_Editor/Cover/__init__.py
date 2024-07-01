from ._anvil_designer import CoverTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, EDITOR, ASSETS

class Cover(CoverTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.work = EDITOR.get_current_work()
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    self.info = jQ('#info')
    self.info.text('Шрифтове')
    self.sidebar = jQ('#fonts')
    self.sidebar.toggle()


  def buld_sidebar(self):
    fonts = ASSETS.get()


  def form_hide(self, **event_args):
    self.save_buffer()

  def save_buffer(self):
    EDITOR.save_work(self.work)
    self.info.addClass('saved')
  
  def sidebar_toggle(self, sender, **event):
    self.sidebar.toggle()
  