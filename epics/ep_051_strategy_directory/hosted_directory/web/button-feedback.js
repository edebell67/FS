/* Shared button feedback · v1.0.0 · 2026-08-24 */
(function () {
  document.addEventListener("pointerdown", (event) => {
    const button = event.target.closest("button");
    if (!button || button.disabled) return;
    const box = button.getBoundingClientRect();
    button.style.setProperty("--press-x", `${event.clientX - box.left}px`);
    button.style.setProperty("--press-y", `${event.clientY - box.top}px`);
  });
  document.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button || button.disabled) return;
    button.classList.remove("button-activated");
    void button.offsetWidth;
    button.classList.add("button-activated");
  });
  document.addEventListener("animationend", (event) => {
    if (event.animationName === "button-confirm")
      event.target.classList.remove("button-activated");
  });
})();
