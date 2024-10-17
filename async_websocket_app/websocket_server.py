from fastapi import FastAPI, WebSocket  
from fastapi.responses import HTMLResponse  

app = FastAPI()  
clients = []  

@app.get("/")  
async def get():  
    html_content = """  
    <!DOCTYPE html>  
    <html>  
        <head>  
            <title>WebSocket Chat</title>  
        </head>  
        <body>  
            <h1>WebSocket Chat</h1>  
            
            <form action="" onsubmit="sendMessage(event)">  
                <input type="text" id="messageText" autocomplete="off"/>  
                <button>Send</button>  
            </form>  
            <ul id='messages'></ul>  
            <script>  
                var ws = new WebSocket("ws://localhost:8000/ws");  
                ws.onmessage = function(event) {  
                    var messages = document.getElementById('messages');  
                    var message = document.createElement('li');  
                    message.textContent = event.data;  
                    messages.appendChild(message);  
                };  
                function sendMessage(event) {  
                    var input = document.getElementById("messageText");  
                    ws.send(input.value);  
                    input.value = '';  
                    event.preventDefault();  
                }  
            </script>  
        </body>  
    </html>  
    """  
    return HTMLResponse(content=html_content)  

@app.websocket("/ws")  
async def websocket_endpoint(websocket: WebSocket):  
    await websocket.accept()  
    clients.append(websocket)  
    
    try:  
        while True:  
            data = await websocket.receive_text()  
            for client in clients:  
                if client != websocket:  
                    await client.send_text(f"Client says: {data}")  
        
    except Exception as e:  
        print("Client disconnected: ", e)  
    finally:  
        clients.remove(websocket)  
        await websocket.close()