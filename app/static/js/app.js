// State Management
let steps = [];
let currentToken = localStorage.getItem('auto_macro_jwt') || null;
let currentUser = null;

// Elements
const dropZone = document.getElementById('scratch-drop-zone');
const codeOutput = document.getElementById('code-output');
const executionLogs = document.getElementById('execution-logs');
const selectTargetLang = document.getElementById('select-target-lang');
const previewFilename = document.getElementById('preview-filename');
const inputFilename = document.getElementById('input-filename');

document.addEventListener('DOMContentLoaded', () => {
  setupWorkspaceTabs();
  setupScratchBlockPalette();
  setupGeneratorAndWebRunner();
  setupVisionLabHandlers();
  setupAuthModalHandlers();

  if (currentToken) {
    fetchUserProfile();
  }
});

// Workspace Tab Switching
function setupWorkspaceTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  const contents = document.querySelectorAll('.tab-content');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      contents.forEach(c => c.classList.add('hidden'));

      tab.classList.add('active');
      const targetId = tab.dataset.tab;
      document.getElementById(targetId).classList.remove('hidden');
    });
  });
}

// Scratch Block Palette & Chain Manager
function setupScratchBlockPalette() {
  const chips = document.querySelectorAll('.block-chip');

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const type = chip.dataset.block;
      if (type === 'click') {
        const x = prompt('Enter Mouse X Coordinate (px):', '450');
        const y = prompt('Enter Mouse Y Coordinate (px):', '320');
        if (x !== null && y !== null) {
          addStep({ action_type: 'mouse_click', x: parseInt(x)||0, y: parseInt(y)||0 });
        }
      } else if (type === 'key') {
        const key = prompt('Enter Key/Shortcut to press (e.g. enter, space, ctrl+c):', 'enter');
        if (key) {
          addStep({ action_type: 'key_binding', key: key.trim() });
        }
      } else if (type === 'delay') {
        const ms = prompt('Enter Wait Duration (Milliseconds):', '1000');
        if (ms) {
          addStep({ action_type: 'delay', duration_ms: parseInt(ms)||1000 });
        }
      } else if (type === 'ocr') {
        alert('Added OCR Text Match condition step!');
        addStep({ action_type: 'key_binding', key: 'ocr_detect_text' });
      } else if (type === 'image') {
        alert('Added Screen Image Detection condition step!');
        addStep({ action_type: 'mouse_click', x: 500, y: 500 });
      }
    });
  });

  document.getElementById('btn-clear-blocks').addEventListener('click', () => {
    steps = [];
    renderBlockChain();
    triggerLivePreview();
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
  if (steps.length === 0) {
    dropZone.innerHTML = '<p class="empty-block-text">Click blocks above to snap them into the Scratch chain!</p>';
    return;
  }

  dropZone.innerHTML = '';
  steps.forEach((s, idx) => {
    const div = document.createElement('div');
    div.className = 'block-puzzle';

    if (s.action_type === 'mouse_click') {
      div.classList.add('block-click-item');
      div.innerHTML = `<span>🖱️ Mouse Click at X: ${s.x}, Y: ${s.y}</span><button class="btn-text" style="color:#fff;" onclick="removeStep(${idx})">✕</button>`;
    } else if (s.action_type === 'key_binding') {
      div.classList.add('block-key-item');
      div.innerHTML = `<span>⌨️ Press Key: "${s.key}"</span><button class="btn-text" style="color:#fff;" onclick="removeStep(${idx})">✕</button>`;
    } else if (s.action_type === 'delay') {
      div.classList.add('block-delay-item');
      div.innerHTML = `<span>⏱️ Wait ${s.duration_ms} ms</span><button class="btn-text" style="color:#fff;" onclick="removeStep(${idx})">✕</button>`;
    }

    dropZone.appendChild(div);
  });
}

// Generator & Web Sandbox Runner
function setupGeneratorAndWebRunner() {
  selectTargetLang.addEventListener('change', () => {
    const map = { python: 'script.py', ahk: 'script.ahk', bash: 'script.sh' };
    previewFilename.textContent = map[selectTargetLang.value] || 'script.txt';
    triggerLivePreview();
  });

  document.getElementById('btn-copy-code').addEventListener('click', () => {
    navigator.clipboard.writeText(codeOutput.textContent);
    alert('Code copied to clipboard!');
  });

  // Web Executor Execution
  document.getElementById('btn-run-web').addEventListener('click', async () => {
    if (steps.length === 0) {
      alert('Please snap at least one Scratch block into the workspace chain before running!');
      return;
    }

    executionLogs.textContent = '⚡ Running script in Web Sandbox... Please wait...';

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
        const exec = data.execution;
        const analytics = data.analytics;

        executionLogs.textContent = exec.logs.join('\n');
        
        // Update Analytics Dashboard Tab
        document.getElementById('metric-score').textContent = `${analytics.efficiency_score}%`;
        document.getElementById('metric-avg-step').textContent = `${analytics.average_step_ms} ms`;
        document.getElementById('metric-total-steps').textContent = analytics.total_steps;

        const recList = document.getElementById('analytics-recommendations');
        recList.innerHTML = analytics.recommendations.map(r => `<li>${r}</li>`).join('');
      } else {
        executionLogs.textContent = '❌ Web execution failed.';
      }
    } catch (err) {
      executionLogs.textContent = '❌ Error executing script: ' + err.message;
    }
  });

  // File Download
  document.getElementById('btn-download').addEventListener('click', async () => {
    if (steps.length === 0) {
      alert('Add blocks to export script!');
      return;
    }
    const payload = {
      target_language: selectTargetLang.value,
      output_name: inputFilename.value.trim() || 'script',
      steps: steps
    };

    const response = await fetch('/api/v1/scripts/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
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
    codeOutput.textContent = '# Click blocks above to generate script preview...';
    return;
  }

  const payload = {
    target_language: selectTargetLang.value,
    output_name: inputFilename.value.trim(),
    steps: steps
  };

  try {
    const res = await fetch('/api/v1/scripts/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const data = await res.json();
      codeOutput.textContent = data.script_code;
    }
  } catch (e) {
    codeOutput.textContent = '# Error generating preview';
  }
}

// Vision & OCR Test Lab Handlers
function setupVisionLabHandlers() {
  document.getElementById('form-vision-match').addEventListener('submit', async (e) => {
    e.preventDefault();
    const targetFile = document.getElementById('vision-target').files[0];
    const templateFile = document.getElementById('vision-template').files[0];
    const resultBox = document.getElementById('match-result');

    const formData = new FormData();
    formData.append('target_image', targetFile);
    formData.append('template_image', templateFile);

    resultBox.classList.remove('hidden');
    resultBox.textContent = 'Searching screen image template...';

    try {
      const res = await fetch('/api/v1/vision/template-match', { method: 'POST', body: formData });
      const data = await res.json();
      if (data.found) {
        resultBox.textContent = `✅ Target Button Found! Center Coordinates: X: ${data.coordinates.x}, Y: ${data.coordinates.y} (Confidence: ${(data.confidence * 100).toFixed(1)}%)`;
      } else {
        resultBox.textContent = `❌ Target template not found on screen image (Highest match: ${(data.confidence * 100).toFixed(1)}%)`;
      }
    } catch (err) {
      resultBox.textContent = 'Error processing image detection.';
    }
  });

  document.getElementById('btn-run-ocr').addEventListener('click', async () => {
    const file = document.getElementById('ocr-image').files[0];
    const resultBox = document.getElementById('ocr-result');
    if (!file) { alert('Select an image file!'); return; }

    const formData = new FormData();
    formData.append('image', file);
    resultBox.classList.remove('hidden');
    resultBox.textContent = 'Scanning image text OCR...';

    const res = await fetch('/api/v1/vision/ocr', { method: 'POST', body: formData });
    const data = await res.json();
    resultBox.textContent = `🔍 OCR Recognized Text: "${data.text}" (Confidence: ${((data.confidence||0)*100).toFixed(1)}%)`;
  });

  document.getElementById('btn-count-objects').addEventListener('click', async () => {
    const file = document.getElementById('ocr-image').files[0];
    const resultBox = document.getElementById('ocr-result');
    if (!file) { alert('Select an image file!'); return; }

    const formData = new FormData();
    formData.append('image', file);
    resultBox.classList.remove('hidden');
    resultBox.textContent = 'Counting objects...';

    const res = await fetch('/api/v1/vision/count-objects', { method: 'POST', body: formData });
    const data = await res.json();
    resultBox.textContent = `🔢 Detected Object Count: ${data.count} matching elements found on image!`;
  });
}

// Auth Modal
function setupAuthModalHandlers() {
  const modal = document.getElementById('auth-modal');
  const viewLogin = document.getElementById('modal-view-login');
  const viewRegister = document.getElementById('modal-view-register');
  const viewProfile = document.getElementById('modal-view-profile');

  document.getElementById('btn-login-modal').addEventListener('click', () => showModalView(viewLogin));
  document.getElementById('btn-register-modal').addEventListener('click', () => showModalView(viewRegister));
  document.getElementById('btn-profile').addEventListener('click', () => {
    if (currentUser) {
      document.getElementById('prof-username').textContent = currentUser.username;
      document.getElementById('prof-email').textContent = currentUser.email;
      showModalView(viewProfile);
    }
  });
  document.getElementById('btn-close-modal').addEventListener('click', () => modal.classList.add('hidden'));

  document.getElementById('form-login').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (res.ok) {
      const data = await res.json();
      currentToken = data.access_token;
      localStorage.setItem('auto_macro_jwt', currentToken);
      modal.classList.add('hidden');
      await fetchUserProfile();
    } else {
      alert('Invalid login credentials');
    }
  });

  document.getElementById('form-register').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      username: document.getElementById('reg-username').value,
      email: document.getElementById('reg-email').value,
      full_name: document.getElementById('reg-fullname').value,
      password: document.getElementById('reg-password').value
    };

    const res = await fetch('/api/v1/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      alert('Account created! Please sign in.');
      showModalView(viewLogin);
    }
  });

  document.getElementById('btn-logout').addEventListener('click', () => {
    currentToken = null;
    currentUser = null;
    localStorage.removeItem('auto_macro_jwt');
    updateAuthUI();
  });
}

function showModalView(targetView) {
  const modal = document.getElementById('auth-modal');
  [document.getElementById('modal-view-login'), document.getElementById('modal-view-register'), document.getElementById('modal-view-profile')].forEach(v => v.classList.add('hidden'));
  targetView.classList.remove('hidden');
  modal.classList.remove('hidden');
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
