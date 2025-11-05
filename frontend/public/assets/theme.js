// Advanced Theme Manager with Multiple Color Themes and Mode Options
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('selectedTheme') || 'blue';
        this.currentMode = localStorage.getItem('selectedMode') || 'dark';
        
        // Define color themes with dark, light, and grey modes
        this.themes = {
            blue: {
                name: 'Blue Ocean',
                icon: '🌊',
                dark: {
                    bg: '#0f1419',
                    bgGradient: 'linear-gradient(135deg, #0f1419 0%, #1a1f2e 50%, #1e2536 100%)',
                    panel: '#1a1f2e',
                    panelHover: '#222938',
                    panelLight: '#252b3d',
                    text: '#e4e7f1',
                    textSecondary: '#a0a9c3',
                    primary: '#3b82f6',
                    primaryLight: '#60a5fa',
                    primaryGlow: 'rgba(59, 130, 246, 0.4)',
                    accent: '#8b5cf6',
                    border: 'rgba(255, 255, 255, 0.06)',
                },
                light: {
                    bg: '#f8fafc',
                    bgGradient: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%)',
                    panel: '#ffffff',
                    panelHover: '#f1f5f9',
                    panelLight: '#e2e8f0',
                    text: '#0f172a',
                    textSecondary: '#475569',
                    primary: '#2563eb',
                    primaryLight: '#3b82f6',
                    primaryGlow: 'rgba(37, 99, 235, 0.2)',
                    accent: '#7c3aed',
                    border: 'rgba(0, 0, 0, 0.08)',
                },
                grey: {
                    bg: '#18181b',
                    bgGradient: 'linear-gradient(135deg, #18181b 0%, #27272a 50%, #3f3f46 100%)',
                    panel: '#27272a',
                    panelHover: '#3f3f46',
                    panelLight: '#52525b',
                    text: '#e4e4e7',
                    textSecondary: '#a1a1aa',
                    primary: '#3b82f6',
                    primaryLight: '#60a5fa',
                    primaryGlow: 'rgba(59, 130, 246, 0.3)',
                    accent: '#8b5cf6',
                    border: 'rgba(255, 255, 255, 0.08)',
                }
            },
            purple: {
                name: 'Purple Night',
                icon: '🌙',
                dark: {
                    bg: '#1a0f2e',
                    bgGradient: 'linear-gradient(135deg, #1a0f2e 0%, #2d1b4e 50%, #3d2667 100%)',
                    panel: '#2d1b4e',
                    panelHover: '#3d2667',
                    panelLight: '#4d3380',
                    text: '#f0e7ff',
                    textSecondary: '#c4b5f3',
                    primary: '#a855f7',
                    primaryLight: '#c084fc',
                    primaryGlow: 'rgba(168, 85, 247, 0.4)',
                    accent: '#ec4899',
                    border: 'rgba(255, 255, 255, 0.08)',
                },
                light: {
                    bg: '#faf5ff',
                    bgGradient: 'linear-gradient(135deg, #faf5ff 0%, #f3e8ff 50%, #e9d5ff 100%)',
                    panel: '#ffffff',
                    panelHover: '#f3e8ff',
                    panelLight: '#e9d5ff',
                    text: '#4c1d95',
                    textSecondary: '#7c3aed',
                    primary: '#9333ea',
                    primaryLight: '#a855f7',
                    primaryGlow: 'rgba(147, 51, 234, 0.2)',
                    accent: '#db2777',
                    border: 'rgba(0, 0, 0, 0.08)',
                },
                grey: {
                    bg: '#1e1a24',
                    bgGradient: 'linear-gradient(135deg, #1e1a24 0%, #2d2736 50%, #3d3548 100%)',
                    panel: '#2d2736',
                    panelHover: '#3d3548',
                    panelLight: '#4d4559',
                    text: '#ebe7f0',
                    textSecondary: '#b5adc4',
                    primary: '#a855f7',
                    primaryLight: '#c084fc',
                    primaryGlow: 'rgba(168, 85, 247, 0.3)',
                    accent: '#ec4899',
                    border: 'rgba(255, 255, 255, 0.08)',
                }
            },
            green: {
                name: 'Forest Green',
                icon: '🌲',
                dark: {
                    bg: '#0a1810',
                    bgGradient: 'linear-gradient(135deg, #0a1810 0%, #14291f 50%, #1e3a2d 100%)',
                    panel: '#14291f',
                    panelHover: '#1e3a2d',
                    panelLight: '#284b3b',
                    text: '#e7f5ec',
                    textSecondary: '#a8d5ba',
                    primary: '#10b981',
                    primaryLight: '#34d399',
                    primaryGlow: 'rgba(16, 185, 129, 0.4)',
                    accent: '#06b6d4',
                    border: 'rgba(255, 255, 255, 0.06)',
                },
                light: {
                    bg: '#f0fdf4',
                    bgGradient: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%)',
                    panel: '#ffffff',
                    panelHover: '#dcfce7',
                    panelLight: '#bbf7d0',
                    text: '#14532d',
                    textSecondary: '#166534',
                    primary: '#059669',
                    primaryLight: '#10b981',
                    primaryGlow: 'rgba(5, 150, 105, 0.2)',
                    accent: '#0891b2',
                    border: 'rgba(0, 0, 0, 0.08)',
                },
                grey: {
                    bg: '#161b18',
                    bgGradient: 'linear-gradient(135deg, #161b18 0%, #25302a 50%, #34453c 100%)',
                    panel: '#25302a',
                    panelHover: '#34453c',
                    panelLight: '#43594e',
                    text: '#e7f0ec',
                    textSecondary: '#a8c4ba',
                    primary: '#10b981',
                    primaryLight: '#34d399',
                    primaryGlow: 'rgba(16, 185, 129, 0.3)',
                    accent: '#06b6d4',
                    border: 'rgba(255, 255, 255, 0.08)',
                }
            },
            orange: {
                name: 'Sunset Orange',
                icon: '🌅',
                dark: {
                    bg: '#1a0f08',
                    bgGradient: 'linear-gradient(135deg, #1a0f08 0%, #2e1f14 50%, #42301f 100%)',
                    panel: '#2e1f14',
                    panelHover: '#42301f',
                    panelLight: '#56412a',
                    text: '#fff5e7',
                    textSecondary: '#f3d5b5',
                    primary: '#f97316',
                    primaryLight: '#fb923c',
                    primaryGlow: 'rgba(249, 115, 22, 0.4)',
                    accent: '#eab308',
                    border: 'rgba(255, 255, 255, 0.06)',
                },
                light: {
                    bg: '#fffbf5',
                    bgGradient: 'linear-gradient(135deg, #fffbf5 0%, #fed7aa 50%, #fdba74 100%)',
                    panel: '#ffffff',
                    panelHover: '#fed7aa',
                    panelLight: '#fdba74',
                    text: '#7c2d12',
                    textSecondary: '#9a3412',
                    primary: '#ea580c',
                    primaryLight: '#f97316',
                    primaryGlow: 'rgba(234, 88, 12, 0.2)',
                    accent: '#ca8a04',
                    border: 'rgba(0, 0, 0, 0.08)',
                },
                grey: {
                    bg: '#1b1816',
                    bgGradient: 'linear-gradient(135deg, #1b1816 0%, #2d2725 50%, #403834 100%)',
                    panel: '#2d2725',
                    panelHover: '#403834',
                    panelLight: '#534843',
                    text: '#f0ebe7',
                    textSecondary: '#c4b5a8',
                    primary: '#f97316',
                    primaryLight: '#fb923c',
                    primaryGlow: 'rgba(249, 115, 22, 0.3)',
                    accent: '#eab308',
                    border: 'rgba(255, 255, 255, 0.08)',
                }
            },
            red: {
                name: 'Ruby Red',
                icon: '💎',
                dark: {
                    bg: '#1a0b0f',
                    bgGradient: 'linear-gradient(135deg, #1a0b0f 0%, #2e141e 50%, #421d2d 100%)',
                    panel: '#2e141e',
                    panelHover: '#421d2d',
                    panelLight: '#56263c',
                    text: '#ffe7ef',
                    textSecondary: '#f3b5c9',
                    primary: '#ef4444',
                    primaryLight: '#f87171',
                    primaryGlow: 'rgba(239, 68, 68, 0.4)',
                    accent: '#ec4899',
                    border: 'rgba(255, 255, 255, 0.06)',
                },
                light: {
                    bg: '#fff5f7',
                    bgGradient: 'linear-gradient(135deg, #fff5f7 0%, #ffe4e6 50%, #fecdd3 100%)',
                    panel: '#ffffff',
                    panelHover: '#ffe4e6',
                    panelLight: '#fecdd3',
                    text: '#7f1d1d',
                    textSecondary: '#991b1b',
                    primary: '#dc2626',
                    primaryLight: '#ef4444',
                    primaryGlow: 'rgba(220, 38, 38, 0.2)',
                    accent: '#db2777',
                    border: 'rgba(0, 0, 0, 0.08)',
                },
                grey: {
                    bg: '#1b1618',
                    bgGradient: 'linear-gradient(135deg, #1b1618 0%, #2d2527 50%, #403438 100%)',
                    panel: '#2d2527',
                    panelHover: '#403438',
                    panelLight: '#534348',
                    text: '#f0e7eb',
                    textSecondary: '#c4a8b5',
                    primary: '#ef4444',
                    primaryLight: '#f87171',
                    primaryGlow: 'rgba(239, 68, 68, 0.3)',
                    accent: '#ec4899',
                    border: 'rgba(255, 255, 255, 0.08)',
                }
            },
            cyan: {
                name: 'Cyan Wave',
                icon: '🌀',
                dark: {
                    bg: '#0a1418',
                    bgGradient: 'linear-gradient(135deg, #0a1418 0%, #14282e 50%, #1e3c42 100%)',
                    panel: '#14282e',
                    panelHover: '#1e3c42',
                    panelLight: '#285056',
                    text: '#e7f5f8',
                    textSecondary: '#a8d5e3',
                    primary: '#06b6d4',
                    primaryLight: '#22d3ee',
                    primaryGlow: 'rgba(6, 182, 212, 0.4)',
                    accent: '#0ea5e9',
                    border: 'rgba(255, 255, 255, 0.06)',
                },
                light: {
                    bg: '#f0fdff',
                    bgGradient: 'linear-gradient(135deg, #f0fdff 0%, #cffafe 50%, #a5f3fc 100%)',
                    panel: '#ffffff',
                    panelHover: '#cffafe',
                    panelLight: '#a5f3fc',
                    text: '#0c4a6e',
                    textSecondary: '#075985',
                    primary: '#0284c7',
                    primaryLight: '#0ea5e9',
                    primaryGlow: 'rgba(2, 132, 199, 0.2)',
                    accent: '#0891b2',
                    border: 'rgba(0, 0, 0, 0.08)',
                },
                grey: {
                    bg: '#161a1b',
                    bgGradient: 'linear-gradient(135deg, #161a1b 0%, #25302d 50%, #34453f 100%)',
                    panel: '#25302d',
                    panelHover: '#34453f',
                    panelLight: '#435951',
                    text: '#e7f0ed',
                    textSecondary: '#a8c4be',
                    primary: '#06b6d4',
                    primaryLight: '#22d3ee',
                    primaryGlow: 'rgba(6, 182, 212, 0.3)',
                    accent: '#0ea5e9',
                    border: 'rgba(255, 255, 255, 0.08)',
                }
            }
        };
        
        this.init();
    }
    
    init() {
        this.applyTheme();
        this.createThemeSelector();
        this.setupKeyboardShortcuts();
    }
    
    applyTheme() {
        const theme = this.themes[this.currentTheme][this.currentMode];
        const root = document.documentElement;
        
        // Add theme classes to body for better CSS targeting
        document.body.className = `theme-${this.currentTheme} mode-${this.currentMode}`;
        
        // Apply all color variables
        root.style.setProperty('--bg', theme.bg);
        root.style.setProperty('--bg-gradient', theme.bgGradient);
        root.style.setProperty('--panel', theme.panel);
        root.style.setProperty('--panel-hover', theme.panelHover);
        root.style.setProperty('--panel-light', theme.panelLight);
        root.style.setProperty('--text', theme.text);
        root.style.setProperty('--text-secondary', theme.textSecondary);
        root.style.setProperty('--primary', theme.primary);
        root.style.setProperty('--primary-light', theme.primaryLight);
        root.style.setProperty('--primary-glow', theme.primaryGlow);
        root.style.setProperty('--accent', theme.accent);
        root.style.setProperty('--border', theme.border);
        
        // Adjust shadows based on mode
        if (this.currentMode === 'light') {
            root.style.setProperty('--shadow-sm', '0 2px 8px rgba(0, 0, 0, 0.08)');
            root.style.setProperty('--shadow', '0 4px 20px rgba(0, 0, 0, 0.12)');
            root.style.setProperty('--shadow-lg', '0 10px 40px rgba(0, 0, 0, 0.15)');
        } else {
            root.style.setProperty('--shadow-sm', '0 2px 8px rgba(0, 0, 0, 0.15)');
            root.style.setProperty('--shadow', '0 4px 20px rgba(0, 0, 0, 0.25)');
            root.style.setProperty('--shadow-lg', '0 10px 40px rgba(0, 0, 0, 0.35)');
        }
        
        // Force re-render of all elements
        document.body.style.display = 'none';
        document.body.offsetHeight; // Trigger reflow
        document.body.style.display = '';
        
        // Save preferences
        localStorage.setItem('selectedTheme', this.currentTheme);
        localStorage.setItem('selectedMode', this.currentMode);
    }
    
    createThemeSelector() {
        // Remove existing selector if present
        const existing = document.getElementById('theme-selector-widget');
        if (existing) existing.remove();
        
        const widget = document.createElement('div');
        widget.id = 'theme-selector-widget';
        widget.innerHTML = `
            <style>
                #theme-selector-widget {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 10000;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                }
                
                .theme-toggle-btn {
                    background: var(--panel);
                    border: 2px solid var(--border);
                    color: var(--text);
                    padding: 12px 16px;
                    border-radius: 12px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: 600;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    box-shadow: var(--shadow-lg);
                    transition: all 0.3s ease;
                }
                
                .theme-toggle-btn:hover {
                    background: var(--panel-hover);
                    border-color: var(--primary);
                    transform: translateY(-2px);
                    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
                }
                
                .theme-panel {
                    position: absolute;
                    bottom: 70px;
                    right: 0;
                    background: var(--panel);
                    border: 2px solid var(--border);
                    border-radius: 16px;
                    padding: 20px;
                    box-shadow: var(--shadow-xl);
                    min-width: 320px;
                    display: none;
                    animation: slideUp 0.3s ease;
                }
                
                .theme-panel.show {
                    display: block;
                }
                
                @keyframes slideUp {
                    from {
                        opacity: 0;
                        transform: translateY(10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                .theme-section {
                    margin-bottom: 20px;
                }
                
                .theme-section:last-child {
                    margin-bottom: 0;
                }
                
                .theme-section-title {
                    color: var(--text-secondary);
                    font-size: 11px;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin-bottom: 12px;
                }
                
                .theme-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 8px;
                }
                
                .theme-option {
                    background: var(--panel-light);
                    border: 2px solid transparent;
                    padding: 12px 8px;
                    border-radius: 10px;
                    cursor: pointer;
                    text-align: center;
                    transition: all 0.2s ease;
                    font-size: 12px;
                    font-weight: 600;
                    color: var(--text);
                }
                
                .theme-option:hover {
                    background: var(--panel-hover);
                    border-color: var(--primary);
                    transform: scale(1.05);
                }
                
                .theme-option.active {
                    background: var(--primary);
                    color: white;
                    border-color: var(--primary);
                }
                
                .color-themes {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 8px;
                }
                
                .color-theme-btn {
                    background: var(--panel-light);
                    border: 2px solid transparent;
                    padding: 10px;
                    border-radius: 10px;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-size: 13px;
                    font-weight: 600;
                    color: var(--text);
                }
                
                .color-theme-btn:hover {
                    background: var(--panel-hover);
                    border-color: var(--primary);
                    transform: scale(1.03);
                }
                
                .color-theme-btn.active {
                    border-color: var(--primary);
                    background: var(--primary);
                    color: white;
                }
                
                .theme-icon {
                    font-size: 18px;
                }
                
                .keyboard-hint {
                    font-size: 10px;
                    color: var(--text-secondary);
                    text-align: center;
                    margin-top: 12px;
                    padding-top: 12px;
                    border-top: 1px solid var(--border);
                }
            </style>
            
            <button class="theme-toggle-btn" onclick="themeManager.togglePanel()">
                <span>🎨</span>
                <span>Themes</span>
            </button>
            
            <div class="theme-panel" id="theme-panel">
                <div class="theme-section">
                    <div class="theme-section-title">Mode</div>
                    <div class="theme-grid">
                        <div class="theme-option ${this.currentMode === 'dark' ? 'active' : ''}" onclick="themeManager.setMode('dark')">
                            🌙 Dark
                        </div>
                        <div class="theme-option ${this.currentMode === 'light' ? 'active' : ''}" onclick="themeManager.setMode('light')">
                            ☀️ Light
                        </div>
                        <div class="theme-option ${this.currentMode === 'grey' ? 'active' : ''}" onclick="themeManager.setMode('grey')">
                            ⚪ Grey
                        </div>
                    </div>
                </div>
                
                <div class="theme-section">
                    <div class="theme-section-title">Color Theme</div>
                    <div class="color-themes">
                        ${Object.keys(this.themes).map(key => `
                            <div class="color-theme-btn ${this.currentTheme === key ? 'active' : ''}" onclick="themeManager.setTheme('${key}')">
                                <span class="theme-icon">${this.themes[key].icon}</span>
                                <span>${this.themes[key].name}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="keyboard-hint">
                    💡 Press <strong>Ctrl+Shift+T</strong> to cycle modes<br>
                    Press <strong>Ctrl+Shift+C</strong> to cycle colors
                </div>
            </div>
        `;
        
        document.body.appendChild(widget);
        
        // Close panel when clicking outside
        document.addEventListener('click', (e) => {
            const panel = document.getElementById('theme-panel');
            const widget = document.getElementById('theme-selector-widget');
            if (panel && widget && !widget.contains(e.target)) {
                panel.classList.remove('show');
            }
        });
    }
    
    togglePanel() {
        const panel = document.getElementById('theme-panel');
        panel.classList.toggle('show');
    }
    
    setTheme(theme) {
        this.currentTheme = theme;
        this.applyTheme();
        this.createThemeSelector();
        this.showToast(`${this.themes[theme].icon} ${this.themes[theme].name} theme applied!`);
    }
    
    setMode(mode) {
        this.currentMode = mode;
        this.applyTheme();
        this.createThemeSelector();
        const modeNames = { dark: '🌙 Dark', light: '☀️ Light', grey: '⚪ Grey' };
        this.showToast(`${modeNames[mode]} mode activated!`);
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+Shift+T to cycle modes
            if (e.ctrlKey && e.shiftKey && e.key === 'T') {
                e.preventDefault();
                const modes = ['dark', 'light', 'grey'];
                const currentIndex = modes.indexOf(this.currentMode);
                const nextMode = modes[(currentIndex + 1) % modes.length];
                this.setMode(nextMode);
            }
            
            // Ctrl+Shift+C to cycle color themes
            if (e.ctrlKey && e.shiftKey && e.key === 'C') {
                e.preventDefault();
                const themes = Object.keys(this.themes);
                const currentIndex = themes.indexOf(this.currentTheme);
                const nextTheme = themes[(currentIndex + 1) % themes.length];
                this.setTheme(nextTheme);
            }
        });
    }
    
    showToast(message) {
        // Remove existing toast
        const existing = document.getElementById('theme-toast');
        if (existing) existing.remove();
        
        const toast = document.createElement('div');
        toast.id = 'theme-toast';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--panel);
            color: var(--text);
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: var(--shadow-lg);
            border: 2px solid var(--primary);
            z-index: 10001;
            font-weight: 600;
            font-size: 14px;
            animation: toastSlide 0.3s ease;
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes toastSlide {
                from {
                    opacity: 0;
                    transform: translateX(100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.transition = 'all 0.3s ease';
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100px)';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Initialize theme manager when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.themeManager = new ThemeManager();
    });
} else {
    window.themeManager = new ThemeManager();
}
