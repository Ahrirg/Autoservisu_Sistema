// Small behaviours Carbon's CSS-only package leaves to the app.
(() => {
  // --- "Notimplemented" modal ----------------------------------------------
  const modal = document.getElementById("not-implemented-modal");
  let lastTrigger = null;

  const openModal = () => {
    modal.classList.add("is-visible");
    modal.querySelector("[data-modal-close]").focus();
  };
  const closeModal = () => {
    modal.classList.remove("is-visible");
    if (lastTrigger) lastTrigger.focus();
  };

  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-not-implemented]");
    if (trigger) {
      event.preventDefault();
      lastTrigger = trigger;
      openModal();
      return;
    }
    if (event.target.closest("[data-modal-close]") || event.target === modal) {
      closeModal();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && modal.classList.contains("is-visible")) closeModal();
  });

  // --- Side nav (small screens) ----------------------------------------------
  const toggle = document.querySelector("[data-side-nav-toggle]");
  const sideNav = document.querySelector("[data-side-nav]");
  if (toggle && sideNav) {
    toggle.addEventListener("click", () => {
      const expanded = sideNav.classList.toggle("cds--side-nav--expanded");
      toggle.setAttribute("aria-expanded", String(expanded));
      toggle.classList.toggle("cds--header__action--active", expanded);
    });
  }
})();
