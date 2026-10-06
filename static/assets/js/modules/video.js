// Video section: click the play button to load the video (file or YouTube)
function initVideoPlayer(frame) {
  const play = frame.querySelector('.video__play');
  const file = frame.dataset.video;
  const youtube = frame.dataset.youtube;

  play?.addEventListener('click', () => {
    let player;
    if (file) {
      player = document.createElement('video');
      player.src = file;
      player.controls = true;
      player.autoplay = true;
      player.playsInline = true;
    } else if (youtube) {
      player = document.createElement('iframe');
      player.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(youtube)}?autoplay=1&rel=0`;
      player.title = 'Ketan Organics video';
      player.allow = 'autoplay; encrypted-media; picture-in-picture';
      player.allowFullscreen = true;
    } else {
      console.warn('Video section: no data-video or data-youtube set on .video__frame');
      return;
    }
    frame.appendChild(player);
    frame.classList.add('is-playing');
  });
}

document.querySelectorAll('[data-video-player]').forEach(initVideoPlayer);
