document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('pdf-form');
  const fileInput = document.getElementById('file-input');
  const message = document.getElementById('message');
  const downloadBtn = document.getElementById('download-btn');
  const progressContainer = document.getElementById('progress-container');
  const progressBar = document.getElementById('progress-bar');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const file = fileInput.files[0];

    if (!file) {
      message.textContent = 'Please choose a PDF file.';
      return;
    }

    message.textContent = 'Uploading and converting...';
    progressContainer.classList.remove('hidden');
    progressBar.style.width = '0%';
    downloadBtn.classList.add('hidden');

    const formData = new FormData();
    formData.append('file', file);

    // Simulate progress
    let fakeProgress = 0;
    const interval = setInterval(() => {
      if (fakeProgress < 90) {
        fakeProgress += 10;
        progressBar.style.width = fakeProgress + '%';
      }
    }, 200);

    fetch('/convert', {
      method: 'POST',
      body: formData,
    })
      .then((res) => {
        clearInterval(interval);
        if (!res.ok) throw new Error("Conversion failed");
        progressBar.style.width = '100%';
        return res.blob();
      })
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        downloadBtn.href = url;
        downloadBtn.download = file.name.replace('.pdf', '.docx');
        downloadBtn.classList.remove('hidden');
        message.textContent = '✅ Conversion successful!';
      })
      .catch((err) => {
        clearInterval(interval);
        message.textContent = '❌ Error: ' + err.message;
        progressBar.style.width = '0%';
        downloadBtn.classList.add('hidden');
      });
  });
});
