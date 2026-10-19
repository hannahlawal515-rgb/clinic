const dialog = document.querySelector("#patient-dialog");
const searchInput = document.querySelector("#queue-search");
const queueRows = [...document.querySelectorAll(".queue-row")];
const noResults = document.querySelector("#no-results");
const searchFeedback = document.querySelector("#search-feedback");

document.querySelectorAll("[data-open-dialog]").forEach((button) => {
  button.addEventListener("click", () => {
    dialog.showModal();
    dialog.querySelector("#id_name").focus();
  });
});

document.querySelectorAll("[data-close-dialog]").forEach((button) => {
  button.addEventListener("click", () => dialog.close());
});

dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});

searchInput?.addEventListener("input", () => {
  const query = searchInput.value.trim().toLocaleLowerCase();
  let visibleCount = 0;

  queueRows.forEach((row) => {
    const matches = row.dataset.search.includes(query);
    row.hidden = !matches;
    if (matches) visibleCount += 1;
  });

  if (noResults) noResults.hidden = visibleCount > 0 || queueRows.length === 0;
  if (searchFeedback) {
    searchFeedback.textContent = query
      ? `${visibleCount} patient${visibleCount === 1 ? "" : "s"} found.`
      : "Search cleared.";
  }
});

const sidebar = document.querySelector("#sidebar");
const menuToggle = document.querySelector(".menu-toggle");
const sidebarBackdrop = document.querySelector(".sidebar-backdrop");
const mobileNavigation = window.matchMedia("(max-width: 600px)");

function closeMobileNavigation() {
  sidebar.classList.remove("is-open");
  menuToggle.setAttribute("aria-expanded", "false");
  menuToggle.setAttribute("aria-label", "Open navigation");
  sidebarBackdrop.hidden = true;
}

menuToggle?.addEventListener("click", () => {
  const isOpen = sidebar.classList.toggle("is-open");
  menuToggle.setAttribute("aria-expanded", String(isOpen));
  menuToggle.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
  sidebarBackdrop.hidden = !isOpen;
});

sidebarBackdrop?.addEventListener("click", closeMobileNavigation);
sidebar.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    if (mobileNavigation.matches) closeMobileNavigation();
  });
});

mobileNavigation.addEventListener("change", (event) => {
  if (!event.matches) closeMobileNavigation();
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && sidebar.classList.contains("is-open")) {
    closeMobileNavigation();
  }

  if (event.key === "/" && !["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName)) {
    event.preventDefault();
    searchInput?.focus();
  }
});

document.querySelectorAll(".arrival-time").forEach((time) => {
  const date = new Date(time.dateTime);
  if (!Number.isNaN(date.valueOf())) {
    time.textContent = new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit" }).format(date);
  }
});