from anvil import *
from anvil.js.window import jQuery as jQ


class NavigationClass:
    def __init__(self, fn_asset_get):
        self.element = jQ('#navigation')
        self.asset = fn_asset_get

    def set(self, file_path:str):
        html:str = self.asset(file_path)
        self.element.html(html)


    def open_form(self, sender, **event):
        sender_id = sender.attr('id')
        self.element.children().removeClass('active')
        sender.addClass('active')
        open_form(sender_id)


    def test(self):
        self.element.html('<span>test</span>')