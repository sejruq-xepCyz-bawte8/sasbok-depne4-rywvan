#Cheteme Index Module
from anvil import *
from . import USER
from . import NAVIGATION

def main():
    print('main')
    NAVIGATION.set(nav_bar='today')
    open_form('Forms_Today.Today')
def no_user():
    print('no user')
    open_form('Form_Welcome')

if __name__ == '__main__':
    print('index')
    if USER.is_user:
        main()
    else:
        no_user()