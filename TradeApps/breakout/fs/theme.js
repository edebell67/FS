// Breakout shared dark/light theme controller.
(function () {
    const STORAGE_KEY = 'breakout.theme';
    const THEMES = new Set(['dark', 'light']);
    const CSS_ID = 'breakout-theme-css';
    const TOGGLE_ID = 'breakout-theme-toggle';
    const FLOATING_ID = 'breakout-theme-floating-toggle';

    function getStoredTheme() {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            return THEMES.has(stored) ? stored : 'dark';
        } catch (_) {
            return 'dark';
        }
    }

    function setStoredTheme(theme) {
        try {
            localStorage.setItem(STORAGE_KEY, theme);
        } catch (_) { }
    }

    function applyTheme(theme) {
        const nextTheme = THEMES.has(theme) ? theme : 'dark';
        document.documentElement.dataset.theme = nextTheme;
        if (document.body) document.body.dataset.theme = nextTheme;
        setStoredTheme(nextTheme);
        syncToggleLabels(nextTheme);
    }

    function toggleTheme() {
        applyTheme(getStoredTheme() === 'light' ? 'dark' : 'light');
    }

    function ensureThemeCss() {
        if (document.getElementById(CSS_ID)) return;
        const link = document.createElement('link');
        link.id = CSS_ID;
        link.rel = 'stylesheet';
        link.href = '/theme.css?v=V20260423_0018';
        document.head.appendChild(link);
    }

    function syncToggleLabels(theme) {
        const nextLabel = theme === 'light' ? 'Light' : 'Dark';
        const nextIcon = theme === 'light' ? 'fa-sun' : 'fa-moon';
        document.querySelectorAll('[data-theme-toggle-label]').forEach(el => {
            el.textContent = nextLabel;
        });
        document.querySelectorAll('[data-theme-toggle-icon]').forEach(el => {
            el.classList.remove('fa-sun', 'fa-moon');
            el.classList.add(nextIcon);
        });
        document.querySelectorAll('.breakout-theme-toggle').forEach(el => {
            el.setAttribute('aria-label', `Switch to ${theme === 'light' ? 'dark' : 'light'} mode`);
            el.setAttribute('title', `Switch to ${theme === 'light' ? 'dark' : 'light'} mode`);
        });
    }

    function buildToggle(id, compact = false) {
        const button = document.createElement('button');
        button.id = id;
        button.type = 'button';
        button.className = `breakout-theme-toggle${compact ? ' compact' : ''}`;
        button.innerHTML = `
            <i class="fas fa-moon" data-theme-toggle-icon></i>
            <span data-theme-toggle-label>Dark</span>
        `;
        button.addEventListener('click', toggleTheme);
        return button;
    }

    function renderSidebarToggle() {
        const footer = document.querySelector('.sidebar-footer');
        if (!footer || document.getElementById(TOGGLE_ID)) return false;
        const versionText = footer.textContent.trim();
        footer.textContent = '';
        footer.appendChild(buildToggle(TOGGLE_ID));
        const version = document.createElement('div');
        version.className = 'sidebar-version';
        version.textContent = versionText;
        footer.appendChild(version);
        return true;
    }

    function renderFloatingToggle() {
        if (document.querySelector('.sidebar') || document.getElementById(FLOATING_ID)) return;
        document.body.appendChild(buildToggle(FLOATING_ID, true));
    }

    function initThemeUi() {
        ensureThemeCss();
        applyTheme(getStoredTheme());
        if (!renderSidebarToggle() && document.body) {
            renderFloatingToggle();
        }
        syncToggleLabels(getStoredTheme());
    }

    ensureThemeCss();
    applyTheme(getStoredTheme());

    window.BreakoutTheme = {
        apply: applyTheme,
        init: initThemeUi,
        toggle: toggleTheme,
        current: getStoredTheme
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initThemeUi);
    } else {
        initThemeUi();
    }
})();
