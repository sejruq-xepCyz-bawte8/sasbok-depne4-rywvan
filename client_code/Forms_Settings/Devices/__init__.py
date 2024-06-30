from ._anvil_designer import DevicesTemplate
from anvil import *
from ...App import NAVIGATION, ASSETS, API, USER
from ...Helpers import zod_device_code

class Devices(DevicesTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
 
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    self.rt_user_info.content = ASSETS.get(file_path='md/settings_devices.md')


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
      delete = alert(content="Това ще изчисти устройството от вашите данни.",
               title="Изтриване устройство",
               large=True,
               buttons=[
                 ("Изтрии", True),
                 ("Откажи", False)
               ])
      if delete:
        USER.delete_user()
        NAVIGATION.delete()
        open_form('Form_Welcome')

  def tb_user_code_change(self, **event_args):
    zod_device_code(self.tb_user_code)
    self.b_activate_code.enabled = self.tb_user_code.valid
    