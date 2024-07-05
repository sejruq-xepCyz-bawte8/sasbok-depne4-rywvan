from ._anvil_designer import AuthorsTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, READER, WORKS

class Authors(AuthorsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.nav_open_form
    

  def form_show(self, **event):
    self.authors_panel = jQ('#authors-panel')
    print(READER.authors)
    for work in READER.authors:
      work_id = work['work_id']
      
      data = READER.get_work_data(work_id)
   
      cover = WORKS.make_cover(data)
      self.authors_panel.append(cover)


  def open_work(self, sender, **event):
    print(sender.attr('id'))
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')

  def b_search_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

