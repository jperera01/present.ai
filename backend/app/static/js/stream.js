(async () => {
  let width = 620;
  let height = 0;

  let streaming = false

  let video = null;
  let canvas = null;
  let context = null
  let videoerror = null;
  let countdown = null;
  let ws = null

  async function startup() {
    ws = new WebSocket("ws://localhost:5000/handle-stream")

    video = document.getElementById("video");
    canvas = document.getElementById("canvas")
    videoerror = document.getElementById("videoerror")
    countdown = document.getElementById("countdown")

    context = canvas.getContext('2d');
    let timeLeft = 3;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      video.srcObject = stream;
      video.play();

      // setInterval(() => {

      var timerId = setInterval(function() {
        if (streaming) {
          timeLeft--;
          countdown.textContent = timeLeft;
          context.drawImage(video, 0, 0, width, height);
          const frame = canvas.toDataURL('image/jpeg')

          if (timeLeft <= 0) {
            sendFrameToBackend(frame)
            clearInterval(timerId);
          }
        }
      }, 1000);
      // }, 100)


    } catch (err) {
      videoerror.style.display = "block"
      console.log(`An error occurred: ${err}`)
    }

    video.addEventListener(
      "canplay",
      (ev) => {
        if (!streaming) {
          height = (video.videoHeight / video.videoWidth) * width;

          video.setAttribute("width", width);
          video.setAttribute("height", height);

          canvas.width = width;
          canvas.height = height;

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
})();
