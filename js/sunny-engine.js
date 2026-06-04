// Sunny Home Services — V2 prototype engine
// Lenis smooth scroll + GSAP ScrollTrigger
// Mirrors V2 Figma: interactive hero title, section reveals, trust marquee,
// counter animations, interactive booking tiles. No canvas scrubbing.

gsap.registerPlugin(ScrollTrigger);

/* ============================================================
   LENIS SMOOTH SCROLL
============================================================ */
const lenis = new Lenis({
  duration: 1.15,
  easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true,
});
lenis.on("scroll", ScrollTrigger.update);
gsap.ticker.add(t => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);

/* ============================================================
   HERO TITLE — interactive (hover, click, mouse parallax)
============================================================ */
function initInteractiveHero() {
  const title = document.getElementById("hero-title");
  if (!title) return;
  const words = title.querySelectorAll(".word");

  // Staggered entrance
  gsap.set(words, { y: 60, opacity: 0, rotationX: -40 });
  gsap.to(words, {
    y: 0, opacity: 1, rotationX: 0,
    stagger: 0.08, duration: 0.9, ease: "power3.out",
    delay: 0.2,
  });

  // Click → "pop" animation
  words.forEach(w => {
    w.addEventListener("click", () => {
      w.classList.remove("is-clicked");
      void w.offsetWidth; // reflow to restart animation
      w.classList.add("is-clicked");
      setTimeout(() => w.classList.remove("is-clicked"), 600);
    });
  });

  // Subtle mouse parallax — title shifts opposite cursor with damped lerp
  const hero = document.querySelector(".section-hero");
  if (!hero) return;
  let rafId = null;
  let targetTx = 0, targetTy = 0;
  let curTx = 0, curTy = 0;

  function tick() {
    curTx += (targetTx - curTx) * 0.08;
    curTy += (targetTy - curTy) * 0.08;
    title.style.transform = `translate3d(${curTx}px, ${curTy}px, 0)`;
    if (Math.abs(targetTx - curTx) > 0.05 || Math.abs(targetTy - curTy) > 0.05) {
      rafId = requestAnimationFrame(tick);
    } else {
      rafId = null;
    }
  }

  hero.addEventListener("mousemove", (e) => {
    const rect = hero.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = (e.clientX - cx) / rect.width;
    const dy = (e.clientY - cy) / rect.height;
    targetTx = -dx * 18;
    targetTy = -dy * 12;
    if (!rafId) rafId = requestAnimationFrame(tick);
  });
  hero.addEventListener("mouseleave", () => {
    targetTx = 0; targetTy = 0;
    if (!rafId) rafId = requestAnimationFrame(tick);
  });
}

/* ============================================================
   SECTION REVEALS — each .reveal section animates as one unit
============================================================ */
function initSectionReveals() {
  document.querySelectorAll(".reveal").forEach(el => {
    const type = el.dataset.animation || "fade-up";
    let from = {};
    switch (type) {
      case "slide-left":  from = { x: -60, opacity: 0 }; break;
      case "slide-right": from = { x:  60, opacity: 0 }; break;
      case "scale-up":    from = { scale: 0.95, opacity: 0 }; break;
      case "fade-up":
      default:            from = { y: 36, opacity: 0 }; break;
    }
    gsap.set(el, from);
    ScrollTrigger.create({
      trigger: el,
      start: "top 82%",
      once: true,
      onEnter: () => {
        gsap.to(el, {
          x: 0, y: 0, scale: 1, opacity: 1,
          duration: 0.95,
          ease: "power3.out",
        });
      },
    });
  });
}

/* ============================================================
   TRUST MARQUEE — continuous horizontal scroll
============================================================ */
function initMarquee() {
  const track = document.getElementById("marquee-track");
  if (!track) return;
  const trackWidth = track.scrollWidth;
  gsap.to(track, {
    x: -trackWidth / 2,
    duration: 28,
    ease: "none",
    repeat: -1,
  });
}

/* ============================================================
   COUNTERS — numeric stats count up when in view
============================================================ */
function initCounters() {
  document.querySelectorAll("[data-value]").forEach(el => {
    const raw = el.dataset.value;
    const targetN = parseFloat(raw);
    if (Number.isNaN(targetN)) return;
    const decimals = parseInt(el.dataset.decimals || "0", 10);
    const prefix = el.dataset.prefix || "";
    const suffix = el.dataset.suffix || "";
    const formatter = (n) => prefix +
      (decimals === 0 ? Math.round(n).toLocaleString() : n.toFixed(decimals)) +
      suffix;
    el.textContent = formatter(0);
    const obj = { val: 0 };
    ScrollTrigger.create({
      trigger: el,
      start: "top 88%",
      once: true,
      onEnter: () => {
        gsap.to(obj, {
          val: targetN,
          duration: 1.6,
          ease: "power2.out",
          onUpdate: () => { el.textContent = formatter(obj.val); },
        });
      },
    });
  });
}

/* ============================================================
   INTERACTIVE BOOKING TILES — click to "select" a service
============================================================ */
function initBookingTiles() {
  const tiles = document.querySelectorAll("#booking-options .opt");
  if (!tiles.length) return;
  tiles.forEach(t => {
    t.addEventListener("click", () => {
      tiles.forEach(x => x.classList.remove("is-active"));
      t.classList.add("is-active");
    });
  });
  // Default: nothing selected (user picks)
}

/* ============================================================
   BOOT
============================================================ */
function boot() {
  initInteractiveHero();
  initSectionReveals();
  initMarquee();
  initCounters();
  initBookingTiles();
  setTimeout(() => ScrollTrigger.refresh(), 120);
}
boot();
