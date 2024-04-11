(async () => {
  let width = 0;
  let height = 0;

  let streaming = false

  let video = null;
  let canvas = null;
  let context = null
  let videoerrorcontainer = null
  let backend_text = null
  let ws = null

  function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result.split(',')[1]);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }

  async function getUserMedia() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });

    const audioTrack = stream.getAudioTracks()[0];

    const audioStream = new MediaStream([audioTrack]);

    const audioRecorder = new MediaRecorder(audioStream);

    let audioChunks = [];


    audioRecorder.ondataavailable = async function(e) {
      audioChunks.push(e.data)
    }

    audioRecorder.onstop = async function() {
      const audioBlob = new Blob(audioChunks, { type: 'audio/ogg' });

      const reader = new FileReader();

      reader.onload = function() {
        const base64data = reader.result.split(',')[1];

        ws.send(JSON.stringify({ type: 'audio', data: base64data }));
      };

      reader.onerror = function(error) {
        console.error("FileReader error: ", error);
      };

      reader.readAsDataURL(audioBlob);

      console.log("stopped and blob created")

      audioChunks = []
    }

    audioRecorder.onerror = function(e) {
      console.log(e)
    }

    audioRecorder.onstart = function() {
      console.log("started")
    }


    setInterval(() => {
      audioRecorder.stop()

      setTimeout(() => {
        audioRecorder.start()
      }, 1)
    }, 5000)



    audioRecorder.start()
    video.srcObject = stream;
    video.play();
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
      await getUserMedia()

      videoerrorcontainer.style.display = "hidden";

      startStream()
    } catch (err) {
      console.log(err)

      videoerrorcontainer.style.display = "block";

    }
  }

  async function startup() {
    ws = new WebSocket("ws://localhost:5000/handle-stream")

    video = document.getElementById("video");
    canvas = document.getElementById("canvas")
    backend_text = document.getElementById("backend_text")
    videoerrorcontainer = document.getElementById("videoerrorcontainer")

    context = canvas.getContext('2d');

    await startStreamHandleException();

    ws.addEventListener("message", function wsMessageEventHandler(e) {
      backend_text.innerText = e.data
    })

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
    // ws.send(frame);
  }


  window.addEventListener("load", startup, false)
})();
