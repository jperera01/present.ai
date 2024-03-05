// (async () => {
let width = 0;
let height = 0;

let streaming = false

let video = null;
let canvas = null;
let context = null
let videoerrorcontainer = null
let ws = null
let recorder = null

async function getUserUser() {
  const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });

  recorder = new MediaRecorder(stream)
  recorder.ondataavailable = async function(e) {
    const data = await e.data.text()
    ws.send(JSON.stringify({
      type: "audio",
      data
    }))
  }

  recorder.onerror = function(e) {
    console.log(e)
  }

  recorder.start(1000)
  video.srcObject = stream;
  video.play();
  console.log(recorder)
}

function startStream() {
  setInterval(() => {

    if (streaming) {
      context.drawImage(video, 0, 0, width, height);
      const frame = canvas.toDataURL('image/jpeg')

      sendFrameToBackend(JSON.stringify({ type: "video", data: frame }))
    }

  }, 100)
}

async function startStreamHandleException() {
  try {
    await getUserUser()


    videoerrorcontainer.style.display = "hidden"

    startStream()
  } catch (err) {
    videoerrorcontainer.style.display = "block"
    // console.log(`An error occurred: ${err}`)
  }
}

async function startup() {
  ws = new WebSocket("ws://localhost:5000/handle-stream")

  video = document.getElementById("video");
  canvas = document.getElementById("canvas")
  videoerrorcontainer = document.getElementById("videoerrorcontainer")

  context = canvas.getContext('2d');

  await startStreamHandleException();

  video.addEventListener(
    "canplay",
    (ev) => {
      if (!streaming) {
        // height = (video.videoHeight / video.videoWidth) * width;

        // video.setAttribute("width", width);
        // video.setAttribute("height", height);

        // canvas.width = width;
        // canvas.height = height;

        streaming = true;
      }
    },
    false
  )
}

async function sendFrameToBackend(frame) {
  ws.send(frame);
}


window.addEventListener("load", startup, false)
// })();
