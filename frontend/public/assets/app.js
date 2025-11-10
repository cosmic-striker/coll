// moved from src/js/app.js
(function () {
  const API_BASE = '/api';
  const TOKEN_KEY = 'dm_access_token';
  const REFRESH_KEY = 'dm_refresh_token';

  function getToken() { return localStorage.getItem(TOKEN_KEY); }
  function setToken(token) { if (token) localStorage.setItem(TOKEN_KEY, token); }
  function setRefreshToken(token) { if (token) localStorage.setItem(REFRESH_KEY, token); }
  function getRefreshToken() { return localStorage.getItem(REFRESH_KEY); }

  async function request(path, options = {}, retry = true) {
    const headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});
    const token = getToken(); if (token) headers['Authorization'] = 'Bearer ' + token;
    const resp = await fetch(API_BASE + path, Object.assign({}, options, { headers }));
    if (resp.status === 401 && retry && getRefreshToken()) {
      const refreshed = await refreshToken(); if (refreshed) return request(path, options, false);
    }
    if (!resp.ok) {
      let msg = 'Request failed';
      try { const data = await resp.json(); msg = data.msg || data.error || msg; } catch (_) {}
      throw new Error(msg);
    }
    const contentType = resp.headers.get('content-type') || '';
    if (contentType.includes('application/json')) return resp.json();
    return resp.text();
  }

  async function refreshToken() {
    try {
      const token = getRefreshToken(); if (!token) return false;
      const resp = await fetch(API_BASE + '/auth/refresh', { method: 'POST', headers: { 'Authorization': 'Bearer ' + token } });
      if (!resp.ok) return false; const data = await resp.json(); setToken(data.access_token); return true;
    } catch (_) { return false; }
  }

  const ApiClient = {
    isAuthenticated() { return Boolean(getToken()); },
    logout() { localStorage.removeItem(TOKEN_KEY); localStorage.removeItem(REFRESH_KEY); },
    async login(username, password) { const data = await request('/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) }, false); setToken(data.access_token); setRefreshToken(data.refresh_token); return data.user; },
    async getProfile() { return request('/auth/profile'); },
    // Users (admin only)
    async listUsers() { return request('/auth/users'); },
    async getUser(id) { return request(`/auth/users/${id}`); },
    async createUser(payload) { return request('/auth/users', { method: 'POST', body: JSON.stringify(payload) }); },
    async updateUser(id, payload) { return request(`/auth/users/${id}`, { method: 'PUT', body: JSON.stringify(payload) }); },
    async deleteUser(id) { return request(`/auth/users/${id}`, { method: 'DELETE' }); },
    // Devices
    async listDevices() { return request('/devices/'); },
    async getDevice(id) { return request(`/devices/${id}`); },
    async createDevice(payload) { return request('/devices/', { method: 'POST', body: JSON.stringify(payload) }); },
    async updateDevice(id, payload) { return request(`/devices/${id}`, { method: 'PUT', body: JSON.stringify(payload) }); },
    async deleteDevice(id) { return request(`/devices/${id}`, { method: 'DELETE' }); },
    async pollDevice(id) { return request(`/devices/${id}/poll`, { method: 'POST' }); },
    async devicesStatus() { return request('/devices/status'); },
    // Cameras
    async listCameras() { return request('/cameras/'); },
    async getCamera(id) { return request(`/cameras/${id}`); },
    async createCamera(payload) { return request('/cameras/', { method: 'POST', body: JSON.stringify(payload) }); },
    async updateCamera(id, payload) { return request(`/cameras/${id}`, { method: 'PUT', body: JSON.stringify(payload) }); },
    async deleteCamera(id) { return request(`/cameras/${id}`, { method: 'DELETE' }); },
    async cameraStream(id) { return request(`/cameras/${id}/stream`); },
    async testCamera(id) { return request(`/cameras/${id}/test`, { method: 'POST' }); },
    async camerasStatus() { return request('/cameras/status'); },
    // Alerts
    async listAlerts(params = {}) { const q = new URLSearchParams(params).toString(); const path = q ? `/alerts/?${q}` : '/alerts/'; return request(path); },
    async getAlert(id) { return request(`/alerts/${id}`); },
    async createAlert(payload) { return request('/alerts/', { method: 'POST', body: JSON.stringify(payload) }); },
    async acknowledgeAlert(id) { return request(`/alerts/${id}/acknowledge`, { method: 'POST' }); },
    async acknowledgeAllAlerts(payload = {}) { return request('/alerts/acknowledge-all', { method: 'POST', body: JSON.stringify(payload) }); },
    async deleteAlert(id) { return request(`/alerts/${id}`, { method: 'DELETE' }); },
    async alertsSummary() { return request('/alerts/summary'); },
    // Settings (admin only)
    async getSettings() { return request('/settings/'); },
    async updateSettings(payload) { return request('/settings/', { method: 'PUT', body: JSON.stringify(payload) }); },
    async testEmail() { return request('/settings/test-email', { method: 'POST' }); },
    async testSlack() { return request('/settings/test-slack', { method: 'POST' }); },
    async restartPolling() { return request('/settings/restart-polling', { method: 'POST' }); },
    async clearCache() { return request('/settings/clear-cache', { method: 'POST' }); }
  };

  window.ApiClient = ApiClient;
})();
