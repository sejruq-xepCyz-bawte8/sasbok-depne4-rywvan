from ._anvil_designer import PublishedTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, API, USER, READER, WORKS

#get_author_published

class Published(PublishedTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    
    self.open_form = NAVIGATION.nav_open_form

    api = 'get_author_published'
    user = USER.get_user()
    self.author_id = user['author_id']
    self.published_works, _ = API.request(api=api, info=self.author_id)
    
  def form_show(self, **event):
    self.panel = jQ('#published-panel')
    self.parse_works()
    
    
    

  def parse_works(self):
    self.panel.html('')
    for work in self.published_works:
      work_id = work['work_id']
      data = READER.get_work_data(work_id=work_id)
      if data:
        cover = WORKS.make_cover(data)
        self.panel.append(cover)

  def open_work(self, sender, **event):
    work_id = sender.attr('id')
    api = "get_work_stats"
    results, _ = API.request(api=api, info=work_id)
    stats = results[0]
    panel = LinearPanel()
    liked = Label(text=f"общо харесани: {stats['liked']}")
    comment = Label(text=f"общо коментари: {stats['comment']}")
    countries = Label(text=f"държави: {stats['countries']}")
    panel.add_component(liked)
    panel.add_component(comment)
    panel.add_component(countries)

    result = alert(content=panel,
               title="Статистики:",
               large=True,
               buttons=[
                 ("Затвори", "YES")
               ])