# ZinChat Demo

This repository provides a minimal proof‑of‑concept for **ZinChat**, a
unified conversational interface bridging humans, AI agents, and IoT
devices.  The goal of ZinChat is to enable natural language
interaction with both people and machines through a single secure
messaging platform.  Although this demo is intentionally simple, it
lays the groundwork for more sophisticated integrations such as
federated messaging, edge AI reasoning, and dynamic encryption (as
outlined in your research plan).

## Features

* **WebSocket chat server**: Built using [FastAPI](https://fastapi.tiangolo.com/), the server hosts a `/ws` endpoint that
  supports real‑time communication between multiple clients.  Messages
  are broadcast to all connected participants.
* **Device command handling**: Messages beginning with the `/device`
  prefix are interpreted as commands for a simulated IoT device.  The
  device simulator returns a response (e.g. a sensor reading or a
  status update) that is sent back to the issuing user.
* **Periodic sensor updates**: A background task emits random sensor
  readings every 10 seconds to all clients, illustrating how device
  telemetry can appear in the chat stream.
* **Self‑contained web client**: Browsing to the root path (`/`)
  presents a simple HTML page that connects to the server via
  WebSocket.  Users can chat and issue device commands directly from
  their browser.

## Running the demo

Ensure you have Python 3.9+ and the required dependencies installed.
If using a virtual environment, activate it first.  Then run:

```bash
uvicorn zinchat.main:app --reload --port 8000
```

Open a browser and navigate to `http://localhost:8000/`.  Open the
page in multiple tabs or windows to see messages broadcast between
clients.  Type `/device status`, `/device start`, or `/device stop`
into the input box to interact with the simulated device.  Every 10
seconds you will see a `Sensor reading: N` message indicating the
device is sending telemetry.

## Extending this prototype

This demo is intended as a starting point.  Possible next steps
include:

* **Federation**: Replace the single server architecture with a
  federated protocol such as Matrix or XMPP to allow cross‑domain
  communication.  Implement the necessary API endpoints and E2EE.
* **Edge reasoning**: Integrate a lightweight language model at the
  edge (e.g. TinyLlama) to interpret natural language commands and
  translate them into device actions.  Use retrieval‑augmented
  generation to combine sensor data with prompts.
* **Security enhancements**: Incorporate your proposed DSEKC protocol
  for dynamic key exchange and fine‑grained encryption choices.  Add
  authentication and authorisation layers.
* **IoT integrations**: Connect real sensors and actuators via
  MQTT/CoAP.  Build gateways on Raspberry Pi or ESP32 devices that
  join the chat via WebSocket or publish telemetry to the server.

We hope this demo helps you iterate on your vision for a
conversational Internet of Everything.  Feel free to adapt and
expand the code to suit your research needs.
