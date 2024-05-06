const video = document.getElementById('video');
const canvas = document.getElementById('canvas');

const ws = new WebSocket('ws://localhost:8000');


async function activarCamara() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    window.stream = stream;
    video.srcObject = stream;
  } catch (e) {
    console.error('navigator.getUserMedia error:', e);
  }

}

// stream de la camara
function capturar() {
  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, 640, 480);
  let data = canvas.toDataURL('image/jpeg', 0.8);
  data = data.replace('data:image/jpeg;base64,', '');
  const message = JSON.stringify({ imagen: data });
  ws.send(message);
}

ws.onopen = function () {
  console.log('Conectado al servidor');
};

ws.onmessage = function (event) {
  const context = canvas.getContext('2d');
  const faces = JSON.parse(event.data).faces;
  faces.forEach(face => {
    context.beginPath();
    context.rect(face.x, face.y, face.w, face.h);
    context.lineWidth = 5;
    context.strokeStyle = face.result === 'Axel' ? 'green' : 'red';
    context.font = '30px Arial';
    context.fillStyle = 'white';
    context.fillText(face.result, face.x, face.y - 10);
    context.stroke();
  });
}

activarCamara();

setInterval(capturar, 500);