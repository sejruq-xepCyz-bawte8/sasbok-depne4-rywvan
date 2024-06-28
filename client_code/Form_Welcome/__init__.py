from ._anvil_designer import Form_WelcomeTemplate
from anvil import *
from ..App import ASSETS, API, USER, NAVIGATION

class Form_Welcome(Form_WelcomeTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    

  def form_show(self, **event):
    self.rich_welcome.content = ASSETS.get('md/welcome.md')

  def choise_change(self, **event):
    self.button_enter.enabled = self.check_terms.checked

  def button_enter_click(self, **event):
    print('enter')
    info = '1' if self.check_age.checked else '0'
    response, status = API.request(api='new_user', info=info)
    print(response, status)
    if response:
      USER.set_user(response)
      NAVIGATION.set(file_path='html/nav_reader.html')
      open_form('Forms_Reader.Today')


