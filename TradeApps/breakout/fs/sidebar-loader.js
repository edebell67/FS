/**
 * Sidebar Loader - Shared sidebar injection for all pages
 * V20260122_FS
 */
(function () {
    function loadThemeController(callback) {
        if (window.BreakoutTheme) {
            window.BreakoutTheme.init();
            if (callback) callback();
            return;
        }
        const existing = document.getElementById('breakout-theme-script');
        if (existing) {
            existing.addEventListener('load', () => {
                if (window.BreakoutTheme) window.BreakoutTheme.init();
                if (callback) callback();
            }, { once: true });
            return;
        }
        const script = document.createElement('script');
        script.id = 'breakout-theme-script';
        script.src = '/theme.js?v=V20260423_0018';
        script.onload = () => {
            if (window.BreakoutTheme) window.BreakoutTheme.init();
            if (callback) callback();
        };
        document.head.appendChild(script);
    }

    loadThemeController();

    // Get current page name from URL
    const currentPath = window.location.pathname;
    const currentPage = currentPath.split('/').pop().replace('.html', '') || 'trade_viewer';

    // Fetch and inject sidebar
    fetch('/sidebar.html')
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById('sidebar-container');
            if (container) {
                container.innerHTML = html;

                // Set active state based on current page
                const links = container.querySelectorAll('.sidebar-link');
                links.forEach(link => {
                    const page = link.getAttribute('data-page');
                    if (page === currentPage) {
                        link.classList.add('active');
                    }
                });
                if (window.BreakoutTheme) window.BreakoutTheme.init();
                else loadThemeController();
            }
        })
        .catch(err => {
            console.error('Failed to load sidebar:', err);
        });

    // [V20260130_1315] Global Health Monitor
    function initHealthMonitor() {
        const healthStyleId = 'global-health-alarm-style';

        async function checkHealth() {
            try {
                // [V20260215_Midnight] User wants alarm ONLY in LIVE mode
                const runModeEl = document.getElementById('runMode');
                const isSim = runModeEl && (runModeEl.value || '').toLowerCase() === 'sim';
                
                let styleEl = document.getElementById(healthStyleId);
                
                // If in SIM mode, remove alarm and exit
                if (isSim) {
                    if (styleEl) styleEl.remove();
                    return;
                }

                const response = await fetch('/api/system_health');
                const text = await response.text();
                let data = null;
                try {
                    data = JSON.parse(text);
                } catch (e) {
                    console.warn('[HEALTH] Non-JSON response from /api/system_health:', text.slice(0, 180));
                    return;
                }

                // If either check fails, go RED (Live only)
                if (data.healthy === false) {
                    console.warn('[HEALTH] Issue detected!', data.checks);
                    if (!styleEl) {
                        styleEl = document.createElement('style');
                        styleEl.id = healthStyleId;
                        // Fluorescent Red Glow effect
                        styleEl.innerHTML = `
                            h1, h2, .navbar-brand, .app-title, .page-title, .sidebar-header, #logo, .brand-text {
                                color: #ff0000 !important;
                                text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000, 0 0 40px #ff0000 !important;
                                animation: health-pulse 1.5s infinite alternate !important;
                                font-weight: bold !important;
                            }
                            @keyframes health-pulse {
                                from { text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000; }
                                to { text-shadow: 0 0 20px #ff0000, 0 0 40px #ff0000, 0 0 60px #ff0000; }
                            }
                        `;
                        document.head.appendChild(styleEl);
                    }
                } else {
                    if (styleEl) styleEl.remove();
                }
            } catch (err) {
                // If API is down, we also consider it unhealthy
                console.error('[HEALTH] API Connection failed:', err);
            }
        }

        // Initial check and set interval
        checkHealth();
        setInterval(checkHealth, 30000); // Poll every 30s
    }

    initHealthMonitor();
})();
