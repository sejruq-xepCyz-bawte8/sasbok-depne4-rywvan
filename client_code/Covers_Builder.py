#Cheteme Covers Builder
from .App import WORKS
from anvil.js.window import jQuery as jQ

def fill_panel(panel_id, work_ids:list=None, works:list=None):
    panel = jQ(f'#{panel_id}')
    panel.html('')
    if work_ids:
      for work_id in work_ids:
        cover = WORKS.make_cover(work_id=work_id)
        panel.append(cover)
    
    if works:
      for work in works:
        cover = WORKS.make_cover(work_id=work['work_id'])
        panel.append(cover)
