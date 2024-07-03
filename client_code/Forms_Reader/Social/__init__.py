from ._anvil_designer import SocialTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from ...App import NAVIGATION

class Social(SocialTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    pass



