from ._anvil_designer import BookmarksTemplate
from anvil import *
from ...App import NAVIGATION, READER

class Bookmarks(BookmarksTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    READER.set_back("bookmarks")
    
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    pass

  def test(self, sender, **event):
    print('nac cl test')

