from anvil_extras.storage import indexed_db
from anvil_extras import non_blocking
import anvil.http
from time import time

CHARTS = ['home', 'last', 'week', 'month', 'authors']

class WorksClass:
    def __init__(self, fn_asset_get, fn_awesome_get):
        self.age = 1
        self.store = indexed_db.create_store('cheteme-works')
        self.contents_store = indexed_db.create_store('cheteme-content')

        
        self.get_asset = fn_asset_get
        self.get_icon = fn_awesome_get
        self.data_template = fn_asset_get('json/work_data.json')
        self.cover_template = fn_asset_get('html/work_cover.html')

        self.works_data = self.store.get('data')
        self.charts = self.store.get('charts')
 

      
        if not self.works_data:
          self.works_data:dict = {}
        
        
        if not self.charts:
              self.charts:dict = {}


        #update non blocking
        home = non_blocking.defer(self.update_home, 0)
        authors = non_blocking.defer(self.update_authors, 0)
        last = non_blocking.defer(self.update_last, 0)
        today = non_blocking.defer(self.update_today, 0)
        week = non_blocking.defer(self.update_week, 0)
        month = non_blocking.defer(self.update_month, 0)

        home_u = non_blocking.repeat(self.update_home, 300)
        authors_u = non_blocking.repeat(self.update_authors, 1800)
        last_u = non_blocking.repeat(self.update_last, 900)
        today_u = non_blocking.repeat(self.update_today, 900)
        week_u = non_blocking.repeat(self.update_week, 1800)
        month_u = non_blocking.repeat(self.update_month, 1800)

  
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
        self.store['data'] = self.works_data
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
            self.update_works_data()
          return response


    def get_work_content(self, work_id:str):
      if work_id in self.contents_store:
        work = self.contents_store[work_id]
        work['timestamp'] = time()
        self.contents_store[work_id] = work
        return work['content']
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
            self.contents_store[work_id] = {'content':content, 'timestamp':time()}
            self.clean_works_content()
            
          return content


    def update_works_data(self):
        if len(self.works_data) > 100:
          sorted_items = sorted(self.works_data.items(), key=lambda item: item[1]['timestamp'])
          self.works_data = {k: v for k, v in sorted_items[-90:]}
          self.store['data'] = self.works_data
        else:
          self.store['data'] = self.works_data

    def clean_works_content(self):
        if len(self.contents_store) > 20:
          sorted_items = sorted(self.contents_store.items(), key=lambda item: item[1]['timestamp'])
          to_clean = [k for k, v in sorted_items[:5]]
          for k in to_clean:
            del self.contents_store[k]



## charts
    def get_chart_data(self, chart_id):
        if chart_id in self.charts:
          chart = self.charts[chart_id]
          chart_data = chart['data']

        else:
          chart_data = self.fetch_chart_data(chart_id)

        return chart_data

          
    def fetch_chart_data(self, chart_id):
          url = f'https://chete.me/api/chart_{chart_id}_age_{self.age}'
          try:
                response = anvil.http.request(url=url,method='GET',json=True)
          except anvil.http.HttpError as e:
                response = None
          if response:
            self.charts[chart_id] = {'data':response, 'timestamp':time()}
            self.store['charts'] = self.charts   
          return response



    def update_home(self):
      self.fetch_chart_data(chart_id = 'home')


    def update_authors(self):
      authors = self.fetch_chart_data(chart_id = 'authors')
      for work in authors:
        work_id = work['work_id']
        if work_id in self.works_data:
          new_ver = work['ver']
          old_ver = self.works_data[work_id]['ver']
          if new_ver != old_ver:
            self.fetch_work_data(work_id)
            if work_id in self.works_content:
              self.fetch_work_content(work_id=work_id)

    def update_last(self):
      last = self.fetch_chart_data(chart_id = 'last')
      for work in last:
        work_id = work['work_id']
        if work_id in self.works_data:
          new_ver = work['ver']
          old_ver = self.works_data[work_id]['ver']
          if new_ver != old_ver:
            self.fetch_work_data(work_id)
            if work_id in self.works_content:
              self.fetch_work_content(work_id=work_id)


    def update_today(self):
      self.fetch_chart_data(chart_id = 'today')


    def update_week(self):
      self.fetch_chart_data(chart_id = 'week')

    def update_month(self):
      self.fetch_chart_data(chart_id = 'month')
      