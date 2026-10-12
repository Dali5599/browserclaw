function getCssSelector(el) {
  if (!el) return '';
  if (el.id) {
    return `#${CSS.escape(el.id)}`;
  }
  if (el === document.body) {
    return 'body';
  }
  let path = [];
  let current = el;
  while (current && current !== document.body) {
    let selector = current.tagName.toLowerCase();
    if (current.className && typeof current.className === 'string') {
      const classes = current.className.trim().split(/\s+/).filter(Boolean);
      if (classes.length > 0) {
        selector += '.' + classes.map(c => CSS.escape(c)).join('.');
      }
    }
    let sibling = current;
    let nth = 1;
    while ((sibling = sibling.previousElementSibling) !== null) {
      if (sibling.tagName === current.tagName) {
        nth++;
      }
    }
    selector += `:nth-of-type(${nth})`;
    path.unshift(selector);
    current = current.parentElement;
  }
  return path.join(' > ');
}

document.addEventListener('click', (event) => {
  const target = event.target;
  const selector = getCssSelector(target);
  const action = {
    type: 'click',
    selector,
    text: target.innerText ? target.innerText.substring(0, 50).trim() : '',
    timestamp: Date.now()
  };
  chrome.runtime.sendMessage({ type: 'RECORD_ACTION', action }).catch(() => {});
}, true);

document.addEventListener('change', (event) => {
  const target = event.target;
  if (['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName)) {
    const selector = getCssSelector(target);
    const action = {
      type: 'change',
      selector,
      value: target.type === 'password' ? '***' : target.value,
      timestamp: Date.now()
    };
    chrome.runtime.sendMessage({ type: 'RECORD_ACTION', action }).catch(() => {});
  }
}, true);

let scrollTimeout;
document.addEventListener('scroll', () => {
  clearTimeout(scrollTimeout);
  scrollTimeout = setTimeout(() => {
    const action = {
      type: 'scroll',
      scrollX: window.scrollX,
      scrollY: window.scrollY,
      timestamp: Date.now()
    };
    chrome.runtime.sendMessage({ type: 'RECORD_ACTION', action }).catch(() => {});
  }, 500);
}, true);
