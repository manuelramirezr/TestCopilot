import React from 'react';

function AudioPlayer() {
  return (
    <div>
      <audio controls>
        <source src="path_to_your_mp3_file.mp3" type="audio/mpeg" />
        Your browser does not support the audio element.
      </audio>
    </div>
  );
}

export default AudioPlayer;