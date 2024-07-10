from anvil.js import window

#"loadingSpinner"
delete = ["anvil-header", "anvil-badge", "error-indicator"]

class BrowserClass:
    def __init__(self):
        self.origin = window.location.origin
        self.protocol = window.location.protocol
        self.host = window.location.host
        self.hostname = window.location.hostname
        self.touch = False
        if 'maxTouchPoints' in window.navigator and window.navigator.maxTouchPoints > 0:
            self.touch = True
        if 'msMaxTouchPoints' in window.navigator and window.navigator.msMaxTouchPoints > 0:
            self.touch = True

        if self.touch:
            window.document.body.classList.add('touch')
        else:
            window.document.body.classList.add('notouch')
  