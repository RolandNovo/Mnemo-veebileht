// Kood on võetud Rauno Jaaska eestikeelse kõne transkribeerimisserveri demost
// modification for Flask <=> Javascript
// import { processTextData } from './flaskAndJavascript.js';

// This is a modified version of streaming_record.js from k2-fsa/sherpa
// https://github.com/k2-fsa/sherpa/blob/master/sherpa/bin/web/js/streaming_record.js

// The original file copies and modifies code
// from https://mdn.github.io/web-dictaphone/scripts/app.js
// and https://gist.github.com/meziantou/edb7217fddfbb70e899e

// const ASR_URL = 'ws://estasrstream.cloud.ut.ee/ws';  // See on ilma sertifikaadita domeen
const ASR_URL = 'wss://api.tartunlp.ai/speech-to-text/ws'; //sertifikaadiga

var socket;
var recognition_text = [];

function getDisplayResult() {
    let i = 0;
    let ans = '';
    for (let s in recognition_text) {
        if (recognition_text[s] == '') continue;

        ans += '' + i + ': ' + recognition_text[s] + '\n';
        i += 1;
    }
    return ans;
}

function initWebSocket() {
    // TODO: swap to wss
    socket = new WebSocket(ASR_URL);

    // Connection opened
    socket.addEventListener('open', function(event) {
        console.log('connected');
        recordBtn.disabled = false;
        recordBtn.innerHTML = 'Eeter!';
    });

    // Connection closed
    socket.addEventListener('close', function(event) {
        console.log('disconnected');
        recordBtn.disabled = false;
        recordBtn.innerHTML = 'Alusta';
    });

    // Listen for messages
    socket.addEventListener('message', function(event) {
        let message = JSON.parse(event.data);
        if (message.segment in recognition_text) {
            recognition_text[message.segment] = message.text;
        } else {
            recognition_text.push(message.text);
        }
        let text_area = document.getElementById('results');
        let text = getDisplayResult();
        if (text_area.value !== text) {
            text_area.value = getDisplayResult();
            text_area.scrollTop = text_area.scrollHeight; // auto scroll
        }
        console.log('Received message: ', event.data);
    });
}

const recordBtn = document.getElementById('streaming_record');
const stopBtn = document.getElementById('streaming_stop');
const googleTranscBtn = document.getElementById('transcBtn'); // lisatud Rolandi poolt
const eelmineBtn = document.getElementById('eelmine_tekst');
const järgmineBtn = document.getElementById('järgmine_tekst');

stopBtn.disabled = true;

let audioCtx;
let mediaStream;

let expectedSampleRate = 16000;
let recordSampleRate; // the sampleRate of the microphone
let recorder = null; // the microphone
let leftchannel = []; // TODO: Use a single channel

let recordingLength = 0; // number of samples so far

// clearBtn.onclick = function() {
//     document.getElementById('results').value = '';
//     recognition_text = [];
// };

recordBtn.onclick = function() {
    initWebSocket();

    mediaStream.connect(recorder);
    recorder.connect(audioCtx.destination);

    console.log('recorder started');
    recordBtn.style.background = 'red';

    stopBtn.disabled = false;
    recordBtn.disabled = true;
};

// copied/modified from https://mdn.github.io/web-dictaphone/
// and
// https://gist.github.com/meziantou/edb7217fddfbb70e899e
if (navigator.mediaDevices.getUserMedia) {
    console.log('getUserMedia supported.');

    // see https://w3c.github.io/mediacapture-main/#dom-mediadevices-getusermedia
    const constraints = { audio: true };

    let onSuccess = function(stream) {
        if (!audioCtx) {
            audioCtx = new AudioContext();
        }
        console.log(audioCtx);
        recordSampleRate = audioCtx.sampleRate;
        console.log('sample rate ' + recordSampleRate);

        // creates an audio node from the microphone incoming stream
        mediaStream = audioCtx.createMediaStreamSource(stream);
        console.log(mediaStream);

        // https://developer.mozilla.org/en-US/docs/Web/API/AudioContext/createScriptProcessor
        // bufferSize: the onaudioprocess event is called when the buffer is full
        var bufferSize = 2048;
        var numberOfInputChannels = 2;
        var numberOfOutputChannels = 2;
        if (audioCtx.createScriptProcessor) {
            recorder = audioCtx.createScriptProcessor(
                bufferSize, numberOfInputChannels, numberOfOutputChannels);
        } else {
            recorder = audioCtx.createJavaScriptNode(
                bufferSize, numberOfInputChannels, numberOfOutputChannels);
        }
        console.log(recorder);

        recorder.onaudioprocess = function(e) {
            let samples = new Float32Array(e.inputBuffer.getChannelData(0))
            samples = downsampleBuffer(samples, expectedSampleRate);

            let buf = new Int16Array(samples.length);
            for (var i = 0; i < samples.length; ++i) {
                let s = samples[i];
                if (s >= 1)
                    s = 1;
                else if (s <= -1)
                    s = -1;

                samples[i] = s;
                buf[i] = s * 32767;
            }

            socket.send(samples);

            leftchannel.push(buf);
            recordingLength += bufferSize;
        };

        stopBtn.onclick = function() {
            console.log('recorder stopped');

            socket.send('Done');
            console.log('Sent Done');

            socket.close();

            // stopBtn recording
            recorder.disconnect(audioCtx.destination);
            mediaStream.disconnect(recorder);

            recordBtn.style.background = '';
            recordBtn.style.color = '';

            stopBtn.disabled = true;
            recordBtn.disabled = false;
            console.log('recorder stopped');

            fetch('/process-text', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        textData: document.getElementById('results').value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    // Update page with processed text data
                    let after_proc_text_area = document.getElementById('MyTextarea');
                    //after_proc_text_area.value = data[0] + data[1]
                    after_proc_text_area.value = data
                        // console.log(after_proc_text_area);
                })
                .catch(error => {
                    console.error(error);
                });
        };
        eelmineBtn.onclick = function() {
            // Send text data to Flask application
            console.log('eelmine button clicked');
            fetch('/eelmine-text', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        textData: document.getElementById('formated-text').value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    // Update page with processed text data
                    let text = document.getElementById('formated-text');
                    if (text.innerHTML === data) {
                        eelmineBtn.disabled = true;
                    } else {
                        järgmineBtn.disabled = false;
                    }
                    //after_proc_text_area.value = data[0] + data[1]
                    text.innerHTML = data
                        // console.log(after_proc_text_area);
                })
                .catch(error => {
                    console.error(error);
                });
        };
        järgmineBtn.onclick = function() {
            // Send text data to Flask application
            console.log('järgmine button clicked');
            fetch('/järgmine-text', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        textData: document.getElementById('formated-text').value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    // Update page with processed text data
                    let text = document.getElementById('formated-text');
                    if (text.innerHTML === data) {
                        järgmineBtn.disabled = true;
                    } else {
                        eelmineBtn.disabled = false;
                    }
                    console.log(text)
                    //after_proc_text_area.value = data[0] + data[1]
                    text.innerHTML = data
                        // console.log(after_proc_text_area);
                })
                .catch(error => {
                    console.error(error);
                });
        };
    };


    let onError = function(err) {
        console.log('The following error occured: ' + err);
    };

    navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);
} else {
    console.log('getUserMedia not supported on your browser!');
    alert('getUserMedia not supported on your browser!');
}

// this function is copied from
// https://github.com/awslabs/aws-lex-browser-audio-capture/blob/master/lib/worker.js#L46
function downsampleBuffer(buffer, exportSampleRate) {
    if (exportSampleRate === recordSampleRate) {
        return buffer;
    }
    var sampleRateRatio = recordSampleRate / exportSampleRate;
    var newLength = Math.round(buffer.length / sampleRateRatio);
    var result = new Float32Array(newLength);
    var offsetResult = 0;
    var offsetBuffer = 0;
    while (offsetResult < result.length) {
        var nextOffsetBuffer = Math.round((offsetResult + 1) * sampleRateRatio);
        var accum = 0,
            count = 0;
        for (var i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
            accum += buffer[i];
            count++;
        }
        result[offsetResult] = accum / count;
        offsetResult++;
        offsetBuffer = nextOffsetBuffer;
    }
    return result;
};