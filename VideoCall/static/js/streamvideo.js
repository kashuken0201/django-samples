var room_name = document.getElementById("room-name").innerHTML;
var username = document.getElementById("username").innerHTML;

var localVideo = document.getElementById('local-video');

const btnToggleAudio = document.getElementById('btn-toggle-audio');
const btnToggleVideo = document.getElementById('btn-toggle-video');

var video_streams = document.getElementById('video-streams');

var mapPeers = {};

var websocket;

var localStream

function openStream(){
    const config = { audio: true, video: true };
    return navigator.mediaDevices.getUserMedia(config);
}

function playStream(video, stream){
    video.srcObject = stream;
    video.autoplay = true;
    video.playsInline = true;
}

// Open my stream
openStream().then(stream => {
    localStream = stream;
    localVideo.muted = true;

    // get devices video and audio
    var audioTracks = stream.getAudioTracks();
    var videoTracks = stream.getVideoTracks();

    // get first device video and audio
    audioTracks[0].enabled = true;
    videoTracks[0].enabled = true;

    // Switch sate 
    btnToggleAudio.addEventListener('click', () => {
        audioTracks[0].enabled = !audioTracks[0].enabled;

        if (audioTracks[0].enabled) btnToggleAudio.style.backgroundColor = '#fff';
        else btnToggleAudio.style.backgroundColor = '#ff0000';
        });

    btnToggleVideo.addEventListener('click', () => {
        videoTracks[0].enabled = !videoTracks[0].enabled;
        if (videoTracks[0].enabled) btnToggleVideo.style.backgroundColor = '#fff';
        else btnToggleVideo.style.backgroundColor = '#ff0000';
        });


    return playStream(localVideo, stream);
}).catch(err => {
    console.log(err);
});

function addVideoStream(stream, name){
    var person = `<div class="video-container" id="video-container">
    <div class="video-player">
            <video class="video-player" id="local-video1"></video>
        <div class="username-wrapper">
            <span class="user-name" id="username">{{username}}</span>
        </div>
    </div>
</div>`
    video_streams.insertAdjacentHTML('beforeend', person);
    video = document.getElementById('local-video1');
    video.srcObject = stream;
    video.muted = true;
    video.autoplay = true;
    video.playsInline = true;
    playStream(video, stream);
}
openStream().then(stream => {
    addVideoStream(stream, 'local-video');
}
).catch(err => {
    console.log(err);
});