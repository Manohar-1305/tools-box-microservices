document.getElementById("uploadForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(document.getElementById("uploadForm"));
    const progressBar = document.getElementById("progressBar");
    const progressContainer = document.getElementById("progressContainer");
    const message = document.getElementById("message");
    const downloadLink = document.getElementById("downloadLink");
    const fileNameDisplay = document.getElementById("fileNameDisplay");
    const convertAnotherBtn = document.getElementById("convertAnotherBtn");

    // Reset UI
    progressBar.style.width = "0%";
    progressBar.innerText = "0%";
    progressContainer.style.display = "block";
    message.innerText = "Converting... Please wait ⏳";
    downloadLink.style.display = "none";
    fileNameDisplay.style.display = "none";
    convertAnotherBtn.style.display = "none";

    // Simulate progress bar
    let percent = 0;
    const interval = setInterval(() => {
        if (percent < 90) {
            percent++;
            progressBar.style.width = percent + "%";
            progressBar.innerText = percent + "%";
        }
    }, 80);

    // Upload and convert
    fetch("/pdf_converter", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(interval);

        if (data.success) {
            progressBar.style.width = "100%";
            progressBar.innerText = "100%";
            message.innerText = "✅ Conversion complete!";

            fileNameDisplay.innerText = "Converted File: " + data.pdf_file;
            fileNameDisplay.style.display = "block";

            downloadLink.href = "/download/" + data.pdf_file;
            downloadLink.download = data.pdf_file;
            downloadLink.style.display = "inline-block";

            convertAnotherBtn.style.display = "inline-block";
        } else {
            progressBar.style.width = "0%";
            progressBar.innerText = "0%";
            message.innerText = "❌ Error: " + data.error;
        }
    })
    .catch(error => {
        clearInterval(interval);
        progressBar.style.width = "0%";
        progressBar.innerText = "0%";
        message.innerText = "❌ Conversion failed. Please try again.";
        console.error(error);
    });
});

document.getElementById("convertAnotherBtn").addEventListener("click", function () {
    const form = document.getElementById("uploadForm");
    form.reset();

    // Hide all feedback
    document.getElementById("progressBar").style.width = "0%";
    document.getElementById("progressBar").innerText = "0%";
    document.getElementById("progressContainer").style.display = "none";
    document.getElementById("message").innerText = "";
    document.getElementById("fileNameDisplay").style.display = "none";
    document.getElementById("downloadLink").style.display = "none";
    document.getElementById("convertAnotherBtn").style.display = "none";

    // Scroll back to file input
    document.getElementById("word_file").scrollIntoView({ behavior: "smooth" });
});
