# ZinChat Demo

ZinChat is a minimal demo application showcasing a conversational interface
between humans, an AI-backed orchestration layer, and IoT devices.
This project uses [FastAPI](https://fastapi.tiangolo.com/) and
WebSockets to enable real‑time chat between multiple clients and a
simulated IoT device.  It demonstrates how natural language input can
trigger device actions and how devices can respond conversationally.

## Features

- **Real‑time chat:** Clients connect via WebSocket and messages are
  broadcast to all participants.
- **Device commands:** Prefix any message with `/device` to control the
  built‑in simulator.  Supported commands include `status`, `start` and
  `stop`.  Unknown commands result in helpful error messages.
- **Sensor telemetry:** A background task emits a random sensor
  reading every 10 seconds, simulating periodic data from a device.
- **Self‑contained client:** The root route serves a simple web page
  with an input box and message area, so you can test the app without
  writing any frontend code.

## Getting Started

### Prerequisites

Ensure you have **Python 3.9 or higher** installed.  This project
only depends on a few Python packages, listed in `requirements.txt`.

### Installation

Clone this repository and install the dependencies:

```bash
git clone https://github.com/HaranathRakshit/ZinChat.git
cd ZinChat
pip install -r requirements.txt
```

### Running the Application

Start the server with [Uvicorn](https://www.uvicorn.org/) (installed
as a dependency):

```bash
uvicorn zinchat.main:app --reload --port 8000
```

The `--reload` flag enables auto‑reloading during development.

Once running, open your browser and navigate to
`http://localhost:8000` to access the chat interface.  Open multiple
tabs or windows to see messages broadcast between them.

### Using the Demo

In the chat input box:

* Type a message normally to broadcast it to all connected users.
* Prefix a message with `/device` to send a command to the device.
  - `/device status` → returns a random sensor reading.
  - `/device start` → replies that the device has been started.
  - `/device stop`  → replies that the device has been stopped.
  - Any other command after `/device` results in a friendly error.
* Every 10 seconds, the server automatically sends a
  `Sensor reading: N` message, where `N` is a random integer.

This demo is intentionally simple.  It is designed to spark ideas
about building more sophisticated conversational systems that
coordinate multiple devices, edge AI modules, and secure
communications.

## Project Structure

```
ZinChat/
├── README.md            # This file
├── requirements.txt     # Python dependencies
└── zinchat/             # Source code package
    ├── __init__.py
    ├── device_simulator.py  # Simulated IoT device logic
    ├── main.py              # FastAPI server and WebSocket logic
    └── README.md            # Package‑level documentation
```

## Running the App from GitHub

You can run this demo directly from the cloned repository (as shown
above) or using the GitHub web UI's Codespaces if available.  The
essential steps are:

1. Clone the repository locally.
2. Install dependencies using `pip install -r requirements.txt`.
3. Launch the server with `uvicorn zinchat.main:app --reload`.
4. Visit `http://localhost:8000` in your browser.

If you prefer not to install anything locally, you can preview the
repository in a Codespace or container environment that supports
Python.  However, running the app requires Python to be available.

## License

This project is provided for demonstration purposes without any
specific license.  Feel free to adapt it for your own experiments and
research.  Pull requests and suggestions are welcome!
