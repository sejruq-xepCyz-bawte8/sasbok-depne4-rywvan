from ._anvil_designer import BookmarksTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from ...App import NAVIGATION

class Bookmarks(BookmarksTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    pass

  def test(self, sender, **event):
    print('nac cl test')

