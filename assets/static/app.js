
// ---- Toast ----
function showToast(message){
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.querySelector("[data-toast-text]").textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => toast.classList.remove("show"), 2200);
}

// ---- Mobile nav ----
function initMobileNav(){
  const btn = document.getElementById("nav-toggle");
  const menu = document.getElementById("mobile-menu");
  if (!btn || !menu) return;
  btn.addEventListener("click", () => {
    const open = menu.classList.toggle("hidden") === false;
    btn.setAttribute("aria-expanded", String(open));
  });
}

// ---- Hero slider (index page only) ----
function initHeroSlider(){
  const track = document.getElementById("hero-track");
  const dots = document.querySelectorAll(".hero-dot");
  const prev = document.getElementById("hero-prev");
  const next = document.getElementById("hero-next");
  if (!track || !dots.length) return;

  const slideCount = track.children.length;
  let index = 0;
  let timer = null;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function render(){
    track.style.transform = `translateX(-${index * 100}%)`;
    dots.forEach((d, i) => {
      if (i === index) d.setAttribute("data-active", "true");
      else d.removeAttribute("data-active");
    });
  }
  function goTo(i){ index = (i + slideCount) % slideCount; render(); }
  function startAutoplay(){
    if (reduceMotion) return;
    stopAutoplay();
    timer = setInterval(() => goTo(index + 1), 5000);
  }
  function stopAutoplay(){ if (timer) clearInterval(timer); }

  prev.addEventListener("click", () => { goTo(index - 1); startAutoplay(); });
  next.addEventListener("click", () => { goTo(index + 1); startAutoplay(); });
  dots.forEach((d, i) => d.addEventListener("click", () => { goTo(i); startAutoplay(); }));

  const wrap = document.getElementById("hero-slider");
  wrap.addEventListener("mouseenter", stopAutoplay);
  wrap.addEventListener("mouseleave", startAutoplay);

  render();
  startAutoplay();
}

document.addEventListener("DOMContentLoaded", () => {
  initMobileNav();
  initHeroSlider();
});
