#Cheteme Bookmarks Form
from ._anvil_designer import BookmarksTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, READER, WORKS


class Bookmarks(BookmarksTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    READER.set_back("bookmarks")
    
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    panel = jQ('#bookmarks-container')
    panel.html('')

    bookmarks_ids = list(READER.bookmarks)

    for work_id in bookmarks_ids:
      cover = WORKS.make_cover(work_id=work_id)
      panel.append(cover)

  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')

