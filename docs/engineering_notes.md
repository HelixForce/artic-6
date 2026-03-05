# ARTIC-6 — Engineering Notes

Lessons learned from design review sessions. Reference this before CAD work or ordering parts.

---

## The "Weight vs. Torque" Trap

This is the most common point of failure for scratch-built arms.

**The Problem:** The upper arm (Link 1) is 350mm long. When fully extended horizontally, the shoulder NEMA 23 must lift the weight of the forearm, wrist, gripper, motors for those joints, AND the 1kg payload.

**The Math:** 
- Torque = Force × Distance
- 1kg payload at 720mm reach creates 7.06Nm of torque
- NEMA 23 produces only 0.79Nm

**The Fix:** 10:1 belt reduction minimum on shoulder and elbow joints.

---

## Structural Rigidity

### Single Plate Problem
3mm aluminum is great for weight, but over 350mm it becomes "springy."

**The Fix:** Sandwich construction — two 3mm plates separated by 40mm aluminum standoffs. This creates a box section that resists torsional twist.

### Standoff Placement
**Critical:** Place standoffs every 100mm minimum, not just at ends.

- A 350mm link with only 2 end standoffs will bow and vibrate
- 4 standoffs = every ~90mm — structurally required
- Think of it like a bridge truss: more connection points = stiffer

---

## CAD-Specific Gotchas

### Thrust Bearing Seat
- 51100 thrust bearing has **24mm OD** (not 26mm as originally assumed)
- CAD seat recess: **24.5mm OD, 0.5mm deep**
- If too deep: rotating part rubs against base plate
- If too shallow: bearing not captured, arm slides off-center

### Slotted Motor Mount Holes
- Slots must move **away from joint center**, not side-to-side
- Need 6mm travel to tension GT2 belt
- Without proper tension: massive backlash (slop)
- Slot dimension: 8mm wide × 14mm long

### Bearing Hole Tolerance
- 608ZZ bearing = 8mm ID/OD
- CAD holes: **8.1mm** (8mm + 0.1mm clearance)
- Bolt clearance: nominal + 0.2mm

### Fully Constrained Sketches
- Every Fusion 360 sketch must be fully constrained (no blue lines)
- Blue lines = dimensions can shift unexpectedly
- Lock down everything before extruding

### D-Flat on Motor Shafts
- 20T pulleys use set screws that need a flat spot
- File a D-flat on NEMA 23 shafts before mounting pulleys
- Without flat: set screw on round surface = pulley slips under load = home position drifts

---

## Thermal Management

### TMC2209 Heat
Running NEMA 23 motors at 2.8A generates serious heat on TMC2209 drivers.

**The Fix:**
- Active cooling (dedicated fan) blowing directly over driver heatsinks
- Ensure motor face makes direct flat contact with aluminum mount
- Aluminum link acts as giant heatsink

### PETG Temperature Limits
- PETG softens at 80°C
- NEMA 23 motors can run at 80°C
- **Never mount PETG directly to NEMA 23** — use aluminum mounts only
- PETG is acceptable for: covers, wrist assembly, gripper body (non-structural)

---

## Cable Management

### Internal Routing Trap
"Fully internal cable routing" is professional but dangerous if not planned.

**The Problem:** As Axis 2 (shoulder) rotates, it pinches or pulls wires from Axis 1 (base).

**The Fix:**
- Create "cable race" — rounded internal path where wire can coil/uncoil like clock spring
- Sharp aluminum edges will saw through silicone insulation over time
- 80-100mm service loop at every joint

### Cable Fatigue
Standard copper wire is not meant to bend thousands of times — it work-hardens and snaps.

**The Fix:**
- Use high-flex silicone wire (rated ≥200°C)
- Maximum bend radius as large as possible in CAD
- Never pinch wire at joints

---

## Sensor Placement

### RealSense Minimum Focus
Intel RealSense D435 has a minimum focus distance of ~200mm.

**The Fix:** Don't mount camera so close to gripper that it can't see what it's picking up. Check in CAD.

### RealSense USB-C Strain
Joint movement can destroy the camera's USB-C port.

**The Fix:** Zip-tie strain relief 20mm from camera body.

---

## Electronics Layout

### Star Ground Bus Bar
Mount copper bus bar as close to 24V PSU as possible.

**In CAD:** Include two M4 holes specifically for bus bar mounting. It's the "center of the universe" for all ground wires.

### Logic Converter Placement
TMC2209 drivers generate EMI noise.

**The Fix:** Place logic level converter and RPi 5 on opposite side of enclosure from TMC2209 drivers. Even 50mm separation prevents ghost signals on GPIO.

---

## PETG Bolt Connections

### Fender Washers
Bolting aluminum to PETG requires fender washers.

**Why:** Over time, vibration causes bolts to "creep" through PETG. Fender washers distribute load.

**CAD:** Make bolt head clearance holes wide enough for fender washers.

### Print Orientation
PETG layers pull apart under bolt tension perpendicular to layers.

**The Fix:** Orient prints so bolt tension is parallel to layer lines, not perpendicular.

---

## Safety

### E-Stop
Must be wired to 24V hardware rail (physically disconnects power), NOT a software pin.

If code freezes, you need hardware-level power cutoff.

### Back-EMF Warning
Moving the arm by hand when unpowered can generate back-EMF that destroys TMC2209 drivers.

**Rule:** Never move arm fast when motors are unpowered.

### Limit Switches — NC Wiring
All switches must be **Normally Closed (NC)**, not Normally Open.

**Why:** If a wire breaks (NC open), the system sees it as "triggered" and stops. With NO wiring, a broken wire looks like "not triggered" — arm drives into floor.

---

## Quick Reference Table

| Issue | Consequence | Fix |
|-------|-------------|-----|
| Single plate over 350mm | Arm flexes/shakes | Sandwich construction |
| NEMA 23 direct drive | Can't lift payload | 10:1 belt reduction |
| PETG motor mounts | Melts at 80°C | Aluminum mounts |
| Standard GT2 belt | Backlash/drift | Steel-core GT2 |
| 608ZZ at base | Fails under axial load | 51100 thrust bearing |
| NO limit switches | Wire break = no stop | NC wiring |
| Fixed motor holes | Can't tension belt | Slotted holes |
| Unlimited Axis 1 rotation | Cables snap | ±170° hard stops |
| Daisy-chain grounds | EMI crashes RPi | Star ground |
| Shared USB hub | RealSense starves Arduino | Separate ports |
| 1/256 microstepping | Kills holding torque | Use 1/16 or 1/32 |
