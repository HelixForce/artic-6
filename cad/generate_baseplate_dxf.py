"""
ARTIC-6 Baseplate DXF Generator for SendCutSend
================================================
Material: 3mm 6061-T6 Aluminum
All features are THROUGH-CUTS (laser/waterjet goes all the way through).

Upload the output .dxf to sendcutsend.com, select:
  - Material: 6061-T6 Aluminum
  - Thickness: 0.118" (3mm)

Run:  python generate_baseplate_dxf.py
"""

import math
import sys
import os

try:
    import ezdxf
except ImportError:
    print("Installing ezdxf...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ezdxf"])
    import ezdxf


# ================================================================
#  PARAMETERS — Change these to adjust the design
# ================================================================

# Plate outer dimensions
PLATE_W = 250.0   # mm
PLATE_H = 250.0   # mm
CX = PLATE_W / 2  # plate center X = 125mm
CY = PLATE_H / 2  # plate center Y = 125mm

# --- Axis 1 center shaft hole ---
# A bolt/shaft passes through here — turntable rotates around it
# Thrust bearing 51100 (10mm bore) sits on the plate surface around this hole
# Bearing capture handled by 3D-printed collar, NOT a pocket (laser can't pocket)
CENTER_HOLE_DIA = 10.5  # mm  (10mm bore + 0.5mm clearance)

# --- Desk mounting holes (4x, near corners) ---
DESK_HOLE_DIA = 5.5     # mm  (M5 bolt clearance)
DESK_HOLE_INSET = 15.0  # mm from plate edge

# --- NEMA 23 motor mount (Axis 1 rotation drive) ---
# Motor hangs BELOW the plate. Shaft comes up through pilot hole.
# 20T pulley on motor shaft drives 80T pulley on turntable via GT2 belt.
# Slotted holes let you slide the motor to tension the belt.
MOTOR_CENTER_DISTANCE = 65.0  # mm from plate center to motor center
MOTOR_ANGLE_DEG = 0.0         # 0° = motor to the right of center
NEMA23_BOLT_SPACING = 47.14   # mm square bolt pattern
NEMA23_PILOT_DIA = 38.5       # mm (centering boss + clearance)
MOTOR_SLOT_WIDTH = 4.5        # mm (M4 clearance)
MOTOR_SLOT_LENGTH = 12.0      # mm total (gives ~7.5mm tensioning travel)

# --- Cable pass-through slot ---
# Routes wires from base electronics up through plate to turntable
CABLE_SLOT_LENGTH = 25.0   # mm
CABLE_SLOT_WIDTH = 8.0     # mm
CABLE_SLOT_X = CX          # centered on plate X
CABLE_SLOT_Y = CY - 30.0   # 30mm below plate center

# --- Ground bus bar mount (2x holes) ---
BUSBAR_HOLE_DIA = 4.5     # mm (M4 clearance)
BUSBAR_X1 = 35.0
BUSBAR_Y = 30.0
BUSBAR_SPACING = 25.0     # mm apart horizontally

# --- Hard stop post hole ---
# A bolt here blocks a tab on the turntable, limiting rotation to ±170°
HARDSTOP_HOLE_DIA = 5.5       # mm (M5)
HARDSTOP_DISTANCE = 40.0      # mm from plate center
HARDSTOP_ANGLE_DEG = 90.0     # degrees (straight up from center)

# --- Electronics tray standoff holes (4x) ---
# For mounting a PCB or electronics bracket with M3 standoffs
ELEC_HOLE_DIA = 3.4  # mm (M3 clearance)
ELEC_HOLES = [
    (30.0, 55.0),
    (90.0, 55.0),
    (30.0, 90.0),
    (90.0, 90.0),
]

# --- Thrust bearing alignment holes (3x) ---
# Small holes around center for a 3D-printed bearing collar to register against
# 51100 thrust bearing OD = 24mm, so these go just outside that radius
BEARING_ALIGN_DIA = 2.5    # mm (for alignment pins/pegs)  -- REMOVED: too small risk
# Actually these should be M3 (3.4mm) for bolting down the bearing collar
BEARING_COLLAR_HOLE_DIA = 3.4  # mm (M3)
BEARING_COLLAR_RADIUS = 16.0   # mm from center (just outside 24mm OD / 2 = 12mm)
BEARING_COLLAR_COUNT = 3        # evenly spaced around center


# ================================================================
#  SLOT DRAWING FUNCTION
# ================================================================

def add_slot(msp, cx, cy, length, width, angle_deg=0):
    """
    Draw a stadium/oblong slot (rounded-end rectangle) as a closed polyline.
    
    cx, cy     = center of slot
    length     = total end-to-end length (including rounded caps)
    width      = total width (diameter of the rounded ends)
    angle_deg  = rotation (0 = horizontal)
    """
    a = (length - width) / 2.0  # half-length of straight section
    r = width / 2.0              # cap radius

    # Points in local coords (horizontal, centered at origin), CCW winding
    # Format: (x, y, bulge)  — bulge=1 means CCW semicircle to next point
    local = [
        (-a,  r, 0),   # top-left      → straight to top-right
        ( a,  r, 1),   # top-right     → CCW semicircle to bottom-right
        ( a, -r, 0),   # bottom-right  → straight to bottom-left
        (-a, -r, 1),   # bottom-left   → CCW semicircle back to top-left
    ]

    # Rotate
    if angle_deg != 0:
        rad = math.radians(angle_deg)
        c, s = math.cos(rad), math.sin(rad)
        local = [(x*c - y*s, x*s + y*c, b) for x, y, b in local]

    # Translate to final position
    pts = [(x + cx, y + cy, b) for x, y, b in local]

    msp.add_lwpolyline(pts, close=True, format='xyb', dxfattribs={'layer': '0'})


# ================================================================
#  BUILD THE DXF
# ================================================================

doc = ezdxf.new('R2010')
doc.units = ezdxf.units.MM
msp = doc.modelspace()

# ---- 1. OUTER PROFILE ----
msp.add_lwpolyline(
    [(0, 0), (PLATE_W, 0), (PLATE_W, PLATE_H), (0, PLATE_H)],
    close=True,
    dxfattribs={'layer': '0'}
)

# ---- 2. CENTER SHAFT HOLE ----
msp.add_circle((CX, CY), radius=CENTER_HOLE_DIA / 2, dxfattribs={'layer': '0'})

# ---- 3. DESK MOUNTING HOLES (4x corners) ----
for x in [DESK_HOLE_INSET, PLATE_W - DESK_HOLE_INSET]:
    for y in [DESK_HOLE_INSET, PLATE_H - DESK_HOLE_INSET]:
        msp.add_circle((x, y), radius=DESK_HOLE_DIA / 2, dxfattribs={'layer': '0'})

# ---- 4. NEMA 23 MOTOR MOUNT ----
# Motor center position
motor_cx = CX + MOTOR_CENTER_DISTANCE * math.cos(math.radians(MOTOR_ANGLE_DEG))
motor_cy = CY + MOTOR_CENTER_DISTANCE * math.sin(math.radians(MOTOR_ANGLE_DEG))

# Pilot hole (motor centering boss passes through from below)
msp.add_circle((motor_cx, motor_cy), radius=NEMA23_PILOT_DIA / 2, dxfattribs={'layer': '0'})

# 4× slotted bolt holes (slots oriented along tensioning direction)
half_bolt = NEMA23_BOLT_SPACING / 2.0
for dx_sign in [-1, 1]:
    for dy_sign in [-1, 1]:
        bolt_x = motor_cx + dx_sign * half_bolt
        bolt_y = motor_cy + dy_sign * half_bolt
        add_slot(msp, bolt_x, bolt_y, MOTOR_SLOT_LENGTH, MOTOR_SLOT_WIDTH, MOTOR_ANGLE_DEG)

# ---- 5. CABLE PASS-THROUGH SLOT ----
add_slot(msp, CABLE_SLOT_X, CABLE_SLOT_Y, CABLE_SLOT_LENGTH, CABLE_SLOT_WIDTH, angle_deg=0)

# ---- 6. GROUND BUS BAR HOLES (2x) ----
msp.add_circle((BUSBAR_X1, BUSBAR_Y), radius=BUSBAR_HOLE_DIA / 2, dxfattribs={'layer': '0'})
msp.add_circle((BUSBAR_X1 + BUSBAR_SPACING, BUSBAR_Y), radius=BUSBAR_HOLE_DIA / 2, dxfattribs={'layer': '0'})

# ---- 7. HARD STOP POST HOLE ----
hs_x = CX + HARDSTOP_DISTANCE * math.cos(math.radians(HARDSTOP_ANGLE_DEG))
hs_y = CY + HARDSTOP_DISTANCE * math.sin(math.radians(HARDSTOP_ANGLE_DEG))
msp.add_circle((hs_x, hs_y), radius=HARDSTOP_HOLE_DIA / 2, dxfattribs={'layer': '0'})

# ---- 8. ELECTRONICS TRAY STANDOFF HOLES (4x) ----
for ex, ey in ELEC_HOLES:
    msp.add_circle((ex, ey), radius=ELEC_HOLE_DIA / 2, dxfattribs={'layer': '0'})

# ---- 9. THRUST BEARING COLLAR MOUNT HOLES (3x) ----
# These bolt down the 3D-printed collar that captures the 51100 thrust bearing
for i in range(BEARING_COLLAR_COUNT):
    angle = math.radians(i * 360.0 / BEARING_COLLAR_COUNT + 30)  # offset 30° so they don't collide with cable slot
    bx = CX + BEARING_COLLAR_RADIUS * math.cos(angle)
    by = CY + BEARING_COLLAR_RADIUS * math.sin(angle)
    msp.add_circle((bx, by), radius=BEARING_COLLAR_HOLE_DIA / 2, dxfattribs={'layer': '0'})


# ================================================================
#  SAVE + SUMMARY
# ================================================================

output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, "baseplate.dxf")
doc.saveas(output_path)

# Print summary
print()
print("=" * 60)
print("  ARTIC-6 BASEPLATE — DXF GENERATED")
print("=" * 60)
print(f"  File:     {output_path}")
print(f"  Plate:    {PLATE_W} x {PLATE_H} mm")
print(f"  Material: 3mm 6061-T6 Aluminum")
print()
print("  FEATURES (all through-cuts):")
print(f"    Outer profile:       {PLATE_W}x{PLATE_H}mm rectangle")
print(f"    Center shaft hole:   {CENTER_HOLE_DIA}mm dia at ({CX}, {CY})")
print(f"    Desk mount holes:    4x {DESK_HOLE_DIA}mm dia, {DESK_HOLE_INSET}mm from edges")
print(f"    Motor pilot hole:    {NEMA23_PILOT_DIA}mm dia at ({motor_cx:.1f}, {motor_cy:.1f})")
print(f"    Motor bolt slots:    4x {MOTOR_SLOT_WIDTH}x{MOTOR_SLOT_LENGTH}mm on {NEMA23_BOLT_SPACING}mm pattern")
print(f"    Cable slot:          {CABLE_SLOT_WIDTH}x{CABLE_SLOT_LENGTH}mm at ({CABLE_SLOT_X:.0f}, {CABLE_SLOT_Y:.0f})")
print(f"    Bus bar holes:       2x {BUSBAR_HOLE_DIA}mm dia")
print(f"    Hard stop post:      {HARDSTOP_HOLE_DIA}mm dia at ({hs_x:.1f}, {hs_y:.1f})")
print(f"    Electronics holes:   4x {ELEC_HOLE_DIA}mm dia")
print(f"    Bearing collar:      3x {BEARING_COLLAR_HOLE_DIA}mm dia at R={BEARING_COLLAR_RADIUS}mm from center")
print()
print("  UPLOAD TO SENDCUTSEND:")
print("    1. Go to sendcutsend.com")
print("    2. Upload baseplate.dxf")
print("    3. Material: 6061-T6 Aluminum")
print("    4. Thickness: 0.118\" (3mm)")
print("    5. Quantity: 1")
print()
print("  NOTES:")
print("    - Motor mounts BELOW the plate (shaft comes up through pilot hole)")
print("    - Thrust bearing 51100 sits on TOP of plate, held by 3D-printed collar")
print("    - Collar bolts through the 3x bearing collar holes")
print("    - Belt runs on top between 20T (motor) and 80T (turntable) pulleys")
print("    - Hard stop post limits turntable rotation to ~±170°")
print("=" * 60)
