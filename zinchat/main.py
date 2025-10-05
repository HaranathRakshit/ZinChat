"""Main entry point for the ZinChat demo application.

This module defines a minimal chat server built atop FastAPI and its
WebSocket support.  Clients connect via a WebSocket endpoint and
exchange text messages.  The server supports two primary use cases:

* Human to human chat – messages are broadcast to all connected
  clients.
* Human to device commands – messages starting with the ``/device``
  prefix are routed to a simple device simulator; the simulator
  returns a response that is sent only to the issuing client.

Additionally, a background task runs on startup to periodically send
simulated sensor readings from the device back to all connected
clients.  This demonstrates how data flowing from IoT devices can
appear seamlessly within the same conversational interface.

To run the server locally:

    uvicorn zinchat.main:app --reload --port 8000

Then browse to http://localhost:8000/ to open the basic web client.
"""

from __future__ import annotations

import asyncio
import random
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from .device_simulator import DeviceSimulator

app = FastAPI(title="ZinChat Demo")

# Store connected client WebSocket references
connected_clients: List[WebSocket] = []


@app.get("/")
def root() -> HTMLResponse:
    """Serve a simple HTML client for demonstration purposes.

    This function returns a minimal webpage containing a text area
    displaying chat messages, an input box, and a button to send
    messages.  It connects to the WebSocket endpoint at ``/ws`` and
    streams incoming messages to the page.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>ZinChat Demo</title>
        <style>
            body { font-family: sans-serif; margin: 40px; }
            #chat { border: 1px solid #ccc; padding: 10px; height: 300px;
                    overflow-y: scroll; margin-bottom: 10px; }
            #messageInput { width: 80%; padding: 8px; }
            #sendButton { padding: 8px 12px; }
        </style>
    </head>
    <body>
        <h1>Welcome to ZinChat</h1>
        <p>Type your messages below. To send a device command, prefix the
        message with <code>/device</code>, e.g. <code>/device status</code>.
        </p>
        <div id="chat"></div>
        <input id="messageInput" type="text" placeholder="Enter message..." />
        <button id="sendButton">Send</button>
        <script>
            const chatDiv = document.getElementById('chat');
            const input = document.getElementById('messageInput');
            const button = document.getElementById('sendButton');
            const wsUrl = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws';
            const socket = new WebSocket(wsUrl);
            socket.onmessage = function(event) {
                const msgElem = document.createElement('div');
                msgElem.textContent = event.data;
                chatDiv.appendChild(msgElem);
                chatDiv.scrollTop = chatDiv.scrollHeight;
            };
            button.onclick = function() {
                const text = input.value.trim();
                if (text) {
                    socket.send(text);
                    input.value = '';
                }
            };
            // Allow sending with Enter key
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    button.click();
                    e.preventDefault();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """Handle incoming WebSocket connections.

    Newly connected clients are added to the global list.  Incoming
    messages are inspected: commands prefixed with ``/device`` are
    processed via the device simulator and the result is sent back to
    the sender; other messages are broadcast to every other connected
    client.  When a client disconnects, it is removed from the list.
    """
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.strip().lower().startswith("/device"):
                # Send the command to the device simulator and respond
                response = DeviceSimulator.handle_command(data)
                await websocket.send_text(f"Device ➤ {response}")
            else:
                # Broadcast the message to all other connected clients
                broadcast_text = f"User ➤ {data}"
                for client in connected_clients:
                    if client is not websocket:
                        try:
                            await client.send_text(broadcast_text)
                        except WebSocketDisconnect:
                            # Remove clients that have closed unexpectedly
                            if client in connected_clients:
                                connected_clients.remove(client)
    except WebSocketDisconnect:
        if websocket in connected_clients:
            connected_clients.remove(websocket)


async def device_sensor_broadcast() -> None:
    """Background task to periodically emit sensor data to clients.

    Every 10 seconds this coroutine generates a random integer and
    broadcasts it as a sensor reading to all connected clients.  In a
    real application this function would interface with actual device
    hardware or other data sources.
    """
    while True:
        await asyncio.sleep(10)
        sensor_value = random.randint(0, 100)
        message = f"Sensor reading: {sensor_value}"
        for client in list(connected_clients):
            try:
                await client.send_text(message)
            except WebSocketDisconnect:
                if client in connected_clients:
                    connected_clients.remove(client)


@app.on_event("startup")
async def startup_event() -> None:
    """Launch background tasks on server start."""
    # Schedule the periodic sensor broadcast
    asyncio.create_task(device_sensor_broadcast())
