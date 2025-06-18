document.getElementById("upload-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const fileInput = document.getElementById("word-file");
  const formData = new FormData();
  formData.append("word_file", fileInput.files[0]);

  fetch("/convert", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      const fileId = data.file_id;
      const progressBar = document.getElementById("progress-bar");
      const progressText = document.getElementById("progress-text");
      const downloadBtn = document.getElementById("download-btn");

      const interval = setInterval(() => {
        fetch(`/progress/${fileId}`)
          .then((res) => res.json())
          .then((data) => {
            const progress = data.progress;
            progressBar.style.width = progress + "%";
            progressText.textContent = progress + "%";

            if (progress >= 100) {
              clearInterval(interval);
              downloadBtn.href = `/download/${fileId}`;
              downloadBtn.style.display = "inline-block";
            }
          });
      }, 500);
    });
});
