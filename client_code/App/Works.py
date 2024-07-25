from anvil_extras.storage import indexed_db
import anvil.http
from time import time

class WorksClass:
    def __init__(self, fn_asset_get, fn_awesome_get):
        self.store = indexed_db.create_store('cheteme-works')
        
        self.get_asset = fn_asset_get
        self.get_icon = fn_awesome_get
        self.data_template = fn_asset_get('json/work_data.json')
        self.cover_template = fn_asset_get('html/work_cover.html')

        self.works_data = self.store.get('data')
        self.works_content = self.store.get('content')
      
        if not self.works_data:
          self.works_data:dict = {}
        
        if not self.works_content:
            self.works_content:dict = {}
  
    def get_cover(self, work_id:str)->str:
        pass

    def get_example_cover(self):
        example_data = self.get_asset('json/work_data_example.json')
        html = self.make_cover(example_data)
        return html
    
    
    def make_cover(self, data:dict)->str:
        if not data:
            return None

        color = data["color"]
        bg_color = data["bg_color"]
        image = data['image'] if data['image'] else ''
        mask = self.parse_mask_bg(data)
        fonts = data["font"].split(' ')
        font = fonts[0]


        if image:
            cover_style = f"""style="background-color: {bg_color}; background-image: url('{image}');" """
        else:
            cover_style = f"""style="background-color: {bg_color};" """ 
        
        mask_style = f"""style="background-image:{mask};" """

        if len(fonts) == 1:
            title_style = f"""style="color:{color};" """
        else:
            text_shadow = f"1px 1px 1px {bg_color}, -1px -1px 1px {bg_color}, -1px 1px 1px {bg_color}, 1px -1px 1px {bg_color}"
            title_style = f"""style="color:{color}; text-shadow:{text_shadow};" """
        
        icons_style = f"""style="color:{color};" """


        html_data = {
            "work_id":data["work_id"],
            "cover_style": cover_style,
            "mask_style": mask_style,
            "font":font,
            "title_style":title_style,
            "title":data["title"],
            "icons_style":icons_style,
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
        background_image = f'linear-gradient(to top, rgba({rgb[0]},{rgb[1]},{rgb[2]},{opacity}) 0%, rgba({rgb[0]},{rgb[1]},{rgb[2]},{opacity}) 45%, rgba({rgb[0]},{rgb[1]},{rgb[2]}, 0) 65%, rgba({rgb[0]},{rgb[1]},{rgb[2]}, 0) 100%)'
        return background_image
    


    def get_work_data(self, work_id:str):
      if work_id in self.works_data:
        work_data = self.works_data[work_id]
        self.works_data[work_id]['timestamp'] = time()
        self.clean_works_data()
        return work_data
      else:
        work_data = self.fetch_work_data(work_id)
        return work_data



  
    def fetch_work_data(self, work_id):
          url = f'https://chete.me/api/wd-{work_id}'
          try:
                response = anvil.http.request(url=url,method='GET',json=True)
          except anvil.http.HttpError as e:
                response = None

          if response:
            self.works_data[work_id] = response
            self.works_data[work_id]['timestamp'] = time()
            self.clean_works_data()
            
          return response


    def get_work_content(self, work_id:str):
      if work_id in self.works_content:
        work_content = self.works_content[work_id]['content']
        self.works_content[work_id]['timestamp'] = time()
        #self.store['content'] = self.works_content
        self.clean_works_content()
        return work_content
      else:
        work_content = self.fetch_work_content(work_id)
        return work_content


    def fetch_work_content(self, work_id):
          url = f'https://chete.me/api/wc-{work_id}'
          try:
                response = anvil.http.request(url=url,method='GET',json=True)
          except anvil.http.HttpError as e:
                content = None

          if response and 'message' in response:
            content = response['message']
            self.works_content[work_id] = {'content':content, 'timestamp':time()}
            self.clean_works_content()
            
          return content


    def clean_works_data(self):
        if len(self.works_data) > 50:
          sorted_items = sorted(self.works_data.items(), key=lambda item: item[1]['timestamp'])
          self.works_data = {k: v for k, v in sorted_items[-40:]}
          self.store['data'] = self.works_data

    def clean_works_content(self):
        if len(self.works_content) > 20:
          sorted_items = sorted(self.works_content.items(), key=lambda item: item[1]['timestamp'])
          self.works_content = {k: v for k, v in sorted_items[-15:]}
          self.store['content'] = self.works_content
