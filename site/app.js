const state = { items: [], query: "", filter: "all" };

const grid = document.querySelector("#artifact-grid");
const template = document.querySelector("#artifact-template");
const search = document.querySelector("#search");
const resultCount = document.querySelector("#results-count");
const clearSearch = document.querySelector("#clear-search");
const emptyState = document.querySelector("#empty-state");

const kindLabels = {
  prototype: "Live prototype",
  document: "Document",
  image: "Image",
};

function filteredItems() {
  const terms = state.query.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
  return state.items.filter((item) => {
    const inCategory = state.filter === "all" || item.category === state.filter;
    const haystack = [item.title, item.collection, item.filename, item.category].join(" ").toLocaleLowerCase();
    return inCategory && terms.every((term) => haystack.includes(term));
  });
}

function render() {
  const items = filteredItems();
  grid.replaceChildren();

  for (const item of items) {
    const card = template.content.firstElementChild.cloneNode(true);
    const links = card.querySelectorAll("a");
    links.forEach((link) => { link.href = item.url; });
    card.querySelector("h2 a").textContent = item.title;
    card.querySelector(".kind").textContent = kindLabels[item.kind] || "Artifact";
    card.querySelector(".collection").textContent = item.collection;
    card.querySelector(".filename").textContent = item.filename;
    card.querySelector(".preview-placeholder span").textContent = item.kind === "document" ? "DOCX" : "ILMA";
    card.classList.toggle("document-card", item.kind === "document");
    card.querySelector(".open-link span").textContent = item.kind === "prototype" ? "Open preview" : "Open file";

    if (item.preview) {
      const preview = card.querySelector(".preview");
      const image = preview.querySelector("img");
      image.src = item.preview;
      image.alt = `Preview of ${item.title}`;
      image.addEventListener("load", () => preview.classList.add("has-image"));
    }
    grid.append(card);
  }

  grid.setAttribute("aria-busy", "false");
  resultCount.textContent = `${items.length} ${items.length === 1 ? "artifact" : "artifacts"}`;
  clearSearch.hidden = state.query.length === 0;
  emptyState.hidden = items.length !== 0;
}

function reset() {
  state.query = "";
  state.filter = "all";
  search.value = "";
  document.querySelectorAll(".filter").forEach((button) => {
    const active = button.dataset.filter === "all";
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  render();
}

search.addEventListener("input", (event) => {
  state.query = event.target.value;
  render();
});

document.querySelectorAll(".filter").forEach((button) => {
  button.addEventListener("click", () => {
    state.filter = button.dataset.filter;
    document.querySelectorAll(".filter").forEach((candidate) => {
      const active = candidate === button;
      candidate.classList.toggle("is-active", active);
      candidate.setAttribute("aria-pressed", String(active));
    });
    render();
  });
});

clearSearch.addEventListener("click", () => {
  state.query = "";
  search.value = "";
  search.focus();
  render();
});

emptyState.querySelector("button").addEventListener("click", reset);

fetch("catalog.json")
  .then((response) => {
    if (!response.ok) throw new Error(`Catalog request failed: ${response.status}`);
    return response.json();
  })
  .then((catalog) => {
    state.items = catalog.items;
    document.querySelector("#prototype-count").textContent = catalog.stats.prototypes;
    document.querySelector("#document-count").textContent = catalog.stats.documents;
    document.querySelector("#collection-count").textContent = catalog.stats.collections;
    render();
  })
  .catch(() => {
    grid.setAttribute("aria-busy", "false");
    resultCount.textContent = "The library could not be loaded. Refresh the page to try again.";
  });
