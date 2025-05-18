// Wait until the page is fully loaded
window.addEventListener('DOMContentLoaded', () => {
  const searchBox = document.getElementById("searchBox");
  const cards = document.querySelectorAll(".event-card");

  searchBox.addEventListener("input", () => {
    const query = searchBox.value.toLowerCase();

    cards.forEach(card => {
      const text = card.innerText.toLowerCase();
      if (text.includes(query)) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  });
});
