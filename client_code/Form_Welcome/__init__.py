from ._anvil_designer import Form_WelcomeTemplate
from anvil import *
from ..App import ASSETS

class Form_Welcome(Form_WelcomeTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)

    self.rich_welcome.content = ASSETS.get('md/welcome.md')

  def form_show(self, **event):
    print('terms')

  def choise_change(self, sender, **event):
    self.button_enter.enabled = self.check_terms.checked

  def button_enter_click(self, sender, **event):
    global USER
    print('enter')
    age = 1 if self.check_age.checked else 0
    user = {
      'user_id': 'new_user',
      'secret':'new_user',
      'age': age
    }
    set_USER(user)
    response, status = make_api_request(api='new_user', info=str(age))
    if status == 200 and response and response.get('user_id'):
      set_USER(response)
      open_form('Forms_Reader.Home')
    else:
      set_USER(None)


