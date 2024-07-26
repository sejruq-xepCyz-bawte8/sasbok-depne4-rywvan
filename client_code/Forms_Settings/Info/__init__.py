#Cheteme Form Info
from ._anvil_designer import InfoTemplate
from anvil import *
from ...App import ASSETS, NAVIGATION


class Info(InfoTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
 
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    self.info.content = ASSETS.get(file_path='md/info.md')
