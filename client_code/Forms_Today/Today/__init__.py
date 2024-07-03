from ._anvil_designer import TodayTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from ...App import NAVIGATION, ASSETS, WORKS
from anvil.js.window import jQuery as jQ



class Today(TodayTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)

    self.open_form = NAVIGATION.nav_open_form

    self.work_template:str = ASSETS.get('html/work_cover.html')
    
    

  def form_show(self, **event):
    self.published_panel = jQ('#published-works')
    
 
    example_cover = WORKS.get_example_cover()
    
    self.published_panel.append(example_cover)
    self.published_panel.append(example_cover)


  def b_work_click(self, **event):
      open_form('Forms_Reader.Reader')