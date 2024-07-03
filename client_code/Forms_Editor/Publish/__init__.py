from ._anvil_designer import PublishTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
import anvil.users
from anvil.js.window import jQuery as jQ
from anvil.js.window import Quill, JSON
import json
from ...App import NAVIGATION, EDITOR, USER, ASSETS

class Publish(PublishTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.open_form = NAVIGATION.nav_open_form
    self.user = USER.get_user()
    

    self.prelink.text = f"chete.me/{self.user['author_uri']}/"
    self.author_uri.text = self.user['author_uri']
    self.work_uri.text = EDITOR.data['uri']

    if EDITOR.data['work_id'] == EDITOR.data['author_id']:
      self.work_uri.visible = False

    self.title.text = EDITOR.data['title']


    self.anvil_user = anvil.users.get_user()
    if self.anvil_user:
      self.b_login.visible = False
      self.anvil_email.text = self.anvil_user['email']
    else:
      self.b_logout.visible = False
      self.anvil_email.text = "За публикуване е необходим вход :)"

  def form_show(self, **event):
    self.info = jQ('#info')
    self.info.text('Сървър')
    self.sidebar = jQ('#editor-option-sidebar')
    self.sidebar.toggle()


    self.quill = Quill('#quill', ASSETS.get('json/quill_publish.json'))
    delta = json.loads(EDITOR.content)
    self.quill.setContents(delta)
    self.content = self.quill.getSemanticHTML()
    
    self.check_conditions()


  def check_conditions(self):
    conditions = ''
    if not self.anvil_user:
      conditions += 'няма логин, '
    if not EDITOR.data['uri']:
      conditions += 'няма пермалинк, '
    if not EDITOR.data['title']:
      conditions += 'няма заглавие, '
    if (EDITOR.data['work_id'] != EDITOR.data['author_id']) and (not EDITOR.data['genres'][0] or not EDITOR.data['genres'][1] or not EDITOR.data['genres'][2]):
      conditions += 'няма жанрове, '
    if not EDITOR.data['uri']:
      conditions += 'няма пермалинк, '
    if not self.content:
      conditions += 'няма текст, '
    if EDITOR.data['size'] > 5_000:
      conditions += f"много голям файл {EDITOR.data['size']}kb, "

    if not conditions:
      self.publish.enabled = True
      self.info_text.text = conditions
    else:
      self.publish.enabled = False
      self.info_text.text = conditions
      self.info_text.foreground = "LightSalmon"



  def save_buffer(self):
    EDITOR.save_work()
    self.info.addClass('saved')
  


  def unpublish_confirm_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    pass

  def author_uri_change(self, sender, **event_args):
    
    if EDITOR.data['work_id'] == EDITOR.data['author_id']:
      EDITOR.data['uri'] = sender.text
      EDITOR.save_work()
    
    self.user['author_uri'] = sender.text
    USER.set_user(user=self.user)

  def work_uri_change(self, sender, **event_args):
    if EDITOR.data['work_id'] != EDITOR.data['author_id']:
      EDITOR.data['uri'] = sender.text
      EDITOR.save_work()


  def publish_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def copy_permalink_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def unpublish_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass


  def sidebar_toggle(self, sender, **event):
    self.sidebar.toggle()

  def b_author_uri_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def b_login_click(self, **event_args):
    user = anvil.users.login_with_form()
    if user:
      self.anvil_email.text = self.anvil_user['email']
    

  def b_logout_click(self, **event_args):
    user = anvil.users.logout()
    if not user:
      self.anvil_email.text = "За публикуване е необходим вход :)"

  def accept_terms_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    pass








    
    
