from anvil.js import window

#"loadingSpinner"
delete = ["anvil-header", "anvil-badge", "error-indicator"]

class BrowserClass:
    def __init__(self):
        self.origin = window.location.origin
        self.protocol = window.location.protocol
        self.host = window.location.host
        self.hostname = window.location.hostname

  