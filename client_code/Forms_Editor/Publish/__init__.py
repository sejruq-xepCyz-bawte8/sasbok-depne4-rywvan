from ._anvil_designer import PublishTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
import anvil.users
from anvil.js.window import jQuery as jQ
from anvil.js.window import Quill, JSON
import json
from ...App import NAVIGATION, EDITOR, USER, ASSETS, ORIGIN_APP, API
from time import time

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

    self.age.checked = False if not EDITOR.data.get('age') else True
    
    

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
    if len(EDITOR.data['title']) > 40:
      conditions += "прекалено дълго заглавие (макс 40)"
    if len(EDITOR.data['uri']) > 40:
      conditions += "прекалено дълъг линк (макс 40)"

    if not conditions:
      self.publish.enabled = True
      self.info_text.text = conditions
    else:
      self.publish.enabled = False
      self.info_text.text = conditions
      self.info_text.foreground = "LightSalmon"

    if ORIGIN_APP == "http://192.168.0.101:3030":
      self.publish.enabled = True


  def save_buffer(self):
    EDITOR.save_work()
    self.info.addClass('saved')
  


  def work_uri_change(self, sender, **event_args):
    if EDITOR.data['work_id'] != EDITOR.data['author_id']:
      EDITOR.data['uri'] = sender.text
      EDITOR.save_work()


  def publish_click(self, **event_args):
    EDITOR.data['ver'] += 1
    EDITOR.save_work()
    data = {
      "data":EDITOR.data,
      "content":self.content
    }
    ticket = "ttt"
    result, status = API.request(api='publish_work', data=data, info=ticket)
    if result and status == 200:
      ticket = result['ticket']
      anvil_result = anvil.server.call('execute_ticket', ticket=ticket)
     
      if anvil_result:
        Notification(f"Успешна публикация 🥳", style='success').show()
      else:
        Notification(f"Неуспешна публикация :(", style='danger').show()
    else:
      Notification(f"Неуспешна публикация :(", style='danger').show()

  def copy_permalink_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass



  def sidebar_toggle(self, sender, **event):
    sender.toggleClass('active')
    self.sidebar.toggle()

  def b_author_uri_click(self, **event_args):
    result, status = API.request(api='author_uri', info=self.author_uri.text)
    
    if result and status == 200:
      author_uri = result['author_uri']
      self.user['author_uri'] = author_uri
      USER.set_user(self.user)
      self.author_uri.text = author_uri
      self.prelink.text = f"chete.me/{author_uri}/"
      if EDITOR.data['work_id'] == EDITOR.data['author_id']:
        EDITOR.data['uri'] = author_uri
        EDITOR.save_work()
      Notification(f"Успешна промяна 🥳 chete.me/{author_uri}/", style='success').show()
      self.check_conditions()
    else:
      Notification("Възникна грешка :(", style='danger').show()
    

  def b_login_click(self, **event_args):
    user = anvil.users.login_with_form()
    if user:
      self.anvil_email.text = "Успешен вход"
      Notification("Успешен вход :)").show()
    

  def b_logout_click(self, **event_args):
    user = anvil.users.logout()
    if not user:
      self.anvil_email.text = "За публикуване е необходим вход :)"

  def accept_terms_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    pass

  def age_changed(self, **event):
    EDITOR.data['age'] = 1 if self.age.checked else 0
    EDITOR.save_work()






    
    
