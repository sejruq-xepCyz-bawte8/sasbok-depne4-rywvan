from anvil import *
from anvil.js.window import jQuery as jQ


class NavigationClass:
    def __init__(self, fn_asset_get):
        self.element = jQ('#navigation')
        self.asset = fn_asset_get

    def set(self, file_path:str):
        html:str = self.asset(file_path)
        self.element.html(html)

    def click(self, **event):
        sender = event['sender']
        sender_id = sender.attr('id')
        self.element.children().removeClass('nav-clicked')
        sender.toggleClass('nav-clicked')
        self.open_form(sender_id)

    def open_form(self, form_name):
        open_form(form_name)

    def form_event(self, event):
        pass

    def test(self):
        self.element.html('<span>test</span>')