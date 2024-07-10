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