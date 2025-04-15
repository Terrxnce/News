async function fetchAlerts() {
  const alertsContainer = document.getElementById("alerts");
  alertsContainer.innerHTML = "<p>Loading...</p>";

  try {
    const res = await fetch("/alerts");
    const data = await res.json();

    alertsContainer.innerHTML = "";

    if (data.length === 0) {
      alertsContainer.innerHTML = "<p>No breaking alerts right now.</p>";
      return;
    }

    data.forEach(alert => {
      const div = document.createElement("div");
      div.className = "alert";
      div.innerHTML = `
        <strong>${alert.timestamp}</strong> — <b>${alert.source}</b><br>
        <a href="${alert.link}" target="_blank">${alert.news}</a>
      `;
      alertsContainer.appendChild(div);
    });

  } catch (err) {
    alertsContainer.innerHTML = "<p>Error fetching alerts.</p>";
    console.error(err);
  }
}

// Auto-refresh every 30s
setInterval(fetchAlerts, 30000);
window.onload = fetchAlerts;
