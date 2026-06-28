/* Color-theme control: cycles Auto → Light → Dark → Auto, persisted in
   localStorage. "Auto" follows the OS via the CSS prefers-color-scheme query
   (no attribute set); Light/Dark set data-theme on <html> to override.
   Loaded synchronously in <head> so the saved theme applies before first paint. */
(function () {
  var KEY = "ai-journey-theme";
  var ORDER = ["auto", "light", "dark"];
  var ICON = { auto: "◐", light: "☀", dark: "☾" }; /* ◐ ☀ ☾ */
  var LABEL = { auto: "Auto", light: "Light", dark: "Dark" };

  function getMode() {
    var v = null;
    try { v = localStorage.getItem(KEY); } catch (e) {}
    return ORDER.indexOf(v) >= 0 ? v : "auto";
  }

  function apply(mode) {
    var root = document.documentElement;
    if (mode === "auto") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", mode);
  }

  /* run immediately to avoid a flash of the wrong theme */
  apply(getMode());

  function wire() {
    var mode = getMode();
    var buttons = document.querySelectorAll(".theme-toggle");

    function render() {
      for (var i = 0; i < buttons.length; i++) {
        var b = buttons[i];
        b.hidden = false;
        var icon = b.querySelector(".theme-icon");
        var label = b.querySelector(".theme-label");
        if (icon) icon.textContent = ICON[mode];
        if (label) label.textContent = LABEL[mode];
        var hint = "Color theme: " + LABEL[mode] + " (click to change)";
        b.setAttribute("aria-label", hint);
        b.setAttribute("title", hint);
      }
    }

    function cycle() {
      mode = ORDER[(ORDER.indexOf(mode) + 1) % ORDER.length];
      try { localStorage.setItem(KEY, mode); } catch (e) {}
      apply(mode);
      render();
    }

    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener("click", cycle);
    }
    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
