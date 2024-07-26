#Cheteme Covers Builder
from .App import WORKS
from anvil.js.window import jQuery as jQ

def fill_panel(panel_id, work_ids:list):
    panel = jQ(f'#{panel_id}')
    panel.html('')
    for work_id in work_ids:
      cover = WORKS.make_cover(work_id=work_id)
      panel.append(cover)
    

