import './index.css';

// Get references to all HTML elements
const fileInput = document.getElementById('file-upload');
const welcomeMessage = document.getElementById('welcome-message');
const loader = document.getElementById('loader');
const resultsSection = document.getElementById('results-section');
const originalImage = document.getElementById('original-image');
const constellationCanvas = document.getElementById('constellation-canvas');
const constellationNames = document.getElementById('constellation-names');

// --- THE NEW DRAWING FUNCTION ---
function drawConstellation(image, data) {
  const canvas = constellationCanvas;
  const ctx = canvas.getContext('2d');

  // Match canvas size to the image's natural size
  canvas.width = image.naturalWidth;
  canvas.height = image.naturalHeight;

  // 1. Draw the original image onto the canvas as the background
  ctx.drawImage(image, 0, 0);

  // 2. Set styles for drawing lines and text
  ctx.strokeStyle = '#22d3ee'; // A bright cyan color
  ctx.lineWidth = 2;
  ctx.fillStyle = '#22d3ee';
  ctx.font = '16px sans-serif';

  // 3. Draw the constellation lines
  data.lines.forEach(line => {
    const [x1, y1, x2, y2] = line;
    ctx.beginPath();
    // Convert relative coordinates (0.0-1.0) to absolute pixel coordinates
    ctx.moveTo(x1 * canvas.width, y1 * canvas.height);
    ctx.lineTo(x2 * canvas.width, y2 * canvas.height);
    ctx.stroke();
  });

  // 4. Draw the star points and their names
  data.points.forEach(point => {
    const x = point.x * canvas.width;
    const y = point.y * canvas.height;
    
    // Draw a small circle for the star
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, 2 * Math.PI); // 5-pixel radius circle
    ctx.fill();

    // Draw the star's name next to it
    ctx.fillText(point.name, x + 10, y + 5);
  });
}

// --- FILE UPLOAD LOGIC (UPDATED) ---
const handleFileUpload = (file) => {
  // Prepare UI for loading
  welcomeMessage.style.display = 'none';
  resultsSection.style.display = 'none';
  loader.style.display = 'block';

  const formData = new FormData();
  formData.append('file', file);

  // Create a temporary URL for the original image to display it
  const originalImageUrl = URL.createObjectURL(file);
  originalImage.src = originalImageUrl;

  // Send the image to the backend to get the JSON data
  fetch('/upload', {
    method: 'POST',
    body: formData,
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`Server responded with status: ${response.status}`);
    }
    return response.json(); // <-- THIS IS THE KEY CHANGE: We expect JSON now
  })
  .then(data => {
    // We have the data! Now, wait for the original image to be fully loaded before we draw on it
    originalImage.onload = () => {
      // Call our new drawing function
      drawConstellation(originalImage, data);

      // Populate the "Detected Constellations" list
      const namesList = data.points.map(point => point.name).join(', ');
      const constellationName = data.constellation;
      const confidence = data.confidence;
      const method = data.method;
      const detectedStars = data.detected_stars;
      const description = data.description;
      const constellationFullName = constellationName + " - " + description;
      const starNames = "Stars: " + namesList;
      const confidenceLevel = "Confidence: " + confidence;
      const detectionMethod = "Method: " + method;
      const starsDetected = "Detected Stars: " + detectedStars;

      // a new heading element
      const heading = document.createElement('h4');
      heading.textContent = constellationFullName;
      heading.style.fontWeight = 'bold'; // Make the heading bold
      heading.style.fontSize = '1.2em';
      const br = document.createElement('br');
      const br2 = document.createElement('br');
      const br3 = document.createElement('br');
      const br4 = document.createElement('br');
      
      const starNamesText = document.createTextNode(starNames);
      const confidenceLevelText = document.createTextNode(confidenceLevel);
      const detectionMethodText = document.createTextNode(detectionMethod);
      const starsDetectedText = document.createTextNode(starsDetected);
      
      const constellationNames = document.getElementById('constellation-names');
      constellationNames.innerHTML = ''; // Clear previous results
      constellationNames.appendChild(heading); // Add the heading
      constellationNames.appendChild(starNamesText);
      constellationNames.appendChild(br);
      constellationNames.appendChild(confidenceLevelText);
      constellationNames.appendChild(br2);
      constellationNames.appendChild(detectionMethodText);
      constellationNames.appendChild(br3);
      constellationNames.appendChild(starsDetectedText);
      

      // Hide loader and show results
      loader.style.display = 'none';
      resultsSection.style.display = 'block';
    };
    // If the image is already loaded (from cache), trigger onload manually
    if (originalImage.complete) {
      originalImage.onload();
    }
  })
  .catch(error => {
    console.error('FETCH ERROR:', error);
    loader.style.display = 'none';
    welcomeMessage.style.display = 'block';
    alert('Something went wrong. Please try again.');
  });
};

// Initial setup
loader.style.display = 'none';
resultsSection.style.display = 'none';

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (file) {
    handleFileUpload(file);
s  }
});