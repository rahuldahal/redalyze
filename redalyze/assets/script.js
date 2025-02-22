// Ensure the script runs after Dash fully loads
document.addEventListener('DOMContentLoaded', () => {
  console.log("AI Interpretation script loaded.");

  // Function to send data to Flask API
  function sendDataToFlask(dataProperty, plotData) {
    console.log(`Sending ${dataProperty} for AI interpretation:`, plotData);
    fetch('/api/interpret', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        data_property: dataProperty,
        data: plotData
      })
    })
    .then(response => response.json())
    .then(result => console.log('AI Interpretation Response:', result))
    .catch(err => console.error('Error sending data:', err));
  }

  // Helper: Wait for dcc.Store to load
  function waitForStore(dataProperty, callback) {
    const interval = setInterval(() => {
      const storeElement = document.querySelector(`#store-${dataProperty}`);
      if (storeElement) {
        clearInterval(interval);
        callback(storeElement);
      }
    }, 100);
  }

  // Delegate event listener for all "Interpret with AI" buttons
  document.body.addEventListener('click', (event) => {
    if (event.target.classList.contains('interepet-trigger')) {
      const dataProperty = event.target.getAttribute('data-property');
      
      waitForStore(dataProperty, (storeElement) => {
        const plotData = JSON.parse(storeElement.dataset.store);
        sendDataToFlask(dataProperty, plotData);
      });
    }
  });
});
