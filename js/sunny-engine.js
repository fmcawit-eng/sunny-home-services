// Sunny Home Services - V2 prototype engine
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
   TYPEWRITER - types a hero title in, character by character
============================================================ */
function typeInTitle(title, startDelay) {
  startDelay = startDelay || 0;
  const allWords = [...title.querySelectorAll(".word")];
  if (!allWords.length) return;
  // If some words are flagged .alt-font, type only those - the rest are handled elsewhere.
  const altWords = allWords.filter(w => w.classList.contains("alt-font"));
  const typeWords = altWords.length ? altWords : allWords;
  // Split into hidden chars immediately so the typed words stay invisible until typing begins.
  const chars = [];
  typeWords.forEach(w => {
    const text = w.textContent;
    w.textContent = "";
    [...text].forEach(ch => {
      const s = document.createElement("span");
      s.className = "char";
      s.textContent = ch;
      s.style.display = "none";
      w.appendChild(s);
      chars.push(s);
    });
  });
  const caret = document.createElement("span");
  caret.className = "type-caret";
  caret.style.display = "none";
  const first = typeWords[0];
  first.insertBefore(caret, first.firstChild);
  let i = 0;
  function step() {
    if (i < chars.length) {
      const c = chars[i++];
      c.style.display = "inline";
      c.after(caret);
      setTimeout(step, /[ ,?.!]/.test(c.textContent) ? 90 : 58);
    } else {
      setTimeout(() => caret.remove(), 2000);
    }
  }
  setTimeout(() => { caret.style.display = ""; step(); }, startDelay);
}

/* ============================================================
   HERO TITLE - typewriter entrance + interactive (hover, click, parallax)
============================================================ */
function initInteractiveHero() {
  const title = document.getElementById("hero-title");
  if (!title) return;
  const words = [...title.querySelectorAll(".word")];

  // If a line is flagged .alt-font, fade the rest of the title in first, then type the flagged line.
  const altWords = words.filter(w => w.classList.contains("alt-font"));
  const fadeWords = words.filter(w => !w.classList.contains("alt-font"));
  if (altWords.length && fadeWords.length) {
    gsap.set(fadeWords, { opacity: 0, y: 20 });
    gsap.to(fadeWords, { opacity: 1, y: 0, duration: 0.7, stagger: 0.08, ease: "power3.out", delay: 0.2 });
    typeInTitle(title, 1100); // hides the typed line now, starts typing after the fade
  } else {
    typeInTitle(title, 280);
  }

  // Supporting hero copy fades up after the headline sequence
  const heroSection = title.closest(".section-hero");
  if (heroSection) {
    const support = heroSection.querySelectorAll(".hero-sub, .lead-on-video, .cta-row");
    gsap.set(support, { y: 16, opacity: 0 });
    gsap.to(support, { y: 0, opacity: 1, duration: 0.7, stagger: 0.12, ease: "power3.out", delay: 1.4 });
  }

  // Click → "pop" animation
  words.forEach(w => {
    w.addEventListener("click", () => {
      w.classList.remove("is-clicked");
      void w.offsetWidth; // reflow to restart animation
      w.classList.add("is-clicked");
      setTimeout(() => w.classList.remove("is-clicked"), 600);
    });
  });

  // Subtle mouse parallax - title shifts opposite cursor with damped lerp
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
   SECTION REVEALS - each .reveal section animates as one unit
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
   PARALLAX - elements with [data-parallax] drift on scroll
============================================================ */
function initParallax() {
  if (typeof ScrollTrigger === "undefined") return;
  document.querySelectorAll("[data-parallax]").forEach(el => {
    const amt = parseFloat(el.dataset.parallax) || 10;
    const container = el.parentElement || el;
    gsap.fromTo(el,
      { yPercent: -amt },
      {
        yPercent: amt, ease: "none",
        scrollTrigger: { trigger: container, start: "top bottom", end: "bottom top", scrub: true },
      }
    );
  });
}

/* ============================================================
   FAMILY PLAN TILES - staggered slide-in on scroll
============================================================ */
function initFamilyPlanTiles() {
  if (typeof ScrollTrigger === "undefined") return;
  document.querySelectorAll(".fp-right").forEach(group => {
    const items = group.querySelectorAll(".fp-benefit");
    if (!items.length) return;
    gsap.set(items, { x: 50, opacity: 0 });
    ScrollTrigger.create({
      trigger: group, start: "top 82%", once: true,
      onEnter: () => gsap.to(items, { x: 0, opacity: 1, duration: 0.6, stagger: 0.15, ease: "power3.out" }),
    });
  });
}

/* ============================================================
   TRUST MARQUEE - continuous horizontal scroll
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
   COUNTERS - numeric stats count up when in view
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
   INTERACTIVE BOOKING TILES - click to "select" a service
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
   HEADER - entrance animation (items reveal in sequence)
============================================================ */
function initHeaderEntrance() {
  const header = document.querySelector(".site-header");
  if (!header) return;
  gsap.set(header, { y: -22, opacity: 0 });
  gsap.to(header, { y: 0, opacity: 1, duration: 0.6, ease: "power3.out" });
  const items = header.querySelectorAll(".header-logo, .header-nav a, .header-phone, .header-cta .btn");
  gsap.set(items, { y: -10, opacity: 0 });
  gsap.to(items, { y: 0, opacity: 1, duration: 0.5, stagger: 0.06, ease: "power2.out", delay: 0.12 });
}

/* ============================================================
   MOBILE NAV - hamburger + slide-in menu, built from the existing header nav
   so no per-page HTML changes are needed.
============================================================ */
function initMobileNav() {
  const header = document.querySelector(".site-header");
  const nav = header && header.querySelector(".header-nav");
  if (!header || !nav || document.querySelector(".nav-toggle")) return;

  const btn = document.createElement("button");
  btn.className = "nav-toggle";
  btn.setAttribute("aria-label", "Open menu");
  btn.setAttribute("aria-expanded", "false");
  btn.innerHTML = "<span></span><span></span><span></span>";
  header.appendChild(btn);

  const panel = document.createElement("div");
  panel.className = "mobile-menu";
  let html = '<div class="mm-top">' +
    '<a class="mm-phone" href="tel:+13858538116">385.853.8116</a>' +
    '<a class="btn btn-primary btn-pill mm-book" href="coming-soon.html">Book Now</a>' +
    '</div><nav class="mm-nav">';
  nav.querySelectorAll(".nav-item").forEach(item => {
    const top = item.querySelector(":scope > a");
    const menu = item.querySelector(".nav-menu");
    if (!top) return;
    if (menu) {
      html += '<div class="mm-group"><button class="mm-parent" type="button">' + top.textContent.trim() + "</button><div class=\"mm-sub\">";
      html += '<a href="' + top.getAttribute("href") + '">All ' + top.textContent.trim() + "</a>";
      menu.querySelectorAll("a").forEach(a => {
        html += '<a href="' + a.getAttribute("href") + '">' + a.textContent.trim() + "</a>";
      });
      html += "</div></div>";
    } else {
      html += '<a class="mm-link" href="' + top.getAttribute("href") + '">' + top.textContent.trim() + "</a>";
    }
  });
  html += "</nav>";
  panel.innerHTML = html;
  document.body.appendChild(panel);

  const setOpen = (o) => {
    document.body.classList.toggle("mm-open", o);
    btn.setAttribute("aria-expanded", o ? "true" : "false");
    btn.setAttribute("aria-label", o ? "Close menu" : "Open menu");
  };
  btn.addEventListener("click", () => setOpen(!document.body.classList.contains("mm-open")));
  panel.addEventListener("click", (e) => { if (e.target.closest("a")) setOpen(false); });
  panel.querySelectorAll(".mm-parent").forEach(p => {
    p.addEventListener("click", () => p.parentElement.classList.toggle("open"));
  });
}

/* ============================================================
   BOOT
============================================================ */
function boot() {
  initMobileNav();
  // ?noanim renders every section in its final/visible state (for screenshots/QA)
  if (/[?&]noanim/.test(location.search)) { initMarquee(); return; }
  initHeaderEntrance();
  initInteractiveHero();
  initSectionReveals();
  initParallax();
  initFamilyPlanTiles();
  initMarquee();
  initCounters();
  initBookingTiles();
  setTimeout(() => ScrollTrigger.refresh(), 120);
}
boot();
