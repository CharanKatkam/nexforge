// Global UI behaviour: scroll-reveal, stat counters, sticky-nav state, back-to-top.
// Vanilla JS, no dependencies. Respects prefers-reduced-motion.
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.addEventListener("DOMContentLoaded", function () {
    document.body.classList.add("is-loaded");

    // --- Auto-tag reveal targets across every page (no template edits) -----
    // Cards, process steps, list-group rows, and accordion items animate in.
    var autoSel = "main section .card, main section .process-step," +
                  " main section .list-group-item, main section .accordion-item," +
                  " main section blockquote";
    document.querySelectorAll(autoSel).forEach(function (el) {
      if (!el.classList.contains("animate-on-scroll")) {
        el.classList.add("animate-on-scroll");
        // stagger by position within the parent row/list
        var sibs = Array.prototype.slice.call(el.parentNode.children);
        el.style.setProperty("--d", Math.min(sibs.indexOf(el), 6));
      }
    });
    // Animated underline accent on centered section headings.
    document.querySelectorAll("main section .text-center > h2").forEach(function (h) {
      h.classList.add("heading-accent");
    });

    // --- Scroll-reveal -----------------------------------------------------
    var revealEls = document.querySelectorAll(".animate-on-scroll, .heading-accent");
    if (reduce) {
      revealEls.forEach(function (el) { el.classList.add("visible"); });
    } else if ("IntersectionObserver" in window) {
      var revealObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            revealObs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
      revealEls.forEach(function (el) { revealObs.observe(el); });
    } else {
      revealEls.forEach(function (el) { el.classList.add("visible"); });
    }

    // --- Stat counters -----------------------------------------------------
    var counters = document.querySelectorAll(".count-up");
    function runCounter(el) {
      var target = parseFloat(el.dataset.target);
      if (isNaN(target)) return;
      var isFloat = target !== Math.floor(target);
      if (reduce) {
        el.textContent = (isFloat ? target.toFixed(1) : Math.floor(target)) + "+";
        return;
      }
      var current = 0, steps = 60, increment = target / steps;
      var timer = setInterval(function () {
        current += increment;
        if (current >= target) {
          el.textContent = (isFloat ? target.toFixed(1) : Math.floor(target)) + "+";
          clearInterval(timer);
        } else {
          el.textContent = isFloat ? current.toFixed(1) : Math.floor(current);
        }
      }, 25);
    }
    if ("IntersectionObserver" in window) {
      var countObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) { runCounter(entry.target); countObs.unobserve(entry.target); }
        });
      }, { threshold: 0.5 });
      counters.forEach(function (c) { countObs.observe(c); });
    } else {
      counters.forEach(runCounter);
    }

    // --- Sticky nav scrolled state ----------------------------------------
    var nav = document.querySelector(".navbar.sticky-top");
    if (nav) {
      var onScroll = function () {
        nav.classList.toggle("navbar-scrolled", window.scrollY > 12);
      };
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }

    // --- Back to top -------------------------------------------------------
    var toTop = document.querySelector(".back-to-top");
    if (toTop) {
      window.addEventListener("scroll", function () {
        toTop.classList.toggle("visible", window.scrollY > 600);
      }, { passive: true });
      toTop.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
      });
    }
  });
})();
