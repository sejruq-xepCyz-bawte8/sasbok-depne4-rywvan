// Find the existing viewport meta tag
var viewportMetaTag = document.querySelector('meta[name="viewport"]');

// Add user-scalable=no attribute if the viewport meta tag exists
if (viewportMetaTag) {
    viewportMetaTag.content += ', user-scalable=no';
} else {
    // If viewport meta tag doesn't exist, create a new one
    viewportMetaTag = document.createElement('meta');
    viewportMetaTag.name = 'viewport';
    viewportMetaTag.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
    
    // Append the new viewport meta tag to the head of the document
    document.head.appendChild(viewportMetaTag);
}



history.pushState(null, null, location.href);
history.back();
history.forward();
var count = 0
var isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
window.addEventListener('popstate', () => {
  count++;
  history.go(1);

  if (count % 2 === 1 && (isSafari || count > 2)) { // In other browser, the first time user press back value of count is > 2, but safari is not
    
    const container = document.getElementById('navigation');
    const firstElement = container.querySelector(':first-child');
    anvil.call($("#appGoesHere > div"), "open_form", $(firstElement))
  }
});