# Firmware

Arduino Mega 2560 stepper control code.

---

## Purpose

The Arduino Mega handles real-time stepper pulse generation. It receives high-level motion commands from the Raspberry Pi via USB serial and translates them into precise step/direction signals for the TMC2209 drivers.

---

## Planned Structure

```
firmware/
├── artic6_firmware/
│   ├── artic6_firmware.ino   ← Main Arduino sketch
│   ├── config.h              ← Pin definitions, motor parameters
│   ├── stepper.h             ← Stepper control functions
│   ├── homing.h              ← Limit switch homing routines
│   └── serial_protocol.h     ← Command parsing from RPi
└── README.md                 ← You are here
```

---

## Hardware Connections

| Arduino Pin | Function | Connected To |
|-------------|----------|--------------|
| D2-D7 | STEP signals | TMC2209 #1-6 STEP |
| D8-D13 | DIR signals | TMC2209 #1-6 DIR |
| D22-D27 | EN signals | TMC2209 #1-6 EN |
| D28-D33 | Limit switches | KW11-3Z NC terminals |
| A0 | HX711 DOUT | Load cell amplifier |
| A1 | HX711 SCK | Load cell amplifier |
| Serial (USB) | Commands | Raspberry Pi 5 |

---

## TMC2209 UART Configuration

Each TMC2209 needs UART for StallGuard configuration:
- Use software serial multiplexing (one TX line per driver)
- Set current limit via UART before enabling
- Configure StallGuard threshold for collision detection

---

## Communication Protocol

Commands from RPi (JSON over serial):
```json
{"cmd": "move", "axis": 2, "steps": 1000, "dir": 1, "speed": 500}
{"cmd": "home", "axis": 1}
{"cmd": "grip", "force": 200}
{"cmd": "stop"}
```

Responses to RPi:
```json
{"status": "ok", "position": [0, 1000, 500, 0, 0, 0]}
{"status": "limit", "axis": 2}
{"status": "stall", "axis": 3}
```

---

*Firmware will be developed after mechanical assembly*
