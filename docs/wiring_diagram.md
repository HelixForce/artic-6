# ARTIC-6 — Wiring Strategy

---

## Changelog — v0.1
- Added two-zone layout (Power Zone vs Logic Zone — 50mm minimum separation)
- Added star grounding requirement — heavy gauge copper bus bar
- Specified opto-isolated relay board (not standard relay)
- Added NC wiring for all 6 limit switches
- Added shielded twisted pair for limit switch runs
- Specified USB port assignment: RealSense → USB3 (blue), Arduino → USB2 (black)
- Added capacitor buffer on relay board 5V input
- Added ferrite bead on Arduino–RPi USB cable
- E-stop wired to 24V hardware rail (not software pin)
- Added staggered relay trigger timing note (50ms delay between each)

---

## Zone Layout

```
┌─────────────────────────────────────────────────────┐
│                   BASE ENCLOSURE                    │
│                                                     │
│  ┌──────────────────┐   50mm+  ┌─────────────────┐ │
│  │   POWER ZONE     │  ──────  │   LOGIC ZONE    │ │
│  │                  │          │                 │ │
│  │  24V 10A PSU     │          │  Raspberry Pi 5 │ │
│  │  6× TMC2209      │          │  Arduino Mega   │ │
│  │  8ch Relay Board │          │  Logic Converter│ │
│  │  Ground Bus Bar  │          │  5V USB-C PSU   │ │
│  └──────────────────┘          └─────────────────┘ │
│                                                     │
│  E-STOP ──────────────────────── 24V MAIN RAIL     │
└─────────────────────────────────────────────────────┘
```

**Rule:** Never bundle 24V motor wires next to 3.3V signal wires.

---

## Power Distribution

```
Wall AC
  │
  ▼
24V 10A PSU ──── E-STOP (hardware, cuts 24V rail entirely)
  │
  ├──► TMC2209 #1 (NEMA 23 — Axis 1, base rotation)
  ├──► TMC2209 #2 (NEMA 23 — Axis 2, shoulder)
  ├──► TMC2209 #3 (NEMA 23 — Axis 3, elbow)
  ├──► TMC2209 #4 (NEMA 17 — Axis 4, wrist pitch)
  ├──► TMC2209 #5 (NEMA 17 — Axis 5, wrist roll)
  └──► TMC2209 #6 (NEMA 17 — Axis 6, gripper)

5V 3A USB-C PSU (dedicated, separate from 24V)
  └──► Raspberry Pi 5 only — never share with motors
```

---

## Star Ground

```
NEMA 23 #1 ground ──┐
NEMA 23 #2 ground ──┤
NEMA 23 #3 ground ──┤
NEMA 17 #4 ground ──┼──► COPPER BUS BAR ──► PSU negative terminal
NEMA 17 #5 ground ──┤    (star ground)
NEMA 17 #6 ground ──┤
Arduino ground ─────┤
RPi ground ─────────┘
```

Never daisy-chain grounds. Motor return current must NOT flow through RPi ground plane.

---

## Signal Chain

```
RPi 5 GPIO (3.3V)
  │
  ▼
Logic Level Converter (bi-directional 3.3V ↔ 5V)
  │
  ▼
Arduino Mega (5V) ──── USB 2.0 (black port) ──── RPi USB hub
  │                    [ferrite bead on cable]
  ├──► STEP/DIR/EN ──► TMC2209 #1–6
  ├──► Limit Switch inputs (6×, NC wired, shielded twisted pair)
  └──► HX711 (load cell amp) → SPI

RealSense D435 ──── USB 3.0 (blue port, direct to RPi) ──── RPi 5
                    [do not share hub with Arduino]
```

---

## Limit Switch Wiring (NC — Fail-Safe)

```
+5V ────────────────┬─────┬─────┬─────┬─────┬─────┐
                    │     │     │     │     │     │
                   SW1   SW2   SW3   SW4   SW5   SW6
                   (NC)  (NC)  (NC)  (NC)  (NC)  (NC)
                    │     │     │     │     │     │
Arduino Pin ───────┼─────┼─────┼─────┼─────┼─────┤
                    │     │     │     │     │     │
                   10k   10k   10k   10k   10k   10k  (pull-down)
                    │     │     │     │     │     │
GND ───────────────┴─────┴─────┴─────┴─────┴─────┘
```

**Logic:**
- Normal state (switch closed): Pin reads HIGH (5V through NC contact)
- Triggered OR wire break: Pin reads LOW (pull-down to GND)
- LOW = STOP immediately — this is fail-safe

---

## EMI Prevention Checklist

- [ ] Ferrite bead on Arduino ↔ RPi USB cable
- [ ] 1000µF cap on each NEMA 23 TMC2209 power input
- [ ] 1000µF cap on relay board 5V input
- [ ] Twist motor wire pairs (A+/A- together, B+/B- together)
- [ ] Shielded twisted pair for all limit switch runs
- [ ] Shield connected to star ground at ONE end only (PSU side)
- [ ] 50mm+ separation between power zone and logic zone
- [ ] RPi powered from dedicated 5V 3A PSU (not buck converter)

---

## E-Stop Wiring

```
24V PSU (+) ─────────┐
                     │
              ┌──────┴──────┐
              │   E-STOP    │  ← 22mm NC mushroom button
              │   (NC)      │
              └──────┬──────┘
                     │
24V RAIL ────────────┘  ← Powers all TMC2209 drivers

When E-STOP pressed:
- 24V rail goes dead instantly
- All motors lose power
- Arm stops (may fall — keep hand nearby)
```

**Important:** E-stop is hardware-level, not software. It physically disconnects 24V regardless of code state.

---

## Relay Board Trigger Timing

When activating multiple relays (e.g., at startup), stagger triggers by 50ms:

```python
# In Arduino or Python
for i in range(6):
    activate_relay(i)
    delay(50)  # ms — prevents inrush current spike
```

This prevents PSU voltage sag from simultaneous relay coil activation.

---

## USB Port Assignment (RPi 5)

| Port | Color | Device | Why |
|------|-------|--------|-----|
| USB 3.0 | Blue | RealSense D435 | High bandwidth (depth + RGB stream) |
| USB 2.0 | Black | Arduino Mega | Low bandwidth (serial commands only) |
| USB 2.0 | Black | USB Microphone | Low bandwidth (audio) |

**Rule:** RealSense must be on USB 3.0 blue port or it will drop frames. Never put Arduino and RealSense on same hub.
