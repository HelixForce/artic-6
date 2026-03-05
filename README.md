# ARTIC-6 — Voice-Controlled 6-DOF Robotic Arm

> *"Grab the pen and place it on the laptop without knocking anything over."*
> ARTIC-6 understands that sentence. Then does it.

<br>

![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Phase](https://img.shields.io/badge/Phase-1%20%E2%80%94%20Design-blue)
![Version](https://img.shields.io/badge/Docs-v0.2-yellow)
![License](https://img.shields.io/badge/License-MIT-green)
![Hack Club](https://img.shields.io/badge/Hack%20Club-Blueprint-red)

---

## What is ARTIC-6?

ARTIC-6 is a fully scratch-designed 6-axis robotic arm that understands and executes natural voice commands. No cloud APIs. No subscriptions. Everything runs locally on a home PC and a Raspberry Pi 5.

You say: *"grab the pen, place it on top of the laptop"*
ARTIC-6 hears it, sees the objects in 3D, figures out the moves, and does it.

**This is not a kit. Every part is designed from scratch.**

<br>

## Demo Goal

```
You:     "Grab the pen on the left side of the desk and place it in the cup"
ARTIC-6: [scans desk with depth camera]
         [identifies pen at x:342mm y:180mm z:12mm]
         [calculates joint angles via inverse kinematics]
         [moves arm, grips pen, places in cup]
         [confirms via vision: done]
```

<br>

## Hardware Specs

| Spec | Value | Notes |
|------|-------|-------|
| Degrees of Freedom | 6-DOF | |
| Max Reach | 720mm | |
| Payload Capacity | 1kg | |
| Link 1 (Upper Arm) | 350mm | Sandwich: 2× 3mm 6061 Al plates + 40mm spacers |
| Link 2 (Forearm) | 280mm | Sandwich: 2× 3mm 6061 Al plates + 40mm spacers |
| Wrist + Gripper | 150mm | PETG printed — non load-bearing only |
| Base Footprint | 250 × 250mm | |
| Gripper Opening | 0–80mm parallel jaw | |
| Shoulder Reduction | 10:1 belt minimum | Required — motor alone insufficient |
| Motors (heavy joints) | 3× NEMA 23 + TMC2209 | StallGuard enabled |
| Motors (wrist/gripper) | 3× NEMA 17 + TMC2209 | StealthChop |
| Base Bearing | Thrust bearing 51100 + 608ZZ | Thrust bearing carries vertical arm weight |
| Onboard Computer | Raspberry Pi 5 (4GB) | Executor only — receives JSON from PC |
| Vision | Intel RealSense D435 | USB 3.0 blue port only |
| Force Feedback | Load cell + HX711 | Tare on every empty grip cycle |
| Wiring | Fully internal — zero exposed | NC limit switches, star ground, silicone wire |
| Joint Limits | ±170° Axis 1 | Physical hard stop tabs in CAD |

<br>

## Software Stack — 100% Local, 100% Free

```
Voice
  │
  ▼
Whisper (local STT)
  │
  ▼
Ollama + Llama 3.3  ◄──── Intel RealSense D435 → USB 3.0 (3D object positions)
  │  (LLM brain)           YOLO v8 (object detection)
  │
  ▼
ROS2 + MoveIt2 (IK + motion planning — S-curve accel, velocity scaling)
  │
  ▼
Arduino Mega → USB 2.0 (real-time stepper pulse generation)
  │
  ▼
6× TMC2209 (StallGuard + StealthChop) → 6 stepper motors → ARM MOVES
```

Zero cloud. Zero API keys. Zero monthly cost. Runs on a Ryzen 5 PC + RPi 5.

<br>

## Repository Structure

```
artic-6/
├── README.md               ← you are here
├── MASTER_REFERENCE.md     ← paste into Claude for full context
├── docs/
│   ├── bom.md              ← full bill of materials with ASINs
│   ├── build_journal.md    ← progress log
│   ├── wiring_diagram.md   ← wiring strategy & zone layout
│   ├── engineering_notes.md← lessons learned from design review
│   └── hackclub_application.md
├── cad/                    ← Fusion 360 files + DXF exports
├── firmware/               ← Arduino Mega stepper control
└── software/               ← Python + ROS2 packages
```

<br>

## Current Status

**Phase 0: Planning** — Complete
- Full engineering review done
- Critical issues identified and solutions documented
- BOM finalized with verified ASINs

**Phase 1: CAD Design** — In Progress
- Fusion 360 student license approved
- Next: Base plate → Link 1 → Link 2 → Joint brackets

**Phase 2: Fabrication** — Pending
- SendCutSend for aluminum cutting
- 3D printing for non-structural parts

<br>

## Budget

| Category | Cost |
|----------|------|
| Motors + Drivers | $166 |
| Gear Reduction | $56 |
| Compute + Electronics | $165 |
| Structure + Hardware | $301 |
| Vision + Sensing | $130 |
| Filament | $82 |
| Wiring | $85 |
| **Parts Subtotal** | **$985** |
| Tools, shipping, tax, spares | ~$230 |
| **Realistic All-In** | **~$1,215** |

<br>

## Documentation

- [Bill of Materials](docs/bom.md) — Every part with ASIN, verified specs
- [Build Journal](docs/build_journal.md) — Progress log
- [Wiring Diagram](docs/wiring_diagram.md) — Power zones, star ground, signal chain
- [Engineering Notes](docs/engineering_notes.md) — Lessons learned, gotchas to avoid
- [Master Reference](MASTER_REFERENCE.md) — Paste into Claude for instant context

<br>

## License

MIT License — see [LICENSE](LICENSE)

<br>

## Author

High school student building a robot arm from scratch. Primary build season: June–August 2026.

---

*Built with determination, aluminum, and zero cloud APIs.*
