from ._anvil_designer import GenresTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, EDITOR, ASSETS, AW

class Genres(GenresTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.work = EDITOR.get_current_work()
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    self.info = jQ('#info')
    self.info.text('Икони')
    self.sidebar = jQ('#keywords')
    self.sidebar.toggle()
    self.buld_sidebar()

  def buld_sidebar(self):
    keywords = ASSETS.get('json/awesome.json')
    icon = ASSETS.get('html/icon.html')
    for key, value in keywords.items():
      fa = AW.get(key)
      icon_html = icon.format(bg=key, fa=value)
      self.sidebar.append(icon_html)


  def form_hide(self, **event_args):
    self.save_buffer()

  def save_buffer(self):
    EDITOR.save_work(self.work)
    self.info.addClass('saved')
  
  def sidebar_toggle(self, sender, **event):
    self.sidebar.toggle()

  def keywords_pressed_enter(self, **event_args):
    pass

  def keywords_change(self, **event_args):
    pass

  def genres_1_change(self, **event_args):
    """This method is called when an item is selected"""
    pass
