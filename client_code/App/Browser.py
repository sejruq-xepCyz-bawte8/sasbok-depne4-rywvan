from anvil.js import window

#"loadingSpinner"
delete = ["anvil-header", "anvil-badge", "error-indicator"]

class BrowserClass:
    def __init__(self):
        self.origin = window.location.origin
        self.protocol = window.location.protocol
        self.host = window.location.host
        self.hostname = window.location.hostname

        for d in delete:
            element = window.document.getElementById(d)
            element.remove()
        
        elements = window.document.getElementsByClassName('anvil-spinner-svg')
        elements[0].remove()
        #spinner = window.document.createElement('div')
        #spinner.id = "loadingSpinner"
        #window.document.body.appendChild(spinner)