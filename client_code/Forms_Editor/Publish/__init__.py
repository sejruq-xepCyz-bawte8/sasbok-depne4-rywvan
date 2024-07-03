from ._anvil_designer import PublishTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, EDITOR

class Publish(PublishTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.open_form = NAVIGATION.nav_open_form

    self.author_uri.text = EDITOR.data['author_uri']
    self.work_uri.text = EDITOR.data['work_uri']

    if EDITOR.data['work_id'] == EDITOR.data['author_id']:
      self.label_slash.visible = False
      self.work_uri.visible = False
    else:
      self.work_uri.enabled = False



  def form_show(self, **event):
    self.info = jQ('#info')
    self.info.text('Логин')
    self.sidebar = jQ('#editor-option-sidebar')
    self.sidebar.toggle()
    self.buld_sidebar()

    self.uri.text = EDITOR.data['uri']
    self.prelink.text = f"chete.me/author_uri/{EDITOR.data['uri']}"




  def build_sidebar():
    pass

  def save_buffer(self):
    EDITOR.save_work()
    self.info.addClass('saved')
  


  def unpublish_confirm_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    pass
