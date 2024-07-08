from ._anvil_designer import StatsTemplate
from anvil import *
from ...App import NAVIGATION, API, USER




class Stats(StatsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    api = "get_author_stats"
    panel_id = 'stats-panel'
    
    self.open_form = NAVIGATION.nav_open_form

    user = USER.get_user()
    author_id = user['author_id']
    results, _ = API.request(api=api, info=author_id)
    self.stats = results[0]

  def form_show(self, **event):
    template = [{'liked': 1, 'readed': 0, 'comment': 1, 'ostay': 0, 'countries': '', 'cities': ''}]
    liked = Label(text=f"общо харесани: {self.stats['liked']}")
    comment = Label(text=f"общо коментари: {self.stats['comment']}")
    countries = Label(text=f"държави: {self.stats['countries']}")
    self.add_component(liked)
    self.add_component(comment)
    self.add_component(countries)



