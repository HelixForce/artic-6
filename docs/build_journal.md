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

## Current Status

**Phase 0: Planning** — ✅ Complete

**Phase 1: CAD Design** — 🔄 In Progress
- Fusion 360 student license approved
- Watching Fusion 360 beginner tutorials
- Ready for first CAD session (weekday 3:30pm+)

---

## Next Milestones

- [ ] Push repo to GitHub
- [ ] Apply for GitHub Student Pack
- [ ] Submit Hack Club Blueprint application (deadline March 31)
- [ ] Fusion 360 — base plate sketch (250×250mm, slotted motor holes, thrust bearing seat 24.5mm)
- [ ] Fusion 360 — Link 1 sandwich plate pair (350mm, 40mm apart, standoffs every 100mm)
- [ ] Export DXF files for SendCutSend quote

---

*Future entries will be added as the build progresses*
