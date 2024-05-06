import asyncio
import base64
import io
import numpy as np
import face_recognition
import json
from PIL import Image
from websockets.server import serve

axel_image = face_recognition.load_image_file("./servidor/frente.jpeg")
axel_face_encoding = face_recognition.face_encodings(axel_image)[0]

known_face_encodings = [axel_face_encoding]
known_face_names = ["Axel"]

async def analizar(websocket):
    async for message in websocket:
        datos = json.loads(message)
        img_general = base64.b64decode(datos["imagen"])
        img = Image.open(io.BytesIO(img_general))

        img = np.array(img)
        face_locations = face_recognition.face_locations(img)
        face_encodings = face_recognition.face_encodings(img, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Desconocido"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            face_names.append(name)
            print(f"Detected {name} at {face_locations}")

        response = []
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            response.append({"result": name, "x": left, "y": top, "w": right - left, "h": bottom - top})

        await websocket.send(json.dumps({"faces": response}))

async def main():
    async with serve(analizar, "", 8000):
        await asyncio.Future()  # This will run forever

asyncio.run(main())
