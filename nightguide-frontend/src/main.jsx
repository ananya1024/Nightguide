import './index.css';

// Get references to all the important HTML elements
const fileInput = document.getElementById('file-upload');
const welcomeMessage = document.getElementById('welcome-message');
const loader = document.getElementById('loader');
const resultsSection = document.getElementById('results-section');
const originalImage = document.getElementById('original-image');
const constellationImage = document.getElementById('constellation-image');

// Add the .hidden class to the CSS to control visibility
const style = document.createElement('style');
style.innerHTML = `.hidden { display: none; }`;
document.head.appendChild(style);

// This function handles the entire upload and display process
const handleFileUpload = (file) => {
  // 1. Prepare UI for loading
  welcomeMessage.classList.add('hidden');
  resultsSection.classList.add('hidden');
  loader.classList.remove('hidden');

  const formData = new FormData();
  formData.append('file', file);

  // Display the original image immediately
  const originalImageUrl = URL.createObjectURL(file);
  originalImage.src = originalImageUrl;

  // 2. Send the image to the backend
  fetch('/upload', {
    method: 'POST',
    body: formData,
  })
    .then(response => {
      if (!response.ok) {
        // If the server sends back an error, we stop here
        throw new Error(`Server responded with status: ${response.ok}`);
      }
      // 3. We expect an IMAGE blob back now, not JSON
      return response.blob();
    })
    .then(imageBlob => {
      // 4. Create a URL for the processed image from the backend
      const constellationImageUrl = URL.createObjectURL(imageBlob);
      // And display it in the constellation image tag
      constellationImage.src = constellationImageUrl;

      // 5. Show the results
      loader.classList.add('hidden');
      resultsSection.classList.remove('hidden');
    })
    .catch(error => {
      // Handle any errors that occurred during the fetch
      console.error('FETCH ERROR:', error);
      loader.classList.add('hidden');
      welcomeMessage.classList.remove('hidden'); // Show the welcome message again
      alert('Something went wrong during processing. Please try again.');
    });
};

// Listen for when a user chooses a file
fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    handleFileUpload(file);
  }
});