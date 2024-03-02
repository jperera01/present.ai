(async () => {
  const width = 320;
  const height = 0;

  const streaming = false

  let video = null;

  async function startup() {
    video = document.getElementById("video");

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      video.srcObject = stream;
      video.play();
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


  window.addEventListener("load", startup, false)
})();
