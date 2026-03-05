# Software

Python + ROS2 packages for ARTIC-6 control.

---

## Purpose

This is the "brain" of ARTIC-6. All AI inference runs on the PC, with the Raspberry Pi 5 acting as an executor that forwards commands to the Arduino.

---

## Planned Structure

```
software/
├── voice_pipeline/
│   ├── whisper_stt.py        ← Local speech-to-text
│   └── ollama_brain.py       ← LLM command interpretation
├── vision/
│   ├── realsense_capture.py  ← Depth + RGB from D435
│   ├── yolo_detect.py        ← Object detection
│   └── scene_builder.py      ← 3D scene representation
├── motion/
│   ├── ros2_interface.py     ← ROS2 + MoveIt2 integration
│   └── trajectory_sender.py  ← Send commands to RPi
├── rpi_executor/
│   ├── main.py               ← Runs on RPi 5
│   └── arduino_bridge.py     ← Serial to Arduino Mega
└── README.md                 ← You are here
```

---

## Software Stack

```
Voice
  │
  ▼
Whisper (local STT on PC)
  │
  ▼
Ollama + Llama 3.3 (command interpretation)
  │
  ▼
ROS2 + MoveIt2 (inverse kinematics + motion planning)
  │
  ▼
Python trajectory sender → RPi 5 → Arduino Mega → Motors
```

---

## Dependencies

**PC (Windows 11):**
- Python 3.10+
- Whisper (openai-whisper or faster-whisper)
- Ollama with Llama 3.3 model
- Ultralytics YOLO v8
- pyrealsense2

**Raspberry Pi 5:**
- Python 3.10+
- pyserial
- Flask or FastAPI (for receiving commands from PC)

**Optional (for full ROS2 stack):**
- ROS2 Humble
- MoveIt2

---

## Communication Flow

1. **PC** captures voice → Whisper transcribes
2. **PC** sends text to Ollama → Gets action plan
3. **PC** captures depth frame → YOLO detects objects
4. **PC** calculates trajectory via MoveIt2
5. **PC** sends motion commands to **RPi** (HTTP/WebSocket)
6. **RPi** forwards commands to **Arduino** (USB serial)
7. **Arduino** executes stepper pulses

---

*Software will be developed after firmware is working*
