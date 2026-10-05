/*
 * ep060-nav.js - shared EP060 side menu. One file, injected into every EP060 page so the menu stays
 * visible, in the same format, whichever page is open.
 *
 * v1.5.0 (2026-10-05): added Strategy Curves (8095, /strategy-curves.html) after Strategy Directory.
 * v1.4.1 (2026-10-03): Strategy Directory moved from 8094 to 8095.
 * v1.4.0 (2026-10-03): 'Forex Leaderboard' is now 'Leaderboard' with two sub items, Forex and Crypto (both on 8159).
 * v1.3.0 (2026-10-02): re-orderable menu (drag, or hover for up/down); order saved in a cookie shared across ports.
 * v1.2.0 (2026-10-02): added Trading Workflow (8061, first) and Forex Leaderboard (8159).
 * v1.1.0 (2026-10-02): added Cross Signal (8110).
 * v1.0.0 (2026-10-02): Initial version. CSP-safe (constructed stylesheet), local hosts only.
 *   Fixed left rail (top bar on narrow screens), pushes page content aside so it never overlaps,
 *   highlights the current page. Copies must stay identical: ep_060 (source), ep_051 hosted_directory/web,
 *   ep_052 lean_exchange/web, ep_057 dashboards_and_uis + cross_signal_prototype, TradeApps/breakout/DB, ep_061 (served via /ep060-nav.js route), ep_059 reports.
 *
 * Each page loads it from its OWN origin (the apps send script-src 'self').
 */
(function () {
  if (window.__ep060Nav) return;
  // Local dev menu only: never render on a public host (the Strategy Directory is also deployed publicly).
  if (!/^(localhost|127\.0\.0\.1|\[::1\]|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/.test(location.hostname)) return;
  window.__ep060Nav = true;

  var host = location.hostname || '127.0.0.1';
  var PAGES = [
    { key: 'workflow',    port: '8061', path: '/',                                     icon: '◎', label: 'Trading Workflow' },
    { key: 'arena',       port: '8056', path: '/arena',                                icon: '◈', label: 'Agentic Arena' },
    { key: 'equity',      port: '8765', path: '/top10_5min_equity_curves.html',        icon: '▥', label: 'Equity Curves' },
    { key: 'divergence',  port: '5051', path: '/ep060_divergence_monitor.html',        icon: '↔', label: 'Count Divergence' },
    { key: 'cross',       port: '8110', path: '/cross_signal.html',                    icon: '⨯', label: 'Cross Signal' },
    { key: 'forex',       port: '8159', path: '/forex/index.html',                     icon: '¤', label: 'Leaderboard',
      children: [
        { port: '8159', path: '/forex/index.html',  label: 'Forex' },
        { port: '8159', path: '/crypto/index.html', label: 'Crypto' }
      ] },
    { key: 'directory',   port: '8095', path: '/',                                     icon: '▦', label: 'Strategy Directory' },
    { key: 'curves',      port: '8095', path: '/strategy-curves.html',                 icon: '∿', label: 'Strategy Curves' }
  ];

  function isCurrent(p) {
    if (p.children) return p.children.some(isCurrent);
    if (location.port !== p.port) return false;
    return p.path === '/' ? location.pathname === '/' : location.pathname.indexOf(p.path) === 0;
  }

  var css = [
    ':root{--ep060-nav-w:200px}',
    '#ep060-nav{position:fixed;top:0;left:0;bottom:0;width:var(--ep060-nav-w);z-index:2147483000;box-sizing:border-box;',
    'background:#0d1117;border-right:1px solid #263241;padding:16px 0;display:flex;flex-direction:column;',
    'font:500 13px/1.2 system-ui,-apple-system,"Segoe UI",sans-serif;overflow-y:auto}',
    '#ep060-nav .t{padding:0 18px 14px;color:#8fa0ff;font-weight:700;letter-spacing:.14em;font-size:11px}',
    '#ep060-nav .it{position:relative;display:flex;align-items:stretch}',
    '#ep060-nav .it.drag{opacity:.4}',
    '#ep060-nav .it.over{box-shadow:inset 0 2px 0 #667eea}',
    '#ep060-nav a{flex:1;min-width:0;display:flex;align-items:center;gap:10px;padding:12px 18px;color:#b6c0cc;text-decoration:none;',
    'border-left:3px solid transparent}',
    '#ep060-nav .mv{display:none;flex-direction:column;justify-content:center;padding-right:6px}',
    '#ep060-nav .it:hover .mv,#ep060-nav .it:focus-within .mv{display:flex}',
    '#ep060-nav .mv button{background:none;border:0;color:#7d8aa3;cursor:pointer;font-size:9px;line-height:1;padding:2px 4px}',
    '#ep060-nav .mv button:hover{color:#fff}',
    '#ep060-nav .rs{margin:auto 18px 0;padding-top:10px;background:none;border:0;color:#5d6b82;font-size:10px;cursor:pointer;text-align:left}',
    '#ep060-nav .rs:hover{color:#b6c0cc}',
    '#ep060-nav a:hover{background:#161d27;color:#fff}',
    '#ep060-nav a.on{background:#1a2432;color:#fff;border-left-color:#667eea}',
    '#ep060-nav a i,#ep060-nav .g i{font-style:normal;width:18px;text-align:center;color:#9baef3}',
    '#ep060-nav .grp{flex:1;min-width:0;display:flex;flex-direction:column}',
    '#ep060-nav .g{display:flex;align-items:center;gap:10px;padding:12px 18px 6px;color:#b6c0cc;border-left:3px solid transparent}',
    '#ep060-nav .g.on{color:#fff;border-left-color:#667eea}',
    '#ep060-nav a.sub{flex:none;padding:7px 18px 7px 49px;font-size:12px}',
    'body.ep060-nav-on{margin-left:var(--ep060-nav-w)!important;padding-left:0!important}',
    '@media (max-width:800px){',
    ' #ep060-nav{position:sticky;top:0;bottom:auto;width:auto;flex-direction:row;flex-wrap:wrap;padding:6px 0;',
    ' border-right:0;border-bottom:1px solid #263241}',
    ' #ep060-nav .t{display:none}',
    ' #ep060-nav .it{flex:1 1 50%}',
    ' #ep060-nav .mv,#ep060-nav .rs{display:none!important}',
    ' #ep060-nav a{flex:1 1 auto;padding:10px 12px;border-left:0;border-bottom:3px solid transparent}',
    ' #ep060-nav a.on{border-bottom-color:#667eea}',
    ' body.ep060-nav-on{margin-left:0!important}}'
  ].join('');

  function build() {
    var old = document.getElementById('ep060-nav');
    if (old) old.remove();
    // Constructed stylesheet: works under strict CSPs (style-src 'self') where an injected <style> is blocked.
    try {
      var sheet = new CSSStyleSheet();
      sheet.replaceSync(css);
      document.adoptedStyleSheets = document.adoptedStyleSheets.concat([sheet]);
    } catch (e) {
      var style = document.createElement('style');
      style.textContent = css;
      document.head.appendChild(style);
    }

    var nav = document.createElement('nav');
    nav.id = 'ep060-nav';
    nav.setAttribute('aria-label', 'EP060 pages');
    nav.innerHTML = '<div class="t">EP060 LINKS</div><div class="list"></div><button type="button" class="rs" title="Restore the default menu order">reset order</button>';
    var list = nav.querySelector('.list');

    // Order is kept in a cookie: cookies are shared across ports on the same host, so every EP060
    // page (each on its own port/origin) shows the same order. localStorage would not be shared.
    var COOKIE = 'ep060_nav_order';
    function loadOrder() {
      var m = document.cookie.match(new RegExp('(?:^|; )' + COOKIE + '=([^;]*)'));
      return m ? decodeURIComponent(m[1]).split(',') : [];
    }
    function saveOrder(keys) {
      document.cookie = COOKIE + '=' + encodeURIComponent(keys.join(',')) + '; path=/; max-age=31536000; SameSite=Lax';
    }
    function ordered() {
      var saved = loadOrder(), out = [];
      saved.forEach(function (k) { PAGES.forEach(function (p) { if (p.key === k && out.indexOf(p) < 0) out.push(p); }); });
      PAGES.forEach(function (p) { if (out.indexOf(p) < 0) out.push(p); }); // new pages go last
      return out;
    }
    function currentKeys() { return [].map.call(list.children, function (el) { return el.getAttribute('data-key'); }); }
    function move(el, dir) {
      var sib = dir < 0 ? el.previousElementSibling : el.nextElementSibling;
      if (!sib) return;
      list.insertBefore(el, dir < 0 ? sib : sib.nextSibling);
      saveOrder(currentKeys());
      var b = el.querySelector(dir < 0 ? '.up' : '.dn'); if (b) b.focus();
    }
    var dragEl = null;
    function item(p) {
      var el = document.createElement('div');
      el.className = 'it'; el.setAttribute('data-key', p.key); el.draggable = true;
      var on = isCurrent(p);
      var link = function (q, cls) {
        var qon = isCurrent(q);
        return '<a href="' + location.protocol + '//' + host + ':' + q.port + q.path + '"' + (cls ? ' class="' + cls + (qon ? ' on' : '') + '"' : (qon ? ' class="on"' : '')) +
          (qon ? ' aria-current="page"' : '') + '>' + (cls ? '' : '<i aria-hidden="true">' + q.icon + '</i>') + '<span>' + q.label + '</span></a>';
      };
      var body = p.children
        ? '<div class="grp"><div class="g' + (on ? ' on' : '') + '"><i aria-hidden="true">' + p.icon + '</i><span>' + p.label + '</span></div>' +
          p.children.map(function (c) { return link(c, 'sub'); }).join('') + '</div>'
        : link(p);
      el.innerHTML = body +
        '<span class="mv"><button type="button" class="up" aria-label="Move ' + p.label + ' up">▲</button>' +
        '<button type="button" class="dn" aria-label="Move ' + p.label + ' down">▼</button></span>';
      el.querySelector('.up').addEventListener('click', function () { move(el, -1); });
      el.querySelector('.dn').addEventListener('click', function () { move(el, 1); });
      el.addEventListener('dragstart', function (e) { dragEl = el; el.classList.add('drag'); e.dataTransfer.effectAllowed = 'move'; try { e.dataTransfer.setData('text/plain', p.key); } catch (x) {} });
      el.addEventListener('dragend', function () { el.classList.remove('drag'); [].forEach.call(list.children, function (c) { c.classList.remove('over'); }); dragEl = null; });
      el.addEventListener('dragover', function (e) { if (dragEl && dragEl !== el) { e.preventDefault(); el.classList.add('over'); } });
      el.addEventListener('dragleave', function () { el.classList.remove('over'); });
      el.addEventListener('drop', function (e) {
        e.preventDefault(); el.classList.remove('over');
        if (!dragEl || dragEl === el) return;
        list.insertBefore(dragEl, el); saveOrder(currentKeys());
      });
      return el;
    }
    function fill(pages) { list.textContent = ''; pages.forEach(function (p) { list.appendChild(item(p)); }); }
    fill(ordered());
    nav.querySelector('.rs').addEventListener('click', function () {
      document.cookie = COOKIE + '=; path=/; max-age=0; SameSite=Lax';
      fill(PAGES);
    });
    document.body.insertBefore(nav, document.body.firstChild);
    document.body.classList.add('ep060-nav-on');
  }

  if (document.body) build(); else document.addEventListener('DOMContentLoaded', build);
})();
