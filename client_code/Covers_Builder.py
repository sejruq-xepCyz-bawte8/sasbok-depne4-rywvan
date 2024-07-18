from .App import READER, WORKS
from anvil.js.window import jQuery as jQ


def fill_panel(panel_id, works:list):
    
    panel = jQ(f'#{panel_id}')
    panel.html('')
    
    for work in works:
      work_id = work['work_id']
      data = READER.get_work_data(work_id)
      cover = WORKS.make_cover(data)
      panel.append(cover)
    

