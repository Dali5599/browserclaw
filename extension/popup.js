document.addEventListener('DOMContentLoaded', async () => {
  const recordBtn = document.getElementById('recordBtn');
  const handoffBtn = document.getElementById('handoffBtn');
  const statusBadge = document.getElementById('statusBadge');
  const statusMsg = document.getElementById('statusMsg');

  function updateUI(state) {
    if (state.isRecording) {
      recordBtn.textContent = 'Stop Recording';
      recordBtn.classList.add('recording');
      statusBadge.textContent = 'Recording';
      statusBadge.className = 'status recording';
    } else {
      recordBtn.textContent = 'Start Recording';
      recordBtn.classList.remove('recording');
      statusBadge.textContent = 'Idle';
      statusBadge.className = 'status idle';
    }

    if (state.actionsCount && state.actionsCount > 0) {
      handoffBtn.disabled = false;
      statusMsg.textContent = `${state.actionsCount} actions captured`;
    } else {
      handoffBtn.disabled = true;
    }
  }

  const response = await chrome.runtime.sendMessage({ type: 'GET_STATE' });
  if (response) {
    updateUI(response);
  }

  recordBtn.addEventListener('click', async () => {
    const res = await chrome.runtime.sendMessage({ type: 'TOGGLE_RECORDING' });
    updateUI(res);
  });

  handoffBtn.addEventListener('click', async () => {
    statusMsg.textContent = 'Handing off session...';
    handoffBtn.disabled = true;
    const res = await chrome.runtime.sendMessage({ type: 'HANDOFF_SESSION' });
    if (res && res.success) {
      statusMsg.textContent = 'Handoff successful!';
      setTimeout(() => { statusMsg.textContent = ''; }, 3000);
    } else {
      statusMsg.textContent = 'Handoff failed: ' + (res?.error || 'Unknown error');
      handoffBtn.disabled = false;
    }
  });
});
