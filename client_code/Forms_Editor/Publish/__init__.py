from ._anvil_designer import PublishTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
import anvil.users
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, EDITOR, USER

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
    self.build_sidebar()



  def build_sidebar(self):
    pass

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







    
    
