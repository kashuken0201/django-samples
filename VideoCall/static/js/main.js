var room_name = document.getElementById("room-name").innerHTML;
var username = document.getElementById("username").innerHTML;

var localVideo = document.getElementById('local-video');

const btnToggleAudio = document.getElementById('btn-toggle-audio');
const btnToggleVideo = document.getElementById('btn-toggle-video');

var video_streams = document.getElementById('video-streams');

var messageList = document.getElementById('message-list');
var messageInput = document.getElementById('msg');
var btnSendMsg = document.getElementById('btn-send');

var mapPeers = {};

var websocket;

var localStream

function createWebsocket(){
    var loc = window.location;
    var wsStart = 'ws://';

    if (loc.protocol == 'https:') {
        wsStart = 'wss://';
    }

    var endPoint = wsStart + loc.host + '/' + room_name + '/';

    console.log(endPoint);

    websocket = new WebSocket(endPoint);

    websocket.addEventListener('open', () => {
        console.log('Connected to server');
        sendSignal('new-peer', {});
    });
    websocket.onmessage = webSocketOnMessage;
    websocket.addEventListener('close', () => {
        console.log('Disconnected from server');
    });
    websocket.addEventListener('error', () => {
        console.log('Error');
    });
}

// Send signal to server
function sendSignal(action, message) {
    var jsonStr = JSON.stringify({
        'peer': username,
        'action': action,
        'message': message,
    });
    websocket.send(jsonStr);
}

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

        if (audioTracks[0].enabled){
            btnToggleAudio.style.backgroundColor = '#fff';
        }
        else{
            btnToggleAudio.style.backgroundColor = '#ff0000';
        }
    });

    btnToggleVideo.addEventListener('click', () => {
        videoTracks[0].enabled = !videoTracks[0].enabled;
        if (videoTracks[0].enabled){
            btnToggleVideo.style.backgroundColor = '#fff';
        }
        else{
            btnToggleVideo.style.backgroundColor = '#ff0000';
        }
    });

    createWebsocket();

    return playStream(localVideo, stream);
}).catch(err => {
    console.log(err);
});

function webSocketOnMessage(event) {
    var parsedData = JSON.parse(event.data);
    var peerUsername = parsedData['peer'];
    var action = parsedData['action'];

    console.log('Received message from peer: ' + peerUsername);

    if (username == peerUsername) {
        return;
    }
    var receiver_channel_name = parsedData['message']['receiver_channel_name'];

    if (action == 'new-peer') {
        createOfferner(peerUsername, receiver_channel_name);
        return;
    }
    if (action == 'new-offer') {
        var offer = parsedData['message']['sdp'];

        console.log('offer: '+peerUsername);

        createAnswerer(offer, peerUsername, receiver_channel_name);
    }
    if (action == 'new-answer') {
        var answer = parsedData['message']['sdp'];

        var peer = mapPeers[peerUsername][0];

        console.log("mapPeers: " + mapPeers);
        
        peer.setRemoteDescription(answer)
            .then(() => {
                console.log('Answer set successfully for %s.', peerUsername);
            });
        
        return;
    }
}

function createOfferner(peerUsername, receiver_channel_name){
    var peer = new RTCPeerConnection(null);
 
    addLocalTracks(peer);

     // create and manage an RTCDataChannel
     var dc = peer.createDataChannel("channel");
     dc.onopen = () => {
         console.log("Connection opened.");
     };
    dc.addEventListener('message', dcOnMessage);

    var remoteVideo = createVideo(peerUsername);
    addRemoteTracks(peer, remoteVideo);

    // add peer to map
    mapPeers[peerUsername] = [peer, dc];

    // Check connection peer
    peer.addEventListener('iceconnectionstatechange', () => {
        var iceConnectionState = peer.iceConnectionState;
        // Disconnected or failed or closed delete video stream frame
        if (iceConnectionState == 'disconnected' || iceConnectionState == 'failed' || iceConnectionState == 'closed') {
            delete mapPeers[peerUsername];

            if (iceConnectionState != 'closed') {
                peer.close();
            }
            removeVideo(remoteVideo);
        }
    });

    // Listen for local ICE candidates on the local RTCPeerConnection
    peer.addEventListener('icecandidate', (event) => {
        if (!event.candidate) {
            console.log('candidate ', event.candidate);
            sendSignal('new-offer', {
                'sdp': peer.localDescription,
                'receiver_channel_name': receiver_channel_name
            });
        }
    });

    // Create local description to communicate peers
    peer.createOffer()
        .then(offer =>  peer.setLocalDescription(offer))
        .then(() => {
            console.log('local description set successfully for ' + peerUsername);
        });
}

function createAnswerer(offer, peerUsername, receiver_channel_name) {
    var peer = new RTCPeerConnection(null);

    addLocalTracks(peer);

    var remoteVideo = createVideo(peerUsername);
    addRemoteTracks(peer, remoteVideo);

    peer.addEventListener('datachannel', (event) => {
        peer.dc = event.channel;
        peer.dc.addEventListener('message', dcOnMessage);

        mapPeers[peerUsername] = [peer, peer.dc];
    });

    peer.addEventListener('iceconnectionstatechange', () => {
        var iceConnectionState = peer.iceConnectionState;
        if (iceConnectionState == 'disconnected' || iceConnectionState == 'failed' || iceConnectionState == 'closed') {
            delete mapPeers[peerUsername];

            if (iceConnectionState != 'closed') {
                peer.close();
            }
            removeVideo(remoteVideo);
        }
    });

    peer.addEventListener('icecandidate', (event) => {
        if (!event.candidate) {
            sendSignal('new-answer', {
                'sdp': peer.localDescription,
                'receiver_channel_name': receiver_channel_name,
            });
        }
    });

    peer.setRemoteDescription(offer)
        .then(() => {
            console.log('remoteDescription set successfully for ' + peerUsername);

            return peer.createAnswer();
        })
        .then(a => {
            console.log('Answer created successfully');

            return peer.setLocalDescription(a);
        })
        .then(() => {
            console.log('Answer created for %s.', peerUsername);
        })
        .catch(error => {
            console.log('Error creating answer for %s.', peerUsername);
            console.log(error);
        });
}

// Add local tracks to peer connection
function addLocalTracks(peer) {
    localStream.getTracks().forEach(track => {
        peer.addTrack(track, localStream);
    });
}

// Add track of peer connection to video
function addRemoteTracks(peer, remoteVideo) {
    var remoteStream = new MediaStream();

    remoteVideo.srcObject = remoteStream;

    // Listen for tracks remote stream
    peer.addEventListener('track', async (event) => {
        remoteStream.addTrack(event.track, remoteStream);
    });
}

// Create view for peer
function createVideo(peerUsername) {
    var person = `<div class="video-container" id="video-container">
                    <div class="video-player">
                            <video class="video-player" id="${peerUsername}-video"></video>
                        <div class="username-wrapper">
                            <span class="user-name" id="${peerUsername}-username">${peerUsername}</span>
                        </div>
                    </div>
                </div>`

    video_streams.insertAdjacentHTML('beforeend', person);
    var remoteVideo = document.getElementById(peerUsername + '-video');

    remoteVideo.id = peerUsername + '-video';
    remoteVideo.autoplay = true;
    remoteVideo.playsInline = true;

    return remoteVideo;
}

// Remove view for peer
function removeVideo(remoteVideo) {
    var videoWrapper = remoteVideo.parentNode.parentNode;

    videoWrapper.parentNode.removeChild(videoWrapper);
}


function dcOnMessage(event) {
    console.log('Data channel message: ' + event.data);
    var message = event.data;

    var li = document.createElement('li');
    li.appendChild(document.createTextNode(message));
    messageList.appendChild(li);
}

btnSendMsg.addEventListener('click', btnSendMsgOnClick);

function btnSendMsgOnClick(){
    var message = messageInput.value;
    
    var li = document.createElement("li");
    li.appendChild(document.createTextNode("Me: " + message));
    messageList.appendChild(li);
    
    var dataChannels = getDataChannels();

    console.log('Sending: ', message);

    // send to all data channels
    for(index in dataChannels){
        console.log('Sending to: ', dataChannels[index].label);
        dataChannels[index].send(username + ': ' + message);
    }
    
    messageInput.value = '';
}

messageInput.addEventListener('keyup', function(event){
    if(event.keyCode == 13){
        // prevent from putting 'Enter' as input
        event.preventDefault();

        // click send message button
        btnSendMsg.click();
    }
});

function getDataChannels(){
    var dataChannels = [];
    for(peerUsername in mapPeers){
        var dataChannel = mapPeers[peerUsername][1];

        dataChannels.push(dataChannel);
    }

    return dataChannels;
}