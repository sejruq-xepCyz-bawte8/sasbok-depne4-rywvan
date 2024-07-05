from ._anvil_designer import TodayTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from ...App import NAVIGATION, ASSETS, WORKS, READER
from anvil.js.window import jQuery as jQ



class Today(TodayTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)

    self.open_form = NAVIGATION.nav_open_form

    self.work_template:str = ASSETS.get('html/work_cover.html')
    
    

  def form_show(self, **event):
    self.published_panel = jQ('#published-works')
    
   
    for work in READER.last:
      work_id = work['work_id']
      
      data = READER.get_work_data(work_id)
      
      cover = WORKS.make_cover(data)
      self.published_panel.append(cover)
      


  def b_work_click(self, **event):
      open_form('Forms_Reader.Reader')


  def open_work(self, sender, **event):
    print(sender.attr('id'))
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')