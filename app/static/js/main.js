// app/static/js/main.js - (./app/static/js/main.js)
// Small Vue and theme-toggle behavior for the UI.

document.addEventListener("DOMContentLoaded", () => {
  // Vue root instance for future reactive dashboard widgets.
  const appElement = document.getElementById("app");
  if (appElement && window.Vue) {
    const { createApp } = Vue;
    createApp({
      data() {
        return {
          message: "MCP API Integration Hub",
        };
      },
    }).mount("#app");
  }

  // Simple light/dark theme toggle stored in localStorage.
  const themeToggle = document.getElementById("themeToggle");
  const rootHtml = document.documentElement;
  const storedTheme = localStorage.getItem("theme");

  if (storedTheme === "dark") {
    rootHtml.setAttribute("data-bs-theme", "dark");
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const current = rootHtml.getAttribute("data-bs-theme") || "light";
      const next = current === "light" ? "dark" : "light";
      rootHtml.setAttribute("data-bs-theme", next);
      localStorage.setItem("theme", next);
    });
  }
});
