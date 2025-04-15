
const DEBUG_ENABLED = false;
const DEBUG_TIMEOUT = 15000;

class HealthService {
  constructor() {
    this.debugActive = false;
  }

  async enableDebugMode() {
    try {
      const response = await fetch('/api/v1/admin/_enable_debug', {
        method: 'POST',
        headers: {
          'X-Correlation-ID': crypto.randomUUID()
        }
      });
      
      if (response.ok) {
        this.debugActive = true;
        setTimeout(() => {
          this.debugActive = false;
          console.warn('Debug mode automatically disabled');
        }, DEBUG_TIMEOUT);
      }
    } catch (error) {
      console.error('Debug activation failed:', error);
    }
  }

  async fetchSystemStatus() {
    const response = await fetch('/api/v1/system/status');
    const data = await response.json();
    
    if (this.debugActive && data._debug) {
      document.getElementById('debug-metadata').innerText = 
        `Build SHA: ${data._debug.build_sha}`;
    }
    return data;
  }
}


document.addEventListener('DOMContentLoaded', () => {
  const healthService = new HealthService();

  document.querySelector('.dev-tools-btn')?.addEventListener('click', () => {
    healthService.enableDebugMode();
  });
  

  setInterval(() => healthService.fetchSystemStatus(), 30000);
});