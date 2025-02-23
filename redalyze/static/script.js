document.addEventListener('DOMContentLoaded', () => {
  console.log("AI Interpretation script running...");

  // Cache object to store API responses
  const cache = {};

  document.body.addEventListener('click', async (event) => {
    if (event.target.classList.contains('interepet-trigger')) {
      const dataProperty = event.target.getAttribute('id');

      console.log("Sending data for AI interpretation:", dataProperty);

      // If cached data exists, use it directly
      if (cache[dataProperty]) {
        console.log("Using cached data for:", dataProperty);
        renderMarkdown(cache[dataProperty], dataProperty);
        return;
      }

      // Otherwise, proceed with API request
      document.getElementById(`loading_${dataProperty}`).style.display = "block";
      document.getElementById(`markdown_${dataProperty}`).style.display = "none";

      try {
        const response = await fetch('/api/interpret', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            plot_type: dataProperty
          }),
        });

        const result = await response.json();
        console.log('AI Interpretation Response:', result);

        // Cache the result for future use
        cache[dataProperty] = result.message;

        await loadExternalResources();
        renderMarkdown(result.message, dataProperty);

      } catch (err) {
        console.error('Error sending data:', err);
      }
    }
  });
});

async function loadExternalResources() {
  await loadScript('https://cdn.jsdelivr.net/npm/marked/marked.min.js');
  console.log('marked.js loaded');
  await loadCss('https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css');
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.onload = () => resolve();
    script.onerror = (e) => reject(`Script loading error: ${e}`);
    document.head.appendChild(script);
  });
}

function loadCss(href) {
  return new Promise((resolve, reject) => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    link.onload = () => resolve();
    link.onerror = (e) => reject(`CSS loading error: ${e}`);
    document.head.appendChild(link);
  });
}

function renderMarkdown(markdownContent, dataProperty) {
  if (typeof marked.parse === 'function') {
    const markdownContainer = document.getElementById(`markdown_${dataProperty}`);
    markdownContainer.innerHTML = marked.parse(markdownContent);

    document.getElementById(`loading_${dataProperty}`).style.display = "none";
    markdownContainer.style.display = "block";
  } else {
    console.error('Marked library is not available');
  }
}
