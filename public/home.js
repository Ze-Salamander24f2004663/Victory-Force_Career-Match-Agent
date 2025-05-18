// public/home.js
window.addEventListener('DOMContentLoaded', async () => {
  const res = await fetch('/api/all-events');
  const events = await res.json();

  const container = document.getElementById('eventList');
  if (events.length === 0) {
    container.innerHTML = '<p>No events available.</p>';
  } else {
    container.innerHTML = events.map(e => `
      <div class="event-card">
        <h3>${e.title}</h3>
        <p><strong>Type:</strong> ${e.type}</p>
        <p><strong>Date:</strong> ${e.date}</p>
        <p><strong>Location:</strong> ${e.location}</p>
        <p><strong>Host:</strong> ${e.host}</p>
      </div>
    `).join('');
  }
});
