document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('upload-form');
  const fileInput = document.getElementById('music-file');
  const musicList = document.getElementById('music-list');
  const audioPlayer = document.getElementById('audio-player');

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const file = fileInput.files[0];
    if (!file) return alert('Please select a file');

    const formData = new FormData();
    formData.append('music', file);

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      if (data.filename) {
        addMusicItem(data.filename);
        fileInput.value = ''; // clear input
      } else {
        alert('Upload failed');
      }
    })
    .catch(() => alert('Error uploading file'));
  });

  function addMusicItem(filename) {
    const li = document.createElement('li');
    li.className = 'music-item';

    const title = document.createElement('span');
    title.textContent = filename;

    const button = document.createElement('button');
    button.textContent = 'Play';
    button.className = 'play-button';
    button.addEventListener('click', () => {
      audioPlayer.src = `/music_files/${filename}`;
      audioPlayer.play();
    });

    li.appendChild(title);
    li.appendChild(button);
    musicList.appendChild(li);
  }

  // Load existing files on page load
  fetch('/list')
    .then(res => res.json())
    .then(files => {
      files.forEach(addMusicItem);
    });
});
