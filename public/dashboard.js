document.addEventListener('DOMContentLoaded', () => {
  showTab('registered');
  loadEvents();

  document.getElementById('hostForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const data = {
      title: form.title.value,
      type: form.type.value,
      date: form.date.value,
      location: form.location.value
    };

    await fetch('/api/host', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    form.reset();
    loadEvents();
    showTab('registered');
  });
});

function showTab(tabId) {
  document.querySelectorAll('.tab').forEach(tab => {
    tab.style.display = tab.id === tabId ? 'block' : 'none';
  });
}

async function loadEvents() {
  const res = await fetch('/api/events');
  const { registered, explore } = await res.json();

  const regDiv = document.getElementById('registeredEvents');
  regDiv.innerHTML = registered.map(e => `<p>${e.title} (${e.date})</p>`).join('');

  const expDiv = document.getElementById('exploreEvents');
  expDiv.innerHTML = explore.map(e => `
    <div>
      <p>${e.title} (${e.date})</p>
      <button onclick="registerEvent('${e._id}')">Register</button>
    </div>
  `).join('');
}

async function registerEvent(eventId) {
  await fetch(`/api/register/${eventId}`, { method: 'POST' });
  loadEvents();
}
