# CAD Files

This folder will contain Fusion 360 project files and DXF exports for SendCutSend.

---

## Planned Files

After Fusion 360 design sessions:

```
cad/
├── artic6.f3d              ← Main Fusion 360 project file
├── base_plate.dxf          ← 250×250mm, thrust bearing seat, slotted motor holes
├── link1_upper_arm.dxf     ← 350mm sandwich plate (make 2)
├── link2_forearm.dxf       ← 280mm sandwich plate (make 2)
├── joint_brackets.dxf      ← Shoulder + elbow pivots
├── motor_mounts.dxf        ← Aluminum L-brackets with slotted holes
└── screenshots/            ← Progress images for documentation
```

---

## CAD Session Order

1. **Base plate** — 250×250mm, slotted NEMA 23 holes, thrust bearing seat (24.5mm OD, 0.5mm deep), cable slot, PSU/electronics mounts, fan bracket, hard stop tabs
2. **Link 1 sandwich plates** (make 2 identical) — 350mm, 8mm pivot holes, M5 standoff holes every 100mm, cable channel, calibration marks at 100mm + 250mm
3. **Link 2 sandwich plates** (make 2 identical) — 280mm, same approach, RealSense strain relief slot
4. **Joint brackets** — shoulder + elbow pivots, hard stop tabs integrated
5. **Motor mounts** — aluminum L-brackets, slotted holes, NEMA 23 bolt pattern (47mm bolt circle, 4× M4)

---

## Key Constraints

| Feature | Dimension | Notes |
|---------|-----------|-------|
| Bearing holes | 8.1mm | 8mm + 0.1mm clearance |
| Bolt clearance | nominal + 0.2mm | |
| Slotted holes | 8mm × 14mm | For belt tensioning |
| Thrust bearing seat | 24.5mm OD, 0.5mm deep | NOT 26mm |
| Standoff spacing | Every 100mm max | Prevents bowing |
| Hard stop tabs | ±170° | Prevents cable wind-up |

---

## Exporting for SendCutSend

1. In Fusion 360: Right-click face → "Create Sketch"
2. File → Export → DXF
3. Upload to sendcutsend.com
4. Select: 3mm 6061-T6 Aluminum
5. Get instant quote

---

*CAD files will be added as design progresses*
