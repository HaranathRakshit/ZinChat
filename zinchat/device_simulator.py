"""Device simulator for ZinChat.

This module defines a simple class used to simulate a controllable IoT
device. It can parse commands issued by chat participants and return
human‑readable responses.  In a real deployment, this module would
interface with actual hardware or remote services. Here it is kept
minimal and deterministic for demonstration purposes.

The ``DeviceSimulator.handle_command`` class method takes a command
string (with an optional ``/device`` prefix) and produces a textual
response describing what the device has done or any error message.

"""

from __future__ import annotations

import random
from typing import Any


class DeviceSimulator:
    """A very simple IoT device abstraction.

    The simulator exposes only a handful of commands.  It does not
    maintain state between invocations – each call to ``handle_command``
    is independent.  This makes it suitable for demonstration purposes
    without introducing complex behaviour.
    """

    @staticmethod
    def handle_command(command: str) -> str:
        """Parse a command and return a response.

        Parameters
        ----------
        command:
            The raw command string sent from the chat client.  A
            leading ``/device`` prefix will be removed if present.

        Returns
        -------
        str
            A human‑readable response describing the result of the
            command.  Unknown commands will result in an error message.
        """
        # Normalise and strip any prefix
        cmd = command.strip()
        if cmd.lower().startswith("/device"):
            cmd = cmd[len("/device"):]
        cmd = cmd.strip().lower()

        # Dispatch based on recognised commands
        if cmd == "status":
            value = random.randint(0, 100)
            return f"Current sensor reading is {value}."
        elif cmd == "start":
            return "Device has been started."
        elif cmd == "stop":
            return "Device has been stopped."
        elif not cmd:
            return "No command provided. Try '/device status'."
        else:
            return f"Unknown device command: '{cmd}'."
