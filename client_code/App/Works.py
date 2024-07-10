from anvil_extras.storage import indexed_db

class WorksClass:
    def __init__(self, fn_asset_get, fn_awesome_get):
        self.store = indexed_db.create_store('cheteme-works')
        self.get_asset = fn_asset_get
        self.get_icon = fn_awesome_get
        self.data_template = fn_asset_get('json/work_data.json')
        self.cover_template = fn_asset_get('html/work_cover.html')


    def get_cover(self, work_id:str)->str:
        pass

    def get_example_cover(self):
        example_data = self.get_asset('json/work_data_example.json')
        html = self.make_cover(example_data)
        return html
    
    
    def make_cover(self, data:dict)->str:
        if not data:
            return None
    
        html_data = {
            "work_id":data["work_id"],
            "bg_color":data["bg_color"],
            "image":'' if not data['image'] else data['image'],
            "mask":self.parse_mask_bg(data),
            "font":data["font"],
            "color":data["color"],
            "title":data["title"],
            "icons":['', '', '', '', '', '']
        }


        genres:list = data['genres']
        icons = []
        for g in genres[1:]:
            if g: icons.append(g)

        keywords:list = data['keywords']
        
        icons.extend(keywords)
        
        
        k = 0
        for i in range(len(icons)):
            if k < 6:
                fa = self.get_icon(icons[i])
                if fa:
                    html_data['icons'][k] = fa
                    k += 1
        


        html = self.cover_template.format(**html_data)
        return html

    @staticmethod
    def parse_mask_bg(data:dict)->str:
        opacity = int(data['m_opacity']) / 100
        hex_shadow = data['m_color'].lstrip('#')
        rgb = tuple(int(hex_shadow[i:i+2], 16) for i in (0, 2, 4))
        background_image = f'linear-gradient(to top, rgba({rgb[0]},{rgb[1]},{rgb[2]},{opacity}) 0%, rgba({rgb[0]},{rgb[1]},{rgb[2]}, 0) 100%)'
        return background_image