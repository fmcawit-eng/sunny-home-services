/* Offers marquee - continuous horizontal scroll.
   Each .marquee-track holds its content twice, so travelling half the scroll
   width loops seamlessly. data-duration sets the pace in seconds.
   This is the same function the full site uses, narrowed to this section. */
(function () {
  function initMarquee() {
    document.querySelectorAll(".marquee-track").forEach(function (track) {
      var trackWidth = track.scrollWidth;
      if (!trackWidth || typeof gsap === "undefined") return;
      gsap.to(track, {
        x: -trackWidth / 2,
        duration: parseFloat(track.dataset.duration) || 28,
        ease: "none",
        repeat: -1
      });
    });
  }
  if (document.readyState !== "loading") initMarquee();
  else document.addEventListener("DOMContentLoaded", initMarquee);
})();
