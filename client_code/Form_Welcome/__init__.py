from ._anvil_designer import Form_WelcomeTemplate
from anvil import *
from ..App import ASSETS, API, USER, NAVIGATION
from ..Helpers import zod_code

class Form_Welcome(Form_WelcomeTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    

  def form_show(self, **event):
    self.rich_welcome.content = ASSETS.get('md/welcome.md')

  def input_change(self, **event):
    zod_code(self.tb_code)
    if self.check_terms.checked and self.tb_code.valid:
      self.button_enter.enabled = True
    else:
      self.button_enter.enabled = False

  def button_enter_click(self, **event):
    print('enter')
    age = '1' if self.check_age.checked else '0'
    response, status = API.request_new_user(code=self.tb_code.text, age=age)
    
    if response:
      Notification("Успешен вход 🥳", style='success').show()

      USER.set_user(response)
      NAVIGATION.set(nav_bar='today')
      open_form('Forms_Today.Today')
    else:
      Notification("Неуспешен вход 😭", style='danger').show()


