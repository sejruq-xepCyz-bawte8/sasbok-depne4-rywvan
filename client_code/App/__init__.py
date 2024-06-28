#Cheteme App
from .Browser import BrowserClass
from .Navigation import NavigationClass
from .Assets import AssetsClass
from .User import UserClass
print('init app')

VERSION = 1
BROWSER = BrowserClass()
USER = UserClass()
ASSETS = AssetsClass(origin=BROWSER.origin)
NAVIGATION = NavigationClass(fn_asset_get=ASSETS.get)




    