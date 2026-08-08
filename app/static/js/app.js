// State Management
let steps = [];
let currentToken = localStorage.getItem('auto_macro_jwt') || null;
let currentUser = null;
let isTrackingOsMouse = false;
let trackingInterval = null;
let lastCapturedX = 0;
let lastCapturedY = 0;

// DOM Elements
const blockChainList = document.getElementById('block-chain-list');
const chainStepCount = document.getElementById('chain-step-count');
const codeOutput = document.getElementById('code-output');
const executionLogs = document.getElementById('execution-logs');
const selectTargetLang = document.getElementById('select-target-lang');
const inputFilename = document.getElementById('input-filename');
const liveMousePos = document.getElementById('live-mouse-pos');

document.addEventListener('DOMContentLoaded', () => {
  setupPaletteClickHandlers();
  setupOsMouseTrackingToggle();
  setupSimTabs();
  setupWebExecution();
  setupAuthModalHandlers();

  if (currentToken) {
    fetchUserProfile();
  }
});

// Palette Block Adders
function setupPaletteClickHandlers() {
  let defaultCounter = 1;
  const blocks = document.querySelectorAll('.palette-block');
  blocks.forEach(block => {
    block.addEventListener('click', () => {
      const type = block.dataset.type;
      if (type === 'click') {
        const defaultX = 200 + (defaultCounter * 45) % 400;
        const defaultY = 150 + (defaultCounter * 35) % 250;
        defaultCounter++;
        const x = prompt('Enter Mouse X Coordinate (px):', defaultX.toString());
        const y = prompt('Enter Mouse Y Coordinate (px):', defaultY.toString());
        if (x !== null && y !== null) {
          addStep({ action_type: 'mouse_click', x: parseInt(x) || 0, y: parseInt(y) || 0 });
        }
      } else if (type === 'key') {
        const key = prompt('Enter Key / Shortcut (e.g. enter, space, ctrl+c):', 'enter');
        if (key) addStep({ action_type: 'key_binding', key: key.trim() });
      } else if (type === 'delay') {
        const ms = prompt('Enter Wait Duration (Milliseconds):', '1000');
        if (ms) addStep({ action_type: 'delay', duration_ms: parseInt(ms) || 1000 });
      } else if (type === 'ocr') {
        addStep({ action_type: 'key_binding', key: 'ocr_read_text' });
      } else if (type === 'image') {
        const imgX = 300 + (defaultCounter * 20) % 300;
        const imgY = 200 + (defaultCounter * 15) % 200;
        defaultCounter++;
        addStep({ action_type: 'mouse_click', x: imgX, y: imgY });
      }
    });
  });

  document.getElementById('btn-clear-chain').addEventListener('click', () => {
    steps = [];
    renderBlockChain();
    triggerLivePreview();
  });
}

  let isTrackingOsMouse = false;
  let trackingInterval = null;
  let windowMouseMoveHandler = null;
  let lastCapturedX = 0;
  let lastCapturedY = 0;

  const btnFetchOsMouse = document.getElementById('btn-fetch-os-mouse');
  if (btnFetchOsMouse) {
    btnFetchOsMouse.addEventListener('click', async () => {
      if (!isTrackingOsMouse) {
        // Start Continuous Tracking
        isTrackingOsMouse = true;
        btnFetchOsMouse.classList.add('btn-tracking-active');
        btnFetchOsMouse.innerHTML = '🔴 Tracking Mouse (Click to Stop & Capture)';

        // 1. Browser Native Real Mouse Tracker (Accurate pixel coordinates)
        windowMouseMoveHandler = (e) => {
          lastCapturedX = e.screenX || e.clientX;
          lastCapturedY = e.screenY || e.clientY;
          liveMousePos.textContent = `📍 Mouse: X: ${lastCapturedX}, Y: ${lastCapturedY}`;
        };
        window.addEventListener('mousemove', windowMouseMoveHandler);
        
        // 2. Fallback OS backend polling
        trackingInterval = setInterval(async () => {
          try {
            const res = await fetch('/api/v1/vision/desktop-mouse-position');
            const data = await res.json();
            if (data.status === "success") {
              lastCapturedX = data.x;
              lastCapturedY = data.y;
              liveMousePos.textContent = `📍 OS Mouse: X: ${data.x}, Y: ${data.y}`;
            }
          } catch (e) {}
        }, 150);

      } else {
        // Stop Continuous Tracking & Add Step
        isTrackingOsMouse = false;
        if (trackingInterval) clearInterval(trackingInterval);
        if (windowMouseMoveHandler) window.removeEventListener('mousemove', windowMouseMoveHandler);
        trackingInterval = null;
        windowMouseMoveHandler = null;

        btnFetchOsMouse.classList.remove('btn-tracking-active');
        btnFetchOsMouse.innerHTML = '🖥️ Track Real Desktop X,Y';

        alert(`✅ Captured Mouse Position:\nX: ${lastCapturedX}, Y: ${lastCapturedY}\n\nAdded click step to workspace!`);
        addStep({ action_type: 'mouse_click', x: lastCapturedX, y: lastCapturedY });
      }
    });
  }

function addStep(stepObj) {
  steps.push(stepObj);
  renderBlockChain();
  triggerLivePreview();
}

function removeStep(idx) {
  steps.splice(idx, 1);
  renderBlockChain();
  triggerLivePreview();
}

function renderBlockChain() {
  chainStepCount.textContent = `${steps.length} Steps`;
  if (steps.length === 0) {
    blockChainList.innerHTML = `
      <div class="empty-canvas-prompt">
        <span class="prompt-icon">🧩</span>
        <p>Your workspace is empty.</p>
        <small>Click blocks above or use "Track Real Desktop X,Y" to capture coordinates!</small>
      </div>`;
    return;
  }

  blockChainList.innerHTML = '';
  steps.forEach((s, idx) => {
    const div = document.createElement('div');
    div.className = `chain-block type-${s.action_type === 'mouse_click' ? 'click' : s.action_type === 'key_binding' ? 'key' : 'delay'}`;

    let label = '';
    if (s.action_type === 'mouse_click') label = `🖱️ Mouse Click at X: ${s.x}, Y: ${s.y}`;
    else if (s.action_type === 'key_binding') label = `⌨️ Press Key: "${s.key}"`;
    else if (s.action_type === 'delay') label = `⏱️ Wait ${s.duration_ms} ms (${(s.duration_ms/1000).toFixed(1)}s)`;

    div.innerHTML = `
      <span>Step ${idx + 1}: ${label}</span>
      <button class="btn-text" style="color:#fff;" onclick="removeStep(${idx})">✕</button>
    `;
    blockChainList.appendChild(div);
  });
}

// Server API Web Execution & Code Preview
function setupWebExecution() {
  document.getElementById('btn-web-run').addEventListener('click', async () => {
    if (steps.length === 0) {
      alert('Please add at least one step to execute!');
      return;
    }

    switchSimTab('tab-logs');
    executionLogs.textContent = '🚀 Sending execution payload to Server API...';

    try {
      const res = await fetch('/api/v1/runner/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target_language: selectTargetLang.value,
          output_name: inputFilename.value.trim(),
          steps: steps
        })
      });

      if (res.ok) {
        const data = await res.json();
        executionLogs.textContent = data.execution.logs.join('\n');
      } else {
        executionLogs.textContent = '❌ Web execution failed.';
      }
    } catch (e) {
      executionLogs.textContent = '❌ Error executing script: ' + e.message;
    }
  });

  selectTargetLang.addEventListener('change', triggerLivePreview);

  document.getElementById('btn-copy-code').addEventListener('click', () => {
    navigator.clipboard.writeText(codeOutput.textContent);
    alert('Code copied to clipboard!');
  });

  document.getElementById('btn-download').addEventListener('click', async () => {
    if (steps.length === 0) return;
    const response = await fetch('/api/v1/scripts/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_language: selectTargetLang.value,
        output_name: inputFilename.value.trim() || 'script',
        steps: steps
      })
    });

    if (response.ok) {
      const blob = await response.blob();
      const extMap = { python: '.py', ahk: '.ahk', bash: '.sh' };
      const ext = extMap[selectTargetLang.value] || '.txt';
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = `${inputFilename.value.trim() || 'script'}${ext}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    }
  });
}

async function triggerLivePreview() {
  if (steps.length === 0) {
    codeOutput.textContent = '# Script preview will generate automatically when blocks are added...';
    return;
  }

  const res = await fetch('/api/v1/scripts/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      target_language: selectTargetLang.value,
      output_name: inputFilename.value.trim(),
      steps: steps
    })
  });
  if (res.ok) {
    const data = await res.json();
    codeOutput.textContent = data.script_code;
  }
}

// Right Panel Tab Switcher
function setupSimTabs() {
  const tabs = document.querySelectorAll('.sim-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      switchSimTab(tab.dataset.tab);
    });
  });
}

function switchSimTab(tabId) {
  const tabs = document.querySelectorAll('.sim-tab');
  const contents = document.querySelectorAll('.sim-tab-content');

  tabs.forEach(t => t.classList.remove('active'));
  contents.forEach(c => c.classList.add('hidden'));

  const activeTab = Array.from(tabs).find(t => t.dataset.tab === tabId);
  if (activeTab) activeTab.classList.add('active');
  document.getElementById(tabId).classList.remove('hidden');
}

// Auth Modal
function setupAuthModalHandlers() {
  const modal = document.getElementById('auth-modal');
  const viewLogin = document.getElementById('modal-view-login');
  const viewRegister = document.getElementById('modal-view-register');

  document.getElementById('btn-login-modal').addEventListener('click', () => {
    viewRegister.classList.add('hidden');
    viewLogin.classList.remove('hidden');
    modal.classList.remove('hidden');
  });

  document.getElementById('btn-register-modal').addEventListener('click', () => {
    viewLogin.classList.add('hidden');
    viewRegister.classList.remove('hidden');
    modal.classList.remove('hidden');
  });

  document.getElementById('btn-close-modal').addEventListener('click', () => modal.classList.add('hidden'));

  document.getElementById('form-login').addEventListener('submit', async (e) => {
    e.preventDefault();
    const res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: document.getElementById('login-username').value,
        password: document.getElementById('login-password').value
      })
    });

    if (res.ok) {
      const data = await res.json();
      currentToken = data.access_token;
      localStorage.setItem('auto_macro_jwt', currentToken);
      modal.classList.add('hidden');
      await fetchUserProfile();
    } else alert('Invalid credentials');
  });

  document.getElementById('form-register').addEventListener('submit', async (e) => {
    e.preventDefault();
    const res = await fetch('/api/v1/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: document.getElementById('reg-username').value,
        email: document.getElementById('reg-email').value,
        password: document.getElementById('reg-password').value
      })
    });

    if (res.ok) {
      alert('Registered! Sign in now.');
      viewRegister.classList.add('hidden');
      viewLogin.classList.remove('hidden');
    }
  });

  document.getElementById('btn-logout').addEventListener('click', () => {
    currentToken = null; currentUser = null;
    localStorage.removeItem('auto_macro_jwt');
    updateAuthUI();
  });
}

async function fetchUserProfile() {
  if (!currentToken) return;
  const res = await fetch('/api/v1/users/me', { headers: { 'Authorization': `Bearer ${currentToken}` } });
  if (res.ok) {
    currentUser = await res.json();
    updateAuthUI();
  }
}

function updateAuthUI() {
  const statusArea = document.getElementById('user-status-area');
  const loggedInArea = document.getElementById('logged-in-area');
  if (currentUser) {
    statusArea.classList.add('hidden');
    loggedInArea.classList.remove('hidden');
    document.getElementById('current-username').textContent = currentUser.username;
  } else {
    statusArea.classList.remove('hidden');
    loggedInArea.classList.add('hidden');
  }
}
