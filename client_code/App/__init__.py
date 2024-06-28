#Cheteme App
from .Browser import BrowserClass
from .Navigation import NavigationClass
from .Assets import AssetsClass
print('init app')

VERSION = 1
BROWSER = BrowserClass()
ASSETS = AssetsClass(BROWSER.origin)
NAVIGATION = NavigationClass(ASSETS)




    