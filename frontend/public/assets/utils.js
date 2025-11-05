// Toast Notification System
(function() {
  const ToastManager = {
    container: null,
    
    init() {
      if (!this.container) {
        this.container = document.createElement('div');
        this.container.className = 'toast-container';
        document.body.appendChild(this.container);
      }
    },
    
    show(message, type = 'info', duration = 3000) {
      this.init();
      
      const toast = document.createElement('div');
      toast.className = `toast ${type}`;
      
      const icons = {
        success: '✓',
        error: '✕',
        warning: '!',
        info: 'ℹ'
      };
      
      const titles = {
        success: 'Success',
        error: 'Error',
        warning: 'Warning',
        info: 'Info'
      };
      
      toast.innerHTML = `
        <div class="toast-icon">${icons[type] || icons.info}</div>
        <div class="toast-content">
          <div class="toast-title">${titles[type] || titles.info}</div>
          <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" aria-label="Close">×</button>
        ${duration > 0 ? '<div class="toast-progress"></div>' : ''}
      `;
      
      const closeBtn = toast.querySelector('.toast-close');
      closeBtn.addEventListener('click', () => this.remove(toast));
      
      this.container.appendChild(toast);
      
      if (duration > 0) {
        setTimeout(() => this.remove(toast), duration);
      }
      
      return toast;
    },
    
    remove(toast) {
      toast.classList.add('removing');
      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 300);
    },
    
    success(message, duration) {
      return this.show(message, 'success', duration);
    },
    
    error(message, duration) {
      return this.show(message, 'error', duration);
    },
    
    warning(message, duration) {
      return this.show(message, 'warning', duration);
    },
    
    info(message, duration) {
      return this.show(message, 'info', duration);
    },
    
    promise(promise, messages = {}) {
      const defaultMessages = {
        loading: 'Loading...',
        success: 'Operation completed successfully',
        error: 'Operation failed'
      };
      const msgs = { ...defaultMessages, ...messages };
      
      const loadingToast = this.show(msgs.loading, 'info', 0);
      
      return promise
        .then((result) => {
          this.remove(loadingToast);
          this.success(msgs.success);
          return result;
        })
        .catch((error) => {
          this.remove(loadingToast);
          this.error(msgs.error + ': ' + (error.message || 'Unknown error'));
          throw error;
        });
    }
  };
  
  window.Toast = ToastManager;
})();

// Loading Overlay Utility
(function() {
  const LoadingManager = {
    show(element, message = 'Loading...') {
      if (typeof element === 'string') {
        element = document.querySelector(element);
      }
      
      if (!element) return;
      
      element.style.position = 'relative';
      
      const overlay = document.createElement('div');
      overlay.className = 'loading-overlay';
      overlay.innerHTML = `
        <div style="text-align: center;">
          <div class="loading large"></div>
          <div style="margin-top: 16px; color: var(--muted); font-size: 14px;">${message}</div>
        </div>
      `;
      
      element.appendChild(overlay);
      return overlay;
    },
    
    hide(element) {
      if (typeof element === 'string') {
        element = document.querySelector(element);
      }
      
      if (!element) return;
      
      const overlay = element.querySelector('.loading-overlay');
      if (overlay) {
        overlay.remove();
      }
    }
  };
  
  window.Loading = LoadingManager;
})();

// Utility Functions
window.Utils = {
  formatDate(dateString) {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    // Less than 1 minute
    if (diff < 60000) return 'Just now';
    
    // Less than 1 hour
    if (diff < 3600000) {
      const mins = Math.floor(diff / 60000);
      return `${mins} minute${mins > 1 ? 's' : ''} ago`;
    }
    
    // Less than 1 day
    if (diff < 86400000) {
      const hours = Math.floor(diff / 3600000);
      return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    }
    
    // Less than 7 days
    if (diff < 604800000) {
      const days = Math.floor(diff / 86400000);
      return `${days} day${days > 1 ? 's' : ''} ago`;
    }
    
    // Format as date
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  },
  
  getStatusBadge(status) {
    const normalizedStatus = (status || 'unknown').toLowerCase();
    return `<span class="status ${normalizedStatus}">${normalizedStatus}</span>`;
  },
  
  getSeverityBadge(severity) {
    const normalizedSeverity = (severity || 'info').toLowerCase();
    return `<span class="status ${normalizedSeverity}">${normalizedSeverity}</span>`;
  },
  
  confirm(message, title = 'Confirm Action') {
    return new Promise((resolve) => {
      if (confirm(message)) {
        resolve(true);
      } else {
        resolve(false);
      }
    });
  },
  
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
};
