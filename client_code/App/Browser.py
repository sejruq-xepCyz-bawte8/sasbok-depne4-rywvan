from anvil.js import window
from anvil.js.window import document

#"loadingSpinner"
delete = ["anvil-header", "anvil-badge", "error-indicator"]

class BrowserClass:
    def __init__(self):

        script_to_head_load(src='_/theme/js/parse_back.js')
        self.origin = window.location.origin
        self.protocol = window.location.protocol
        self.host = window.location.host
        self.hostname = window.location.hostname
        print(self.hostname)
        self.touch = False
        if 'maxTouchPoints' in window.navigator and window.navigator.maxTouchPoints > 0:
            self.touch = True
        if 'msMaxTouchPoints' in window.navigator and window.navigator.msMaxTouchPoints > 0:
            self.touch = True

        if self.touch:
            window.document.body.classList.add('touch')
        else:
            window.document.body.classList.add('notouch')
  







def script_to_head_load(src:str) -> None:
    script = document.createElement('script')
    script.src = src
    document.head.appendChild(script)



