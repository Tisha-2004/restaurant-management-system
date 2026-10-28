/* Restaurant Management System - shared front-end behaviour */
(function () {
  "use strict";

  // --- Dark mode toggle (persisted in localStorage) ---
  const root = document.documentElement;
  const stored = localStorage.getItem("rms-theme");
  if (stored) root.setAttribute("data-bs-theme", stored);

  document.addEventListener("click", function (event) {
    const toggle = event.target.closest("#themeToggle");
    if (!toggle) return;
    const next = root.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-bs-theme", next);
    localStorage.setItem("rms-theme", next);
    const icon = toggle.querySelector("i");
    if (icon) icon.className = next === "dark" ? "fa-solid fa-sun" : "fa-solid fa-moon";
  });

  // --- Page loader ---
  window.addEventListener("load", function () {
    const loader = document.getElementById("pageLoader");
    if (loader) setTimeout(() => loader.classList.add("hidden"), 250);
  });

  // --- Reveal-on-scroll animation ---
  const revealables = document.querySelectorAll(".fade-up");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => entries.forEach((entry) => entry.isIntersecting && entry.target.classList.add("visible")),
      { threshold: 0.12 }
    );
    revealables.forEach((el) => observer.observe(el));
  } else {
    revealables.forEach((el) => el.classList.add("visible"));
  }

  // --- Back to top ---
  const backToTop = document.getElementById("backToTop");
  if (backToTop) {
    window.addEventListener("scroll", () => backToTop.classList.toggle("show", window.scrollY > 400));
    backToTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  }

  // --- Mobile sidebar (admin) ---
  const sidebarToggle = document.getElementById("sidebarToggle");
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", () =>
      document.getElementById("adminSidebar").classList.toggle("open")
    );
  }

  // --- Image preview before upload ---
  const imageInput = document.getElementById("imageInput");
  const imagePreview = document.getElementById("imagePreview");
  if (imageInput && imagePreview) {
    if (imagePreview.getAttribute("src")) imagePreview.classList.remove("d-none");
    imageInput.addEventListener("change", function () {
      const file = this.files && this.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        imagePreview.src = e.target.result;
        imagePreview.classList.remove("d-none");
      };
      reader.readAsDataURL(file);
    });
  }

  // --- Auto-dismiss alerts after 6s ---
  document.querySelectorAll(".alert-dismissible").forEach((alert) => {
    setTimeout(() => alert.querySelector(".btn-close")?.click(), 6000);
  });
})();
