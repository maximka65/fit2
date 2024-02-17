from fastapi import FastAPI, WebSocket, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.websockets import WebSocketDisconnect
import cv2
import numpy as np

app = FastAPI()

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            # Преобразование байтов в изображение
            nparr = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # Сохраняем одно изображение
            cv2.imwrite('saved_image.jpg', img)
            
            # Отправляем изображение обратно на клиент
            _, img_encoded = cv2.imencode('.jpg', img)
            await websocket.send_bytes(img_encoded.tobytes())

    except WebSocketDisconnect:
        print("Клиент закрыл соединение")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        
@app.get("/")
def read_root():
    return FileResponse('static/index.html')
