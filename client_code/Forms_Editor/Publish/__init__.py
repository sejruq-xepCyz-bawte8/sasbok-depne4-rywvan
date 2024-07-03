from ._anvil_designer import PublishTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, EDITOR

class Publish(PublishTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    self.info = jQ('#info')
    self.info.text('Логин')
    self.sidebar = jQ('#editor-option-sidebar')
    self.sidebar.toggle()
    self.buld_sidebar()

    self.uri.text = EDITOR.data['uri']
    self.prelink.text = f"chete.me/author_uri/{EDITOR.data['uri']}"

  def uri_change(self, sender, **event_args):
    EDITOR.data['uri'] = sender.text
    self.prelink.text = f"chete.me/author_uri/{EDITOR.data['uri']}"


  def build_sidebar():
    pass

  def save_buffer(self):
    EDITOR.save_work()
    self.info.addClass('saved')
  
  def sidebar_toggle(self, sender, **event):
    self.sidebar.toggle()