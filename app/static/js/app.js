// State Management
let steps = [];
let currentToken = localStorage.getItem('auto_macro_jwt') || null;
let currentUser = null;

// DOM Elements
const stepList = document.getElementById('step-list');
const stepCount = document.getElementById('step-count');
const codeOutput = document.getElementById('code-output');
const selectTargetLang = document.getElementById('select-target-lang');
const previewFilename = document.getElementById('preview-filename');
const inputFilename = document.getElementById('input-filename');

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
  setupActionTabSwitching();
  setupActionFormHandlers();
  setupAuthModalHandlers();
  setupGeneratorHandlers();
  
  if (currentToken) {
    fetchUserProfile();
  }
});

// Action Tab Switcher
function setupActionTabSwitching() {
  const tabs = document.querySelectorAll('.btn-action-tab');
  const forms = {
    mouse_click: document.getElementById('form-mouse'),
    key_binding: document.getElementById('form-key'),
    delay: document.getElementById('form-delay')
  };

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const action = tab.dataset.action;
      Object.keys(forms).forEach(key => {
        if (key === action) {
          forms[key].classList.remove('hidden');
        } else {
          forms[key].classList.add('hidden');
        }
      });
    });
  });
}

// Action Form Submissions
function setupActionFormHandlers() {
  document.getElementById('form-mouse').addEventListener('submit', (e) => {
    e.preventDefault();
    const x = parseInt(document.getElementById('input-x').value) || 0;
    const y = parseInt(document.getElementById('input-y').value) || 0;
    addStep({ action_type: 'mouse_click', x, y });
  });

  document.getElementById('form-key').addEventListener('submit', (e) => {
    e.preventDefault();
    const key = document.getElementById('input-key').value.trim() || 'enter';
    addStep({ action_type: 'key_binding', key });
  });

  document.getElementById('form-delay').addEventListener('submit', (e) => {
    e.preventDefault();
    const duration_ms = parseInt(document.getElementById('input-delay').value) || 1000;
    addStep({ action_type: 'delay', duration_ms });
  });

  document.getElementById('btn-clear-steps').addEventListener('click', () => {
    steps = [];
    renderSteps();
    triggerLivePreview();
  });
}

function addStep(stepObj) {
  steps.push(stepObj);
  renderSteps();
  triggerLivePreview();
}

function removeStep(index) {
  steps.splice(index, 1);
  renderSteps();
  triggerLivePreview();
}

function renderSteps() {
  stepCount.textContent = `${steps.length} Steps`;
  if (steps.length === 0) {
    stepList.innerHTML = '<li class="empty-state">No steps added yet. Choose an action above!</li>';
    return;
  }

  stepList.innerHTML = '';
  steps.forEach((s, idx) => {
    const li = document.createElement('li');
    li.className = 'step-item';
    
    let text = '';
    let badgeClass = '';
    if (s.action_type === 'mouse_click') {
      badgeClass = 'badge-click';
      text = `Click at (X: ${s.x}, Y: ${s.y})`;
    } else if (s.action_type === 'key_binding') {
      badgeClass = 'badge-key';
      text = `Press Key: "${s.key}"`;
    } else if (s.action_type === 'delay') {
      badgeClass = 'badge-delay';
      text = `Wait ${s.duration_ms} ms (${(s.duration_ms/1000).toFixed(1)}s)`;
    }

    li.innerHTML = `
      <div>
        <span class="step-badge ${badgeClass}">${s.action_type.toUpperCase()}</span>
        <span>${text}</span>
      </div>
      <button class="btn-text" onclick="removeStep(${idx})">✕</button>
    `;
    stepList.appendChild(li);
  });
}

// Live Code Generator API Integration
function setupGeneratorHandlers() {
  selectTargetLang.addEventListener('change', () => {
    updateFileExtensionTab();
    triggerLivePreview();
  });

  document.getElementById('btn-copy-code').addEventListener('click', () => {
    const text = codeOutput.textContent;
    navigator.clipboard.writeText(text);
    alert('Script code copied to clipboard!');
  });

  document.getElementById('btn-download').addEventListener('click', async () => {
    if (steps.length === 0) {
      alert('Please add at least one automation step before downloading!');
      return;
    }

    const payload = {
      target_language: selectTargetLang.value,
      output_name: inputFilename.value.trim() || 'script',
      steps: steps
    };

    try {
      const response = await fetch('/api/v1/scripts/export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error('Export failed');

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
    } catch (err) {
      alert('Failed to download script: ' + err.message);
    }
  });
}

async function triggerLivePreview() {
  const lang = selectTargetLang.value;
  updateFileExtensionTab();

  if (steps.length === 0) {
    codeOutput.textContent = '# Add steps on the left panel to preview generated script...';
    return;
  }

  const payload = {
    target_language: lang,
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
    codeOutput.textContent = '# Error generating script preview';
  }
}

function updateFileExtensionTab() {
  const map = { python: 'script.py', ahk: 'script.ahk', bash: 'script.sh' };
  previewFilename.textContent = map[selectTargetLang.value] || 'script.txt';
}

// Auth & User Management Modal Handlers
function setupAuthModalHandlers() {
  const modal = document.getElementById('auth-modal');
  const viewLogin = document.getElementById('modal-view-login');
  const viewRegister = document.getElementById('modal-view-register');
  const viewProfile = document.getElementById('modal-view-profile');

  document.getElementById('btn-login-modal').addEventListener('click', () => {
    showModalView(viewLogin);
  });

  document.getElementById('btn-register-modal').addEventListener('click', () => {
    showModalView(viewRegister);
  });

  document.getElementById('btn-profile').addEventListener('click', () => {
    if (currentUser) {
      document.getElementById('prof-username').textContent = currentUser.username;
      document.getElementById('prof-email').textContent = currentUser.email;
      document.getElementById('prof-fullname').textContent = currentUser.full_name || 'N/A';
      showModalView(viewProfile);
    }
  });

  document.getElementById('btn-close-modal').addEventListener('click', () => {
    modal.classList.add('hidden');
  });

  document.getElementById('link-to-register').addEventListener('click', (e) => {
    e.preventDefault();
    showModalView(viewRegister);
  });

  document.getElementById('link-to-login').addEventListener('click', (e) => {
    e.preventDefault();
    showModalView(viewLogin);
  });

  // Check Username Realtime Availability
  document.getElementById('reg-username').addEventListener('input', async (e) => {
    const name = e.target.value.trim();
    const hint = document.getElementById('username-check-status');
    if (name.length < 3) {
      hint.textContent = '';
      return;
    }
    const res = await fetch(`/api/v1/users/check-username/${name}`);
    if (res.ok) {
      const data = await res.json();
      if (data.is_available) {
        hint.textContent = '✓ Username is available';
        hint.style.color = '#3fb950';
      } else {
        hint.textContent = '✕ Username is taken';
        hint.style.color = '#f85149';
      }
    }
  });

  // Login Form Submit
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
      alert('Sign in successful!');
    } else {
      alert('Invalid username or password');
    }
  });

  // Register Form Submit
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
      alert('Account created successfully! Please sign in.');
      showModalView(viewLogin);
    } else {
      const err = await res.json();
      alert('Registration failed: ' + (err.detail || 'Error creating account'));
    }
  });

  // Change Password Form Submit
  document.getElementById('form-change-password').addEventListener('submit', async (e) => {
    e.preventDefault();
    const old_password = document.getElementById('pass-old').value;
    const new_password = document.getElementById('pass-new').value;

    const res = await fetch('/api/v1/auth/change-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentToken}`
      },
      body: JSON.stringify({ old_password, new_password })
    });

    if (res.ok) {
      alert('Password updated successfully!');
      modal.classList.add('hidden');
    } else {
      const err = await res.json();
      alert('Failed to change password: ' + (err.detail || 'Error'));
    }
  });

  // Logout
  document.getElementById('btn-logout').addEventListener('click', async () => {
    if (currentToken) {
      await fetch('/api/v1/auth/logout', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${currentToken}` }
      });
    }
    currentToken = null;
    currentUser = null;
    localStorage.removeItem('auto_macro_jwt');
    updateAuthUI();
  });
}

function showModalView(targetView) {
  const modal = document.getElementById('auth-modal');
  const views = [
    document.getElementById('modal-view-login'),
    document.getElementById('modal-view-register'),
    document.getElementById('modal-view-profile')
  ];

  views.forEach(v => v.classList.add('hidden'));
  targetView.classList.remove('hidden');
  modal.classList.remove('hidden');
}

async function fetchUserProfile() {
  if (!currentToken) return;
  try {
    const res = await fetch('/api/v1/users/me', {
      headers: { 'Authorization': `Bearer ${currentToken}` }
    });

    if (res.ok) {
      currentUser = await res.json();
      updateAuthUI();
    } else {
      currentToken = null;
      localStorage.removeItem('auto_macro_jwt');
      updateAuthUI();
    }
  } catch (e) {
    updateAuthUI();
  }
}

function updateAuthUI() {
  const statusArea = document.getElementById('user-status-area');
  const loggedInArea = document.getElementById('logged-in-area');
  const usernameLabel = document.getElementById('current-username');

  if (currentUser) {
    statusArea.classList.add('hidden');
    loggedInArea.classList.remove('hidden');
    usernameLabel.textContent = currentUser.username;
  } else {
    statusArea.classList.remove('hidden');
    loggedInArea.classList.add('hidden');
  }
}
