#Cheteme Covers Builder
from .App import WORKS
from anvil.js.window import jQuery as jQ

def fill_panel(panel_id, works:list):
    panel = jQ(f'#{panel_id}')
    panel.html('')
    for work in works:
      cover = WORKS.make_cover(work_id=work['work_id'])
      panel.append(cover)
    

