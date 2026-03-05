# Firmware

Arduino Mega 2560 stepper control code for the ARTIC-6 robot arm.

---

## Setup Instructions

### 1. Install Arduino IDE
Download from [arduino.cc](https://www.arduino.cc/en/software) — use version 2.x.

### 2. Install AccelStepper Library
In Arduino IDE: **Sketch → Include Library → Manage Libraries** → search **"AccelStepper"** by Mike McCauley → **Install**

### 3. Configure Board
- **Tools → Board → Arduino Mega or Mega 2560**
- **Tools → Processor → ATmega2560**
- **Tools → Port → (your COM port)**

### 4. Upload
Open `artic6_firmware/artic6_firmware.ino` → click Upload (→ button).

### 5. Test
Open **Serial Monitor** (magnifying glass icon), set **115200 baud** and **Newline** line ending:
```
Type: PING
Response: OK PONG
```

---

## File Structure

```
firmware/
├── artic6_firmware/
│   ├── artic6_firmware.ino   ← Main sketch (upload this)
│   ├── config.h              ← Pin definitions, speeds, limits, ratios
│   ├── stepper.h             ← Motor control (AccelStepper wrapper)
│   ├── homing.h              ← Limit switch homing sequences
│   └── serial_protocol.h     ← Command parser (RPi ↔ Arduino)
└── README.md                 ← You are here
```

---

## Serial Command Reference

Send commands from RPi (or Serial Monitor) at 115200 baud. Each command is a line ending with `\n`.

| Command | Example | What It Does |
|---------|---------|-------------|
| `PING` | `PING` | Heartbeat check → responds `OK PONG` |
| `ENABLE` | `ENABLE` | Energize all motors (they hold position) |
| `DISABLE` | `DISABLE` | De-energize all motors (arm goes limp) |
| `HOME` | `HOME` | Home all 6 axes in safe order |
| `HOMEA <axis>` | `HOMEA 2` | Home single axis (1-6) |
| `MOVE <axis> <deg>` | `MOVE 2 45.0` | Move axis to absolute angle |
| `MOVR <axis> <deg>` | `MOVR 3 -10.5` | Move axis by relative amount |
| `MOVA <a1-a6>` | `MOVA 0 45 -30 0 0 0` | Move all 6 axes simultaneously |
| `POS` | `POS` | Report current joint angles |
| `STATUS` | `STATUS` | Report e-stop, homing, motion state |
| `STOP` | `STOP` | Decelerate all axes to stop |
| `ESTOP` | `ESTOP` | Emergency stop (instant, disables motors) |
| `RESET` | `RESET` | Clear e-stop state (re-home required) |

### Typical Startup Sequence
```
PING          → OK PONG
ENABLE        → OK motors enabled
HOME          → OK HOME complete  (takes ~30 seconds)
MOVE 2 45     → OK MOVE 2 → 45.00
POS           → POS 0.00 45.00 0.00 0.00 0.00 0.00
```

### Response Format
- `OK ...` — command succeeded
- `ERR ...` — command failed (reason given)
- `WARN ...` — non-fatal warning (e.g., limit switch hit)
- `POS ...` — position data
- `STATUS ...` — status data

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

## How It Works

1. **On power-up:** All motors are disabled (free-spinning). Firmware waits for commands.
2. **ENABLE:** Motors energize and hold position. Arm is stiff but doesn't know where it is.
3. **HOME:** Each axis slowly moves toward its limit switch, backs off, re-approaches slowly for precision, then moves to a known offset. Now the firmware knows exactly where each joint is.
4. **MOVE:** AccelStepper calculates a smooth acceleration/deceleration profile and generates step pulses. The TMC2209 driver converts each pulse into a motor microstep.
5. **Safety:** Limit switches are checked every 100ms during motion. If one triggers, that axis stops immediately. E-stop cuts all motors.

---

## Tuning Guide

All tunable parameters are in `config.h`:

| Parameter | What to Change | When |
|-----------|---------------|------|
| `MAX_SPEED_x` | Increase for faster motion | If motors don't skip steps |
| `MAX_ACCEL_x` | Increase for snappier response | If motors don't skip steps |
| `MICROSTEPS` | 8→16 for smoother, 8→4 for faster | Trade smoothness vs speed |
| `REDUCTION_x` | Match your actual pulley ratios | After measuring real hardware |
| `HOME_OFFSETS` | Adjust zero position | After assembly |
| `JOINT_MIN/MAX` | Expand/shrink range of motion | After testing physical limits |

**If a motor skips steps** (makes grinding/clicking noise): reduce `MAX_SPEED` and `MAX_ACCEL` for that axis.

---

## Future: TMC2209 UART Configuration

Not yet implemented. Each TMC2209 needs UART for:
- Setting motor current limit (instead of potentiometer)
- StallGuard4 sensorless homing (backup to limit switches)
- CoolStep power savings

This will be added after basic motion works.

---
