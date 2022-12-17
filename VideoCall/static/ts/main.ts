const room_name = document.getElementById("room-name")?.innerHTML||'';
const username = document.getElementById("username")?.innerHTML||'';

const room_id = document.getElementById("room-id")?.innerHTML||'';
const user_id = (document.getElementById("user-id") as HTMLInputElement)?.value||'';

const localVideo = document.getElementById('local-video') as HTMLVideoElement;

const btnToggleAudio = document.getElementById('btn-toggle-audio') as HTMLButtonElement;
const btnToggleVideo = document.getElementById('btn-toggle-video') as HTMLButtonElement;

const video_Streams = document.getElementById('video-streams');

const messageList = document.getElementById('message-list') as HTMLUListElement;
const messageInput = document.getElementById('msg') as HTMLInputElement;
const btnSendMsg = document.getElementById('btn-send') as HTMLButtonElement;

let mapPeers = new Map<string, [RTCPeerConnection, RTCDataChannel]>();

let websocket;

let localStream

function CreateWebsocket() : void {
    var loc = window.location;
    var wsStart = 'ws://';

    if (loc.protocol == 'https:') {
        wsStart = 'wss://';
    }

    var endPoint = wsStart + loc.host + '/meeting/' + room_id + '/';

    console.log(endPoint);

    websocket = new WebSocket(endPoint);

    websocket.addEventListener('open', () => {
        console.log('Connected to server');
        SendSignal('new-peer', {});
    });
    websocket.onmessage = WebSocketOnMessage;
    websocket.addEventListener('close', () => {
        console.log('Disconnected from server');
    });
    websocket.addEventListener('error', () => {
        console.log('Error');
    });
}

// Send signal to server
function SendSignal(action: string, message): void {
    var jsonStr = JSON.stringify({
        'peer_username': username,
        'peer_id': user_id,
        'action': action,
        'message': message,
    });
    websocket.send(jsonStr);
}

function OpenStream(): Promise<MediaStream> {
    const config = { audio: true, video: true };
    return navigator.mediaDevices.getUserMedia(config);
}

function PlayStream(video: HTMLVideoElement, stream: MediaStream): void{
    video.srcObject = stream;
    video.autoplay = true;
    video.playsInline = true;
}

// Open my stream
OpenStream().then(stream => {
    if(localVideo == null) {
        return;
    }
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

    CreateWebsocket();

    return PlayStream(localVideo, stream);
}).catch(err => {
    console.log(err);
});

function WebSocketOnMessage(event: MessageEvent): void {
    let parsedData = JSON.parse(event.data);
    let peerUserid = parsedData['peer_id'];
    let peerUsername = parsedData['peer_username'];
    let action = parsedData['action'];

    console.log('Received message from peer: ' + peerUserid);

    if (user_id == peerUserid) {
        return;
    }
    var receiver_channel_name = parsedData['message']['receiver_channel_name'];

    if (action == 'new-peer') {
        CreateOfferner(peerUserid, peerUsername, receiver_channel_name);
        return;
    }
    if (action == 'new-offer') {
        var offer = parsedData['message']['sdp'];

        console.log('offer: '+peerUserid);

        CreateAnswerer(offer, peerUserid, peerUsername, receiver_channel_name);
    }
    if (action == 'new-answer') {
        var answer = parsedData['message']['sdp'];

        var peer = mapPeers.get(peerUserid)?.[0];
        
        if(peer) {
            peer.setRemoteDescription(answer)
                .then(() => {
                    console.log('Answer set successfully for %s.', peerUserid);
                });
        }
        return;
    }
}

function CreateOfferner(peerUserid: string, peerUsername: string, receiver_channel_name: string): void {
    var peer = new RTCPeerConnection(undefined);
 
    AddLocalTracks(peer);

     // create and manage an RTCDataChannel
     var dc = peer.createDataChannel("channel");
     dc.onopen = () => {
         console.log("Connection opened.");
     };
    dc.addEventListener('message', DcOnMessage);

    var remoteVideo = CreateVideo(peerUserid, peerUsername);
    AddRemoteTracks(peer, remoteVideo);

    // add peer to map
    mapPeers.set(peerUserid, [peer, dc]);

    // Check connection peer
    peer.addEventListener('iceconnectionstatechange', () => {
        var iceConnectionState = peer.iceConnectionState;
        // Disconnected or failed or closed delete video stream frame
        if (iceConnectionState == 'disconnected' || iceConnectionState == 'failed' || iceConnectionState == 'closed') {
            mapPeers.delete(peerUserid);

            if (iceConnectionState != 'closed') {
                peer.close();
            }
            RemoveVideo(remoteVideo);
        }
    });

    // Listen for local ICE candidates on the local RTCPeerConnection
    peer.addEventListener('icecandidate', (event) => {
        if (!event.candidate) {
            console.log('candidate ', event.candidate);
            SendSignal('new-offer', {
                'sdp': peer.localDescription,
                'receiver_channel_name': receiver_channel_name
            });
        }
    });

    // Create local description to communicate peers
    peer.createOffer()
        .then(offer =>  peer.setLocalDescription(offer))
        .then(() => {
            console.log('local description set successfully for ' + peerUserid);
        });
}

function CreateAnswerer(offer: RTCSessionDescription, peerUserid: string, peerUsername: string, receiver_channel_name: string): void {
    var peer = new RTCPeerConnection(undefined);

    AddLocalTracks(peer);

    var remoteVideo = CreateVideo(peerUserid, peerUsername);
    AddRemoteTracks(peer, remoteVideo);

    peer.addEventListener('datachannel', (event) => {
        var dc = event.channel;
        dc.addEventListener('message', DcOnMessage);

        mapPeers.set(peerUserid, [peer, dc]);
    });

    peer.addEventListener('iceconnectionstatechange', () => {
        var iceConnectionState = peer.iceConnectionState;
        if (iceConnectionState == 'disconnected' || iceConnectionState == 'failed' || iceConnectionState == 'closed') {
            mapPeers.delete(peerUserid);

            if (iceConnectionState != 'closed') {
                peer.close();
            }
            RemoveVideo(remoteVideo);
        }
    });

    peer.addEventListener('icecandidate', (event) => {
        if (!event.candidate) {
            SendSignal('new-answer', {
                'sdp': peer.localDescription,
                'receiver_channel_name': receiver_channel_name,
            });
        }
    });

    peer.setRemoteDescription(offer)
        .then(() => {
            console.log('remoteDescription set successfully for ' + peerUserid);

            return peer.createAnswer();
        })
        .then(a => {
            console.log('Answer created successfully');

            return peer.setLocalDescription(a);
        })
        .then(() => {
            console.log('Answer created for %s.', peerUserid);
        })
        .catch(error => {
            console.log('Error creating answer for %s.', peerUserid);
            console.log(error);
        });
}

// Add local tracks to peer connection
function AddLocalTracks(peer: RTCPeerConnection): void {
    localStream.getTracks().forEach(track => {
        peer.addTrack(track, localStream);
    });
}

// Add track of peer connection to video
function AddRemoteTracks(peer: RTCPeerConnection, remoteVideo: HTMLVideoElement): void {
    var remoteStream = new MediaStream();

    remoteVideo.srcObject = remoteStream;

    // Listen for tracks remote stream
    peer.addEventListener('track', async (event) => {
        remoteStream.addTrack(event.track);
    });
}

// Create view for peer
function CreateVideo(peerUserid: string, peerUsername: string): HTMLVideoElement {
    var person = `<div class="video-container" id="video-container">
                    <div class="video-player">
                            <video class="video-player" id="${peerUserid}-video"></video>
                        <div class="username-wrapper">
                            <span class="user-name" id="${peerUserid}-username">${peerUsername}</span>
                        </div>
                    </div>
                </div>`
    if (video_Streams != null) {
        video_Streams.insertAdjacentHTML('beforeend', person);
    }
    var remoteVideo = document.getElementById(peerUserid + '-video') as HTMLVideoElement;
    
    if(remoteVideo != null){
        remoteVideo.id = peerUserid + '-video';
        remoteVideo.autoplay = true;
        remoteVideo.playsInline = true;
    }

    return remoteVideo;
}

// Remove view for peer
function RemoveVideo(remoteVideo): void {
    var videoWrapper = remoteVideo.parentNode.parentNode;

    videoWrapper.parentNode.removeChild(videoWrapper);
}

function CreateMessage(username: string, message: string): string {
    var now = new Date();
    var withPmAm = now.toLocaleTimeString('en-US', {
        // en-US can be set to 'default' to use user's browser settings
        hour: '2-digit',
        minute: '2-digit',
      });
    var msg_html = `<div class="message">
                        <p class="meta">${username}<span> ${withPmAm}</span></p>
                        <p class="text">
                            ${message}
                        </p>
                    </div>`
    return msg_html;
}

function AddMessage(msg_html: string): void {
    messageList.insertAdjacentHTML('beforeend', msg_html);
    messageList.scrollTop = messageList.scrollHeight;
}

function DcOnMessage(event) {
    console.log('Data channel message: ' + event.data);
    var message = event.data;
    
    var name = message.split(':')[0];
    var msg = message.split(':')[1];

    var msg_html = CreateMessage(name, msg);
    AddMessage(msg_html);
}

if (btnSendMsg != null) {
    btnSendMsg.addEventListener('click', BtnSendMsgOnClick);
}

function BtnSendMsgOnClick(): void {
    var message = messageInput.value;
    if(message == ''){
        return;
    }
    
    var msg_html = CreateMessage(username, message);
    AddMessage(msg_html);
    
    var dataChannels = GetDataChannels();

    console.log('Sending: ', message);

    // send to all data channels
    dataChannels.forEach(dc => {
        dc.send(username + ':' + message);
    });
    
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

function GetDataChannels(): RTCDataChannel[] {
    var dataChannels = new Array();
    mapPeers.forEach((value, key) => {
        dataChannels.push(value[1]);
    });
    return dataChannels;
}

let deleteMember = async() =>{
    await fetch('/meeting/member/'+user_id+'/delete/', {
        method: 'POST',
    });
}
window.onbeforeunload = event => {
    event.returnValue = 'Are you sure you want to leave the room?';
    deleteMember();
}
  