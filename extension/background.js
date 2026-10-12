let isRecording = false;
let recordedActions = [];

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'GET_STATE') {
    sendResponse({
      isRecording,
      actionsCount: recordedActions.length
    });
  } else if (message.type === 'TOGGLE_RECORDING') {
    isRecording = !isRecording;
    if (!isRecording) {
      console.log('Recording stopped. Total actions:', recordedActions.length);
    } else {
      recordedActions = [];
      console.log('Recording started...');
    }
    sendResponse({
      isRecording,
      actionsCount: recordedActions.length
    });
  } else if (message.type === 'RECORD_ACTION') {
    if (isRecording) {
      recordedActions.push(message.action);
    }
    sendResponse({ success: true, count: recordedActions.length });
  } else if (message.type === 'HANDOFF_SESSION') {
    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      const activeTab = tabs[0];
      if (!activeTab) {
        sendResponse({ success: false, error: 'No active tab found' });
        return;
      }

      try {
        const url = activeTab.url;
        const title = activeTab.title;
        
        const cookies = await chrome.cookies.getAll({ url });
        
        let localStorageData = {};
        try {
          const results = await chrome.scripting.executeScript({
            target: { tabId: activeTab.id },
            func: () => Object.assign({}, window.localStorage)
          });
          if (results && results[0] && results[0].result) {
            localStorageData = results[0].result;
          }
        } catch (e) {
          console.warn('Could not extract localStorage:', e);
        }

        const payload = {
          url,
          title,
          cookies,
          localStorage: localStorageData,
          actions: recordedActions
        };

        const backendUrl = 'http://localhost:8000/api/extension/handoff';
        const apiResponse = await fetch(backendUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (!apiResponse.ok) {
          throw new Error(`Server returned status ${apiResponse.status}`);
        }

        const data = await apiResponse.json();
        console.log('Session handed off successfully:', data);
        sendResponse({ success: true, data });
      } catch (err) {
        console.error('Failed to handoff session:', err);
        sendResponse({ success: false, error: err.message });
      }
    });
    return true;
  }
});
