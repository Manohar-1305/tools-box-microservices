document.getElementById("convert-btn").addEventListener("click", async () => {
  const text = document.getElementById("text-input").value.trim();
  const progressContainer = document.getElementById("progress-container");
  const progressBar = document.getElementById("progress-bar");
  const progressText = document.getElementById("progress-text");
  const audioPlayer = document.getElementById("audio-player");
  const downloadBtn = document.getElementById("download-btn");
  const status = document.getElementById("status");

  if (!text) {
    status.textContent = "⚠️ Please enter some text.";
    return;
  }

  // Reset UI
  status.textContent = "";
  audioPlayer.classList.add("hidden");
  downloadBtn.classList.add("hidden");
  progressBar.style.width = "0%";
  progressText.textContent = "0%";
  progressContainer.classList.remove("hidden");

  // Start fake progress animation
  let progress = 0;
  let animationRunning = true;

  const interval = setInterval(() => {
    if (progress >= 95 || !animationRunning) {
      clearInterval(interval);
    } else {
      progress += 1;
      progressBar.style.width = `${progress}%`;
      progressText.textContent = `${progress}%`;
    }
  }, 50); // ~5 seconds to reach 95%

  try {
    const response = await fetch("/convert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!response.ok) throw new Error("Conversion failed");

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    // Complete progress
    animationRunning = false;
    progressBar.style.width = "100%";
    progressText.textContent = "100%";

    // Show results
    audioPlayer.src = url;
    audioPlayer.classList.remove("hidden");
    downloadBtn.href = url;
    downloadBtn.download = "output.mp3";
    downloadBtn.classList.remove("hidden");
    status.textContent = "✅ Conversion complete!";
  } catch (err) {
    animationRunning = false;
    progressBar.style.width = "0%";
    progressText.textContent = "0%";
    status.textContent = "❌ Error: " + err.message;
  }
});
