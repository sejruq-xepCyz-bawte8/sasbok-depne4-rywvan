from ._anvil_designer import AuthorTemplate
from anvil import *
from ...App import NAVIGATION, SETTINGS, ASSETS, API, USER


class Author(AuthorTemplate):
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
    ticket_data, status = API.request(api='merge_users_ticket')
    if ticket_data and status == 200:
      self.tb_user_code.text = ticket_data['ticket']
    else:
      self.tb_user_code.text = 'Неуспешна активация'
      
  def b_activate_code_click(self, **event_args):
    ticket = self.tb_user_code.text
    master_user, status = API.request(api='merge_users', info=ticket)
    if master_user and status == 200:
      USER.set_user(user=master_user)
      self.tb_user_code.text = 'Успешна активация'
    else:
      self.tb_user_code.text = 'Неуспешна активация'
   
  def b_clean_click(self, **event_args):
      USER.delete_user()
