(() => {
  const buttons = document.querySelectorAll('[data-gallery-style]');
  const title = document.getElementById('showroom-title');
  const copy = document.getElementById('showroom-copy');
  const action = document.getElementById('showroom-action');
  if (!buttons.length || !title || !copy || !action) return;
  let explored = [];
  buttons.forEach((button) => button.addEventListener('click', () => {
    const style = button.dataset.galleryStyle;
    if (!explored.includes(style)) explored.push(style);
    buttons.forEach((item) => item.classList.toggle('is-selected', item === button));
    title.textContent = `You explored ${style}.`;
    copy.textContent = `Example controlled response: “You seem drawn to ${style}. In an owner-approved launch, I could show more inspiration in that direction and offer a design-consultation enquiry route.”`;
    action.disabled = false;
    action.textContent = 'Preview consultation prompt';
  }));
  action.addEventListener('click', () => {
    if (action.disabled) return;
    title.textContent = 'Consultation prompt — demonstration only';
    copy.textContent = 'A real owner-approved version could ask for the room type, location, preferred style and best contact method, then pass only a consented enquiry to the chosen business workflow. No enquiry is collected or sent by this preview.';
    action.textContent = 'No live enquiry is sent';
    action.disabled = true;
  });
})();
