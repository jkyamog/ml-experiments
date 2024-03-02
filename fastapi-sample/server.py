import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles

load_dotenv() # load the env vars before initializing the pipeline

import pipeline

app = FastAPI()

@app.post('/api/completion')
async def api_completion(request: Request):
    data = await request.body() 
    message_text = data.decode()

    chain = pipeline.make_chain()
    completion = chain.invoke(message_text)

    return completion


@app.websocket('/ws/completion')
async def ws_completion(websocket: WebSocket):
    await websocket.accept()

    try:
        data = await websocket.receive_text()

        chain = pipeline.make_chain()

        async for completion in chain.astream(data):            
            await websocket.send_text(completion) 
        else:
            await websocket.close()

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e: 
        print(f'Error {e}')
        await websocket.send_text('Server Error')
        await websocket.close()


app.mount("/client", StaticFiles(directory="client", html=True), name="frontend")