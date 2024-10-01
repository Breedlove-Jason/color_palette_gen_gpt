document
  .getElementById('paletteForm')
  .addEventListener('submit', function (event) {
    event.preventDefault();

    const textPrompt = document.getElementById('text_prompt').value;

    fetch('/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `text_prompt=${encodeURIComponent(textPrompt)}`,
    })
      .then((response) => response.json())
      .then((data) => {
        const paletteContainer = document.getElementById('paletteContainer');
        paletteContainer.innerHTML = ''; // Clear previous palette

        data.colors.forEach((color) => {
          const colorDiv = document.createElement('div');
          colorDiv.classList.add('color-column');
          colorDiv.style.backgroundColor = color;
          colorDiv.innerHTML = `<span>${color}</span>`;

          // Click event to copy the hex code to clipboard
          colorDiv.addEventListener('click', function () {
            navigator.clipboard.writeText(color).then(() => {
              alert(`Copied ${color} to clipboard!`);
            });
          });

          paletteContainer.appendChild(colorDiv);
        });
      });
  });
