(async () => {
  const width = 320;
  const height = 0;

  const streaming = false

  let video = null;
  let canvas = null;
  let context = null

  async function startup() {
    video = document.getElementById("video");
    canvas = document.getElementById("canvas")
    context = canvas.getContext('2d');

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      video.srcObject = stream;
      video.play();

      setInterval(() => {
        context.drawImage(video, 0, 0, canvas.width, canvas.height)
        const frame = canvas.toDataURL('image/jpeg')

        sendFrameToBackend()
      }, 100)


    } catch (err) {
      console.log(`An error occurred: ${err}`)
    }

    video.addEventListener(
      "canplay",
      (ev) => {
        if (!streaming) {
          height = (video.videoHeight / video.videoWidth) * width;

          video.setAttribute("width", width);
          video.setAttribute("height", height);
          streaming = true;
        }
      },
      false
    )
  }

  async function sendFrameToBackend() {
  }


  window.addEventListener("load", startup, false)
})();
