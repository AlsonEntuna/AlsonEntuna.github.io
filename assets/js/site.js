// Site behaviour: theme toggle, mobile menu, scroll reveal, gallery lightbox.
(function () {
  const root = document.documentElement;
  root.classList.add("js");

  // Theme toggle — remembers the choice; falls back to the system theme.
  const toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const current = root.dataset.theme ||
        (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      const next = current === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  // Mobile menu
  const menuBtn = document.querySelector(".menu-toggle");
  const nav = document.getElementById("site-nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
  }

  // Reveal sections as they scroll into view
  const items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("is-visible"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach((el) => io.observe(el));
  } else {
    items.forEach((el) => el.classList.add("is-visible"));
  }

  // Gallery lightbox (uses the full-size image in data-full)
  const box = document.querySelector(".lightbox");
  const thumbs = [...document.querySelectorAll(".gallery button[data-full]")];
  if (box && thumbs.length) {
    const img = box.querySelector("img");
    const cap = box.querySelector(".lightbox__caption");
    let index = 0;
    const show = (i) => {
      index = (i + thumbs.length) % thumbs.length;
      const t = thumbs[index];
      img.src = t.dataset.full;
      img.alt = t.querySelector("img").alt;
      cap.innerHTML = t.dataset.caption || "";
    };
    thumbs.forEach((t, i) => t.addEventListener("click", () => { show(i); box.showModal(); }));
    box.querySelector(".lightbox__prev").addEventListener("click", () => show(index - 1));
    box.querySelector(".lightbox__next").addEventListener("click", () => show(index + 1));
    box.querySelector(".lightbox__close").addEventListener("click", () => box.close());
    box.addEventListener("click", (e) => { if (e.target === box) box.close(); });
    box.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") show(index - 1);
      if (e.key === "ArrowRight") show(index + 1);
    });
  }

  // Footer year
  document.querySelectorAll("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });
})();
