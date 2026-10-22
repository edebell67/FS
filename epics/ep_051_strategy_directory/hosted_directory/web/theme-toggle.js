/* Theme control · v1.0.0 · 2026-08-25 */
(function () {
  const key = "dna-directory-theme";
  let saved = "light";
  try { saved = localStorage.getItem(key) === "dark" ? "dark" : "light"; } catch (_) {}
  document.documentElement.dataset.theme = saved;
  document.documentElement.style.colorScheme = saved;

  function mount() {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "theme-toggle";
    button.setAttribute("aria-label", "Switch colour theme");
    const render = () => {
      const dark = document.documentElement.dataset.theme === "dark";
      button.setAttribute("aria-pressed", String(dark));
      button.innerHTML = `<span aria-hidden="true">${dark ? "☀" : "◐"}</span><span>${dark ? "Light mode" : "Dark mode"}</span>`;
    };
    button.addEventListener("click", () => {
      const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      document.documentElement.style.colorScheme = next;
      try { localStorage.setItem(key, next); } catch (_) {}
      render();
    });
    render();
    document.body.appendChild(button);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();
