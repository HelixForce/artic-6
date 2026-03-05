# ARTIC-6 — Build Journal

Progress log. Updated as the build moves forward.

---

## March 2026 — Phase 0: Planning & Engineering Review

### Week 1

**Progress:**
- Defined project scope: 6-DOF arm, 720mm reach, 1kg payload, voice-activated
- Researched motor options — decided on NEMA 23/17 + TMC2209 over hobby servos
- Chose local AI stack: Whisper + Ollama + YOLO v8 + ROS2 — zero paid APIs
- Completed full cost worksheet — all-in realistic budget ~$1,215
- Applied for Hack Club Blueprint funding ($380 requested)
- Applied for Fusion 360 student license — **approved same day**
- Created GitHub repository with full BOM, wiring notes, CAD spec

### Engineering Review (Critical Findings)

Ran deep engineering review before touching Fusion 360 or ordering anything.
Key discoveries that changed the design:

| Issue Found | Consequence if ignored | Fix Applied |
|-------------|----------------------|-------------|
| NEMA 23 alone = 0.79Nm, need 7.06Nm | Arm cannot lift itself | 10:1 belt reduction added |
| Single 3mm plate twists over 350mm | Arm flexes and shakes at gripper | Sandwich construction (2 plates + 40mm standoffs) |
| PETG motor mounts soften at 80°C | Motor sinks into mount over time | Aluminum motor mounts |
| Standard GT2 belt stretches | Backlash — gripper position drifts | Steel-core GT2 belts |
| 608ZZ can't handle axial load at base | Base bearing fails under arm weight | Thrust bearing 51100 added to Axis 1 |
| NC vs NO limit switches | Wire breaks = arm drives into floor | All switches wired NC |
| Fixed motor mount holes | Can't tension belt later | Slotted holes in CAD |
| Unlimited rotation on Axis 1 | Internal cables wind up and snap | Hard stop tabs at ±170° in CAD |
| Star ground not planned | Motor noise crashes RPi / sensors | Star ground bus bar added |
| RealSense on shared USB | Bandwidth starves Arduino comms | RealSense → USB3, Arduino → USB2 |

**Lesson learned:** Every hour in planning saved at minimum one rebuild cycle.
The original v0.0 design would have failed at the shoulder immediately.

---

---

## March 4, 2026 — First CAD Session: SendCutSend DXFs + 3D Print Files

### What I Did Today

Generated production-ready DXF files for SendCutSend and my first 3D-printable STL. All aluminum parts are 3mm 6061-T6, cut with laser/waterjet (2D through-cuts only).

### Files Created

| File | Type | What It Is | Order Qty |
|------|------|-----------|-----------|
| `cad/baseplate.dxf` | SendCutSend | 250×250mm base plate — center shaft hole, NEMA 23 motor mount with slotted bolt holes for belt tensioning, cable pass-through, desk mounts, hard stop post, electronics tray holes, thrust bearing collar mount holes | 1× |
| `cad/link1_upper_arm.dxf` | SendCutSend | 350×60mm upper arm plate — dual 608ZZ bearing holes at each pivot, 4 pairs of M5 standoff holes, center cable channel, lightening holes, calibration notches | 2× (sandwich pair) |
| `cad/link2_forearm.dxf` | SendCutSend | 280×50mm forearm plate — same layout as Link 1 but narrower, 3 standoff pairs, RealSense USB-C strain relief slot | 2× (sandwich pair) |
| `cad/thrust_bearing_collar.stl` | 3D Print (PETG) | 44mm collar that captures the 51100 thrust bearing on the baseplate — replaces the 0.5mm recess that laser cutting can't do | 1× |

### Key Design Decisions Made

- **Thrust bearing seat problem solved:** SendCutSend can't cut partial-depth pockets (laser goes all the way through). Designed a 3D-printed PETG collar that bolts on top of the baseplate and captures the 51100 bearing in a 2mm recess. 3× M3 bolt holes match between collar and baseplate.
- **Motor mounts below baseplate:** NEMA 23 body hangs underneath, shaft comes up through 38.5mm pilot hole. 20T pulley on top drives 80T on turntable. Belt center-distance = 65mm, giving 145.8° belt wrap (above 120° minimum).
- **Slotted motor bolt holes:** 4.5×12mm stadium slots give ~7.5mm of travel to tension GT2 belt after assembly. Can't do this after cutting.
- **Link plates use sandwich construction:** Two identical plates spaced 40mm apart with M5 hex standoffs every ~90mm. Creates a rigid box section that resists the torsional twist a single 3mm plate can't handle.
- **Calibration notches on link plates:** 3mm semicircle cuts on bottom edge at 100mm and 250mm from shoulder end — alignment reference during assembly.

### Engineering Audit Results

Wrote and ran a full geometric audit script checking every hole diameter, edge clearance, feature overlap, and SendCutSend manufacturing limits.

**Bugs caught and fixed:**
1. Bearing collar bolt holes were only 1.3mm from outer edge → increased collar OD from 38mm to 44mm (now 4.3mm wall)
2. Calibration notches were 2mm diameter → below SendCutSend's 3mm minimum feature size → increased to 3mm
3. Lightening holes on link plates were sized too large (18mm) to actually fit → reduced to 12mm so they clear edges
4. Original calibration notches were floating inside the plate body instead of cutting the edge → fixed to semicircles on edge

**Final audit: 0 errors, 0 warnings.**

### What I Learned

- SendCutSend is 2D only — no pockets, no depth, everything goes through. Design around this by combining laser-cut plates with 3D-printed adapters.
- The "just put holes 20mm from the edge" advice I got from another AI was wrong. Every hole position needs to be driven by what it's for (motor bolt pattern, bearing spacing, etc.), not an arbitrary margin.
- Running an automated geometry audit before ordering is essential — caught 4 errors I would have paid $130+ to discover.
- Python + ezdxf can generate production-quality DXF files directly. All parameters are changeable at the top of each script — regenerate in seconds.

### What's NOT Done Yet (Don't Order Yet)

- **Shoulder joint brackets** — determine motor mount position on Link 1
- **Elbow joint brackets** — same for Link 2
- **Motor mounts** (6×) — L-brackets, depend on bracket geometry
- **3D assembly verification in Fusion 360** — must import DXFs, extrude, and confirm everything fits in 3D before sending to SendCutSend
- **Belt center-distance confirmation** — need physical pulleys in hand to verify 65mm assumption

### Priority: Order GT2 Pulleys Now

The 20T and 80T aluminum GT2 pulleys ($14 total from AliExpress) need to ship ASAP — 2-4 week delivery. They're needed to confirm belt center-distance before finalizing any DXF that has motor mount holes. Everything else is blocked until CAD is fully assembled in Fusion 360.

---

## Current Status

**Phase 0: Planning** — ✅ Complete

**Phase 1: CAD Design** — 🔄 In Progress
- [x] Base plate DXF generated and audited
- [x] Link 1 upper arm DXF generated and audited
- [x] Link 2 forearm DXF generated and audited
- [x] Thrust bearing collar STL generated
- [x] Imported DXFs into Fusion 360, extruded to 3mm
- [x] Got SendCutSend quote: ~$130 USD
- [ ] Design shoulder joint brackets
- [ ] Design elbow joint brackets
- [ ] Design motor mounts (6×)
- [ ] Full 3D assembly verification in Fusion 360
- [ ] Final SendCutSend order (after brackets + mounts designed)

**Phase 1.5: Firmware** — ✅ v0.1 Complete
- [x] config.h — pin assignments, speeds, accels, joint limits, gear ratios
- [x] stepper.h — AccelStepper wrapper, limit checking, e-stop
- [x] homing.h — limit switch homing (fast approach, back off, slow re-approach)
- [x] serial_protocol.h — plain text command parser (PING, MOVE, HOME, ESTOP, etc.)
- [x] artic6_firmware.ino — main sketch, compiles and ready to upload
- [ ] Upload to Arduino Mega and test serial comms
- [ ] TMC2209 UART configuration (future)

**Phase 2: Parts Ordering** — ⏳ Waiting for funds
- [ ] Order GT2 pulleys from AliExpress (critical path — 2-4 week shipping)
- [ ] Order remaining BOM items
- [ ] Submit SendCutSend order (after CAD fully verified)

---

## March 5, 2026 — Firmware Written + Project Review

### What I Did Today

Wrote the complete v0.1 firmware for the Arduino Mega — 5 files, fully functional stepper control with serial command interface. Also created an interactive arm layout visualization.

### Files Created

| File | What It Is |
|------|-----------|
| `firmware/artic6_firmware/config.h` | All pin assignments, motor speeds, accelerations, joint limits, gear ratios — single file to tune everything |
| `firmware/artic6_firmware/stepper.h` | AccelStepper wrapper — smooth acceleration, joint limit checking, e-stop, enable/disable per axis |
| `firmware/artic6_firmware/homing.h` | Limit switch homing — 3-phase (fast approach → back off → slow re-approach) for each axis |
| `firmware/artic6_firmware/serial_protocol.h` | Command parser — RPi sends text commands like `MOVE 2 45` over USB serial |
| `firmware/artic6_firmware/artic6_firmware.ino` | Main sketch — startup, loop, safety checks |
| `docs/arm_layout_visual.html` | Interactive side-view of assembled arm with movable shoulder/elbow sliders |

### Key Decisions

- **AccelStepper library** chosen for motor control — handles acceleration profiles, no manual timer math
- **Plain text serial protocol** (not JSON) — simpler to debug, type commands directly in Serial Monitor
- **Homing order: shoulder → elbow → base → wrist** — prevents collisions during homing sequence
- **100ms limit switch polling** during motion — safety net catches unexpected triggers
- **All motors disabled on power-up** — arm hangs limp until explicitly enabled, prevents surprises

### What I Learned

- DXF files being "2D" is correct — they're laser cutting profiles, the 3D structure comes from sandwich assembly
- 3mm 6061-T6 aluminum is the right thickness — sandwich construction with 40mm standoffs gives rigidity of much thicker material
- Firmware can be written and tested before any hardware arrives
- The material is 6061-T6 (not 6016 — that's an automotive alloy)

### Project Status Snapshot

- 3D printer arriving Friday
- No parts ordered yet (waiting for funds)
- GT2 pulleys are the critical path item (2-4 week AliExpress shipping)
- Hack Club funding ($380) — won't know until after March 31
- Fusion 360 open, DXFs imported and extruded, but brackets/mounts not designed yet
- Firmware ready to upload the moment an Arduino Mega is in hand

---

## Next Milestones

- [ ] Print thrust bearing collar in PETG (Friday, when printer arrives)
- [ ] Upload firmware to Arduino Mega, test PING/PONG
- [ ] Design shoulder + elbow joint brackets in Fusion 360
- [ ] Design motor mounts in Fusion 360
- [ ] Order GT2 pulleys ASAP (critical path)
- [ ] Get a multimeter
- [ ] Learn soldering basics (YouTube)
- [ ] Write Python serial bridge (RPi → Arduino)
- [ ] Full 3D assembly check in Fusion 360
- [ ] Submit SendCutSend order when funds + CAD ready

---

*Next session: Fusion 360 — design joint brackets and motor mounts*
