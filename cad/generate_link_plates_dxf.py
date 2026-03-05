"""
ARTIC-6 Link Plate DXF Generator for SendCutSend
=================================================
Generates:
  - link1_upper_arm.dxf  (350mm, order 2x)
  - link2_forearm.dxf    (280mm, order 2x)

Material: 3mm 6061-T6 Aluminum
Sandwich construction: 2 identical plates + 40mm hex standoffs between them.

Run:  python generate_link_plates_dxf.py
"""

import math
import sys
import os

try:
    import ezdxf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ezdxf"])
    import ezdxf


# ================================================================
#  SLOT DRAWING FUNCTION
# ================================================================

def add_slot(msp, cx, cy, length, width, angle_deg=0):
    """Stadium/oblong slot (rounded-end rectangle) as a closed polyline."""
    a = (length - width) / 2.0
    r = width / 2.0
    local = [
        (-a,  r, 0),
        ( a,  r, 1),
        ( a, -r, 0),
        (-a, -r, 1),
    ]
    if angle_deg != 0:
        rad = math.radians(angle_deg)
        c, s = math.cos(rad), math.sin(rad)
        local = [(x*c - y*s, x*s + y*c, b) for x, y, b in local]
    pts = [(x + cx, y + cy, b) for x, y, b in local]
    msp.add_lwpolyline(pts, close=True, format='xyb', dxfattribs={'layer': '0'})


def add_rounded_rect(msp, x, y, w, h, r):
    """Rounded-corner rectangle as a closed polyline with bulge arcs."""
    # Bulge for 90° arc: tan(angle/4) = tan(pi/8) ≈ 0.4142
    b = math.tan(math.pi / 8)
    pts = [
        (x + r,     y,         b),   # bottom-left arc start  → bottom-right arc start
        (x + w - r, y,         0),
        (x + w,     y + r,     b),   # bottom-right arc       → top-right arc start
        (x + w,     y + h - r, 0),
        (x + w - r, y + h,     b),   # top-right arc          → top-left arc start
        (x + r,     y + h,     0),
        (x,         y + h - r, b),   # top-left arc           → bottom-left
        (x,         y + r,     0),
    ]
    msp.add_lwpolyline(pts, close=True, format='xyb', dxfattribs={'layer': '0'})


# ================================================================
#  COMMON PARAMETERS
# ================================================================

# Bearing holes — 608ZZ (8mm ID, 22mm OD, 7mm thick)
# Two bearings spaced apart at each joint for tilt resistance
BEARING_HOLE_DIA = 8.1         # mm (8mm + 0.1mm clearance for press/slide fit)
BEARING_SPACING = 30.0         # mm between the two bearing holes at each end (center-to-center)

# Standoff holes — M5 hex standoffs connect the two plates 40mm apart
STANDOFF_HOLE_DIA = 5.2        # mm (M5 + 0.2mm clearance)

# Cable channel — through-slot for routing wires along the link interior
CABLE_SLOT_WIDTH = 10.0        # mm
CABLE_SLOT_CORNER_R = 3.0      # mm rounded ends (min feature for 3mm material)

# Lightening holes — optional weight reduction (keeps rigidity between standoffs)
LIGHTEN_HOLE_DIA = 12.0        # mm — sized to fit between cable slot and plate edge
LIGHTEN_ENABLED = True

# Corner radius on plate outline
PLATE_CORNER_R = 4.0           # mm — no sharp corners to snag cables or cut hands

# Calibration notches — small semicircle cuts on edge for alignment during assembly
NOTCH_WIDTH = 3.0              # mm (SendCutSend minimum feature = 3mm)
NOTCH_DEPTH = 1.5              # mm


# ================================================================
#  LINK 1 — UPPER ARM (350mm)
# ================================================================

L1_LENGTH = 350.0   # mm
L1_WIDTH = 60.0     # mm — wide enough for dual bearing holes + cable channel
L1_CX = L1_LENGTH / 2.0
L1_CY = L1_WIDTH / 2.0

# Pivot bearing holes — two 608ZZ bearings at each end, spaced apart for rigidity
# Bottom pivot = shoulder joint, Top pivot = elbow joint
L1_PIVOT_INSET = 18.0  # mm from plate end to bearing center

# Standoff positions along the length (every ~87mm = 4 standoffs between pivots)
# Two columns of standoffs, symmetric about centerline
L1_STANDOFF_Y_OFFSET = 20.0   # mm from centerline (so 40mm apart = matches plate width nicely)
L1_STANDOFF_POSITIONS_X = []   # auto-calculated below

# Calculate standoff X positions: evenly spaced, starting after bottom pivot, ending before top pivot
_l1_start = L1_PIVOT_INSET + 15.0   # clear of pivot area
_l1_end = L1_LENGTH - L1_PIVOT_INSET - 15.0
_l1_n_standoffs = 4  # number of standoff pairs along length
for i in range(_l1_n_standoffs):
    _x = _l1_start + i * (_l1_end - _l1_start) / (_l1_n_standoffs - 1)
    L1_STANDOFF_POSITIONS_X.append(_x)

# Cable channel — runs down the center between standoff columns
L1_CABLE_SLOT_X_START = _l1_start + 20.0
L1_CABLE_SLOT_X_END = _l1_end - 20.0
L1_CABLE_SLOT_LENGTH = L1_CABLE_SLOT_X_END - L1_CABLE_SLOT_X_START

# Calibration notch positions (edge marks for alignment reference)
L1_NOTCH_POSITIONS = [100.0, 250.0]  # from docs: calibration marks at 100mm + 250mm


# ================================================================
#  LINK 2 — FOREARM (280mm)
# ================================================================

L2_LENGTH = 280.0   # mm
L2_WIDTH = 50.0     # mm — slightly narrower (lighter loads)
L2_CX = L2_LENGTH / 2.0
L2_CY = L2_WIDTH / 2.0

L2_PIVOT_INSET = 16.0  # mm from plate end to bearing center

# Standoff positions (3 pairs between pivots — every ~93mm)
L2_STANDOFF_Y_OFFSET = 16.0
L2_STANDOFF_POSITIONS_X = []

_l2_start = L2_PIVOT_INSET + 15.0
_l2_end = L2_LENGTH - L2_PIVOT_INSET - 15.0
_l2_n_standoffs = 3
for i in range(_l2_n_standoffs):
    _x = _l2_start + i * (_l2_end - _l2_start) / (_l2_n_standoffs - 1)
    L2_STANDOFF_POSITIONS_X.append(_x)

L2_CABLE_SLOT_X_START = _l2_start + 15.0
L2_CABLE_SLOT_X_END = _l2_end - 15.0
L2_CABLE_SLOT_LENGTH = L2_CABLE_SLOT_X_END - L2_CABLE_SLOT_X_START

# RealSense strain relief slot — near the top (elbow end → wrist)
# A small slot for zip-tie strain relief of the USB-C cable
L2_STRAIN_RELIEF_X = L2_LENGTH - L2_PIVOT_INSET - 30.0  # 30mm below top pivot
L2_STRAIN_RELIEF_WIDTH = 4.0    # mm wide
L2_STRAIN_RELIEF_LENGTH = 12.0  # mm long


# ================================================================
#  GENERATE LINK 1 DXF
# ================================================================

def generate_link1():
    doc = ezdxf.new('R2010')
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()

    # ---- Outer profile (rounded rectangle) ----
    add_rounded_rect(msp, 0, 0, L1_LENGTH, L1_WIDTH, PLATE_CORNER_R)

    # ---- Bottom pivot (shoulder joint) — 2× bearing holes ----
    bx = L1_PIVOT_INSET
    msp.add_circle((bx, L1_CY - BEARING_SPACING / 2), radius=BEARING_HOLE_DIA / 2,
                    dxfattribs={'layer': '0'})
    msp.add_circle((bx, L1_CY + BEARING_SPACING / 2), radius=BEARING_HOLE_DIA / 2,
                    dxfattribs={'layer': '0'})

    # ---- Top pivot (elbow joint) — 2× bearing holes ----
    tx = L1_LENGTH - L1_PIVOT_INSET
    msp.add_circle((tx, L1_CY - BEARING_SPACING / 2), radius=BEARING_HOLE_DIA / 2,
                    dxfattribs={'layer': '0'})
    msp.add_circle((tx, L1_CY + BEARING_SPACING / 2), radius=BEARING_HOLE_DIA / 2,
                    dxfattribs={'layer': '0'})

    # ---- Standoff holes (2 columns × N positions) ----
    for sx in L1_STANDOFF_POSITIONS_X:
        for sy_sign in [-1, 1]:
            sy = L1_CY + sy_sign * L1_STANDOFF_Y_OFFSET
            msp.add_circle((sx, sy), radius=STANDOFF_HOLE_DIA / 2,
                           dxfattribs={'layer': '0'})

    # ---- Cable channel (center slot) ----
    cable_cx = (L1_CABLE_SLOT_X_START + L1_CABLE_SLOT_X_END) / 2.0
    add_slot(msp, cable_cx, L1_CY, L1_CABLE_SLOT_LENGTH, CABLE_SLOT_WIDTH, angle_deg=0)

    # ---- Lightening holes (between standoffs, offset from cable slot) ----
    if LIGHTEN_ENABLED and len(L1_STANDOFF_POSITIONS_X) >= 2:
        for i in range(len(L1_STANDOFF_POSITIONS_X) - 1):
            mid_x = (L1_STANDOFF_POSITIONS_X[i] + L1_STANDOFF_POSITIONS_X[i + 1]) / 2.0
            # Two lightening holes per bay, one above and one below cable slot
            for y_off in [-14.0, 14.0]:
                ly = L1_CY + y_off
                # Only add if hole stays inside plate with 4mm margin
                if ly - LIGHTEN_HOLE_DIA / 2 > 4.0 and ly + LIGHTEN_HOLE_DIA / 2 < L1_WIDTH - 4.0:
                    msp.add_circle((mid_x, ly), radius=LIGHTEN_HOLE_DIA / 2,
                                   dxfattribs={'layer': '0'})

    # ---- Calibration notches (small semicircle cuts on bottom edge) ----
    for nx in L1_NOTCH_POSITIONS:
        # Small semicircle on bottom edge — marks 100mm and 250mm from shoulder pivot
        # Laser will cut this as part of the outer profile
        msp.add_circle((nx, 0.0), radius=NOTCH_WIDTH / 2.0,
                       dxfattribs={'layer': '0'})

    return doc


# ================================================================
#  GENERATE LINK 2 DXF
# ================================================================

def generate_link2():
    doc = ezdxf.new('R2010')
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()

    # ---- Outer profile (rounded rectangle) ----
    add_rounded_rect(msp, 0, 0, L2_LENGTH, L2_WIDTH, PLATE_CORNER_R)

    # ---- Bottom pivot (elbow joint) — 2× bearing holes ----
    bx = L2_PIVOT_INSET
    msp.add_circle((bx, L2_CY - BEARING_SPACING / 2), radius=BEARING_HOLE_DIA / 2,
                    dxfattribs={'layer': '0'})
    msp.add_circle((bx, L2_CY + BEARING_SPACING / 2), radius=BEARING_HOLE_DIA / 2,
                    dxfattribs={'layer': '0'})

    # ---- Top pivot (wrist joint) — 2× bearing holes ----
    tx = L2_LENGTH - L2_PIVOT_INSET
    msp.add_circle((tx, L2_CY - BEARING_SPACING / 2), radius=BEARING_HOLE_DIA / 2,
                    dxfattribs={'layer': '0'})
    msp.add_circle((tx, L2_CY + BEARING_SPACING / 2), radius=BEARING_HOLE_DIA / 2,
                    dxfattribs={'layer': '0'})

    # ---- Standoff holes (2 columns × N positions) ----
    for sx in L2_STANDOFF_POSITIONS_X:
        for sy_sign in [-1, 1]:
            sy = L2_CY + sy_sign * L2_STANDOFF_Y_OFFSET
            msp.add_circle((sx, sy), radius=STANDOFF_HOLE_DIA / 2,
                           dxfattribs={'layer': '0'})

    # ---- Cable channel (center slot) ----
    cable_cx = (L2_CABLE_SLOT_X_START + L2_CABLE_SLOT_X_END) / 2.0
    add_slot(msp, cable_cx, L2_CY, L2_CABLE_SLOT_LENGTH, CABLE_SLOT_WIDTH, angle_deg=0)

    # ---- Lightening holes ----
    if LIGHTEN_ENABLED and len(L2_STANDOFF_POSITIONS_X) >= 2:
        for i in range(len(L2_STANDOFF_POSITIONS_X) - 1):
            mid_x = (L2_STANDOFF_POSITIONS_X[i] + L2_STANDOFF_POSITIONS_X[i + 1]) / 2.0
            for y_off in [-12.0, 12.0]:
                ly = L2_CY + y_off
                if ly - LIGHTEN_HOLE_DIA / 2 > 4.0 and ly + LIGHTEN_HOLE_DIA / 2 < L2_WIDTH - 4.0:
                    msp.add_circle((mid_x, ly), radius=LIGHTEN_HOLE_DIA / 2,
                                   dxfattribs={'layer': '0'})

    # ---- RealSense strain relief slot ----
    add_slot(msp, L2_STRAIN_RELIEF_X, L2_CY,
             L2_STRAIN_RELIEF_LENGTH, L2_STRAIN_RELIEF_WIDTH, angle_deg=90)

    return doc


# ================================================================
#  SAVE + SUMMARY
# ================================================================

output_dir = os.path.dirname(os.path.abspath(__file__))

# Link 1
doc1 = generate_link1()
path1 = os.path.join(output_dir, "link1_upper_arm.dxf")
doc1.saveas(path1)

# Link 2
doc2 = generate_link2()
path2 = os.path.join(output_dir, "link2_forearm.dxf")
doc2.saveas(path2)

print()
print("=" * 65)
print("  ARTIC-6 LINK PLATES — DXFs GENERATED")
print("=" * 65)
print()
print("  LINK 1 — UPPER ARM")
print(f"    File:       {path1}")
print(f"    Dimensions: {L1_LENGTH} x {L1_WIDTH} mm")
print(f"    Order:      2× identical plates (sandwich with 40mm standoffs)")
print(f"    Pivot holes: 2× {BEARING_HOLE_DIA}mm at each end ({BEARING_SPACING}mm apart)")
print(f"    Standoffs:   {len(L1_STANDOFF_POSITIONS_X)} pairs of M5 holes")
print(f"                 X positions: {[f'{x:.1f}' for x in L1_STANDOFF_POSITIONS_X]}")
print(f"    Cable slot:  {CABLE_SLOT_WIDTH}x{L1_CABLE_SLOT_LENGTH:.0f}mm center channel")
print(f"    Lightening:  {'Yes' if LIGHTEN_ENABLED else 'No'} — {LIGHTEN_HOLE_DIA}mm holes between bays")
print(f"    Cal marks:   Notches at {L1_NOTCH_POSITIONS}mm from shoulder end")
print()
print("  LINK 2 — FOREARM")
print(f"    File:       {path2}")
print(f"    Dimensions: {L2_LENGTH} x {L2_WIDTH} mm")
print(f"    Order:      2× identical plates (sandwich with 40mm standoffs)")
print(f"    Pivot holes: 2× {BEARING_HOLE_DIA}mm at each end ({BEARING_SPACING}mm apart)")
print(f"    Standoffs:   {len(L2_STANDOFF_POSITIONS_X)} pairs of M5 holes")
print(f"                 X positions: {[f'{x:.1f}' for x in L2_STANDOFF_POSITIONS_X]}")
print(f"    Cable slot:  {CABLE_SLOT_WIDTH}x{L2_CABLE_SLOT_LENGTH:.0f}mm center channel")
print(f"    Strain relief: {L2_STRAIN_RELIEF_WIDTH}x{L2_STRAIN_RELIEF_LENGTH}mm slot for RealSense USB-C zip-tie")
print()
print("  UPLOAD TO SENDCUTSEND:")
print("    Material: 6061-T6 Aluminum")
print("    Thickness: 0.118\" (3mm)")
print("    Quantity: 2 for EACH file (you need 2 of Link 1 and 2 of Link 2)")
print()
print("  ASSEMBLY:")
print("    - Two identical plates face each other, 40mm apart")
print("    - M5×40mm hex standoffs connect them (male-female)")
print("    - 608ZZ bearings press into the 8.1mm pivot holes")
print("    - Wires route through the center cable channel")
print("    - This creates a rigid box-section that resists twist")
print("=" * 65)
