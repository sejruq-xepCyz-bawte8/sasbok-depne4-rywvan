from ._anvil_designer import ChartsTemplate
from anvil import *
from ...App import NAVIGATION, READER
from ...Covers_Builder import fill_panel

class Charts(ChartsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.filters:set = set()
    
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    
    fill_panel(panel_id='charts-panel', works=READER.chart(chart='liked', days=3))


  def b_search_click(self, sender, **event):
    search = self.search_for.text
    fill_panel(panel_id='charts-panel', works=READER.search(search))
    

      

  def search_for_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass

  def filter_toggle(self, sender, *event):
    filter = sender.attr('id')
    sender.find('.filter-fa').toggleClass('fa-duotone')
    if filter in self.filters:
      self.filters.remove(filter)
    else:
      self.filters.add(filter)
    print(self.filters)

  def clean_search_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def search_for_focus(self, **event_args):
    """This method is called when the TextBox gets focus"""
    pass

