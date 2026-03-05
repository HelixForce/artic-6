#!/usr/bin/env python3
"""
ARTIC-6 Serial Bridge — RPi 5 ↔ Arduino Mega

Sends plain-text commands over USB serial and parses responses.
Matches firmware serial_protocol.h exactly.

Usage:
    from arduino_bridge import ArmBridge

    arm = ArmBridge()          # auto-detects port
    arm.ping()                 # True if connected
    arm.enable()
    arm.home()
    arm.move(2, 45.0)          # shoulder to 45°
    arm.move_all(0, 45, -30, 0, 0, 0)
    print(arm.get_pos())       # [0.0, 45.0, -30.0, 0.0, 0.0, 0.0]
    arm.estop()
"""

import serial
import serial.tools.list_ports
import time
import threading


class ArmBridge:
    NUM_AXES = 6

    def __init__(self, port=None, baudrate=115200, timeout=2.0):
        if port is None:
            port = self._find_port()
        self._ser = serial.Serial(port, baudrate, timeout=timeout)
        self._lock = threading.Lock()
        time.sleep(2)  # Arduino resets on serial open

    # ---- Auto-detect Arduino Mega ----
    @staticmethod
    def _find_port():
        for p in serial.tools.list_ports.comports():
            desc = (p.description or "").lower()
            vid_pid = (p.hwid or "").upper()
            if "mega" in desc or "2560" in desc or "2341:0042" in vid_pid:
                return p.device
        # Fallback: first available serial port
        ports = list(serial.tools.list_ports.comports())
        if ports:
            return ports[0].device
        raise ConnectionError("No serial port found — is the Arduino plugged in?")

    # ---- Low-level send/receive ----
    def _send(self, cmd, timeout=10.0):
        """Send command, return response line."""
        with self._lock:
            self._ser.reset_input_buffer()
            self._ser.write((cmd.strip() + "\n").encode("ascii"))
            self._ser.flush()
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                line = self._ser.readline().decode("ascii", errors="replace").strip()
                if line:
                    return line
            raise TimeoutError(f"No response to: {cmd}")

    def _send_ok(self, cmd, timeout=10.0):
        """Send command, expect OK response. Raises on ERR."""
        resp = self._send(cmd, timeout)
        if resp.startswith("OK"):
            return resp
        raise RuntimeError(f"Command '{cmd}' failed: {resp}")

    # ---- Commands ----
    def ping(self):
        try:
            return self._send("PING", timeout=3.0) == "OK PONG"
        except (TimeoutError, OSError):
            return False

    def enable(self):
        return self._send_ok("ENABLE")

    def disable(self):
        return self._send_ok("DISABLE")

    def home(self, timeout=120.0):
        """Home all axes. Long timeout — homing takes a while."""
        return self._send_ok("HOME", timeout=timeout)

    def home_axis(self, axis, timeout=60.0):
        """Home single axis (1-6)."""
        if not 1 <= axis <= self.NUM_AXES:
            raise ValueError(f"Axis must be 1-{self.NUM_AXES}")
        return self._send_ok(f"HOMEA {axis}", timeout=timeout)

    def move(self, axis, degrees):
        """Move single axis to absolute angle (1-6)."""
        if not 1 <= axis <= self.NUM_AXES:
            raise ValueError(f"Axis must be 1-{self.NUM_AXES}")
        return self._send_ok(f"MOVE {axis} {degrees:.2f}")

    def move_relative(self, axis, degrees):
        """Move single axis by relative angle (1-6)."""
        if not 1 <= axis <= self.NUM_AXES:
            raise ValueError(f"Axis must be 1-{self.NUM_AXES}")
        return self._send_ok(f"MOVR {axis} {degrees:.2f}")

    def move_all(self, a1, a2, a3, a4, a5, a6):
        """Move all 6 axes to absolute positions."""
        return self._send_ok(f"MOVA {a1:.2f} {a2:.2f} {a3:.2f} {a4:.2f} {a5:.2f} {a6:.2f}")

    def stop(self):
        return self._send_ok("STOP")

    def estop(self):
        return self._send_ok("ESTOP")

    def reset(self):
        """Reset from e-stop. Must re-home after."""
        return self._send_ok("RESET")

    def get_pos(self):
        """Return list of 6 joint positions in degrees."""
        resp = self._send("POS")
        if not resp.startswith("POS"):
            raise RuntimeError(f"Unexpected POS response: {resp}")
        parts = resp.split()[1:]
        return [float(p) for p in parts]

    def get_status(self):
        """Return parsed status dict."""
        resp = self._send("STATUS")
        if not resp.startswith("STATUS"):
            raise RuntimeError(f"Unexpected STATUS response: {resp}")
        status = {}
        for token in resp.split()[1:]:
            if "=" in token:
                k, v = token.split("=", 1)
                if v in ("YES", "NO"):
                    status[k] = v == "YES"
                elif "," in v:
                    status[k] = [float(x) for x in v.split(",")]
                else:
                    status[k] = v
        return status

    def wait_until_idle(self, poll_interval=0.2, timeout=120.0):
        """Block until all axes stop moving."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            st = self.get_status()
            if not st.get("moving", False):
                return True
            time.sleep(poll_interval)
        raise TimeoutError("Arm still moving after timeout")

    def close(self):
        if self._ser and self._ser.is_open:
            self._ser.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# ---- Quick CLI test ----
if __name__ == "__main__":
    import sys

    port = sys.argv[1] if len(sys.argv) > 1 else None
    with ArmBridge(port) as arm:
        print(f"Connected: {arm.ping()}")
        print(f"Status:    {arm.get_status()}")
        print(f"Position:  {arm.get_pos()}")
