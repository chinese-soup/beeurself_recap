document.addEventListener("DOMContentLoaded", function() {
  const additionalContent = document.querySelector('.additional-content');
  let contentLoaded = false;

  // Function to load additional content
  function loadAdditionalContent() {
    if (!contentLoaded && isElementInViewport(additionalContent)) {
      // Simulated content loading, you can fetch data here
      const newContent = document.createElement('p');
      newContent.textContent = 'More content loaded...';
      additionalContent.appendChild(newContent);
      contentLoaded = true;
      additionalContent.style.display = 'block';
    }
  }