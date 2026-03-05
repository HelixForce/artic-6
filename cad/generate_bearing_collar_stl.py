"""
ARTIC-6 Thrust Bearing Collar — STL Generator
===============================================
3D-printed PETG collar that captures the 51100 thrust bearing on the baseplate.

   - Sits on TOP of the 250×250mm aluminum baseplate
   - Bearing drops into the recess on the bottom
   - Bolts down through 3× M3 holes (matching baseplate DXF)
   - Shaft/bolt passes through the center bore

Print settings:
   Material:   PETG
   Layer:      0.2mm
   Infill:     60%+ (this is structural)
   Walls:      4 minimum
   Orientation: Print flat (recess facing up on bed = cleaner recess surface)
                Actually print recess DOWN so bearing contact is smooth bed-side

Run:  python generate_bearing_collar_stl.py
"""

import numpy as np
import struct
import os

# ================================================================
#  PARAMETERS
# ================================================================

# 51100 thrust bearing: 10mm bore, 24mm OD, 9mm thick
# The collar captures the bearing in a recess on its bottom face

OUTER_DIA = 44.0          # mm — collar outer diameter (flange, needs 3mm+ wall around bolt holes)
COLLAR_HEIGHT = 6.0       # mm — total height
BORE_DIA = 10.5           # mm — center hole (matches baseplate 10.5mm hole)
BEARING_RECESS_DIA = 24.5 # mm — 51100 OD + 0.5mm clearance
BEARING_RECESS_DEPTH = 2.0 # mm — captures bearing without being too tight

# Bolt holes — M3 clearance, matching baseplate DXF positions
BOLT_HOLE_DIA = 3.4       # mm
BOLT_RADIUS = 16.0        # mm from center
N_BOLTS = 3
BOLT_ANGLE_OFFSET = 30.0  # degrees (matches baseplate generator)

# Mesh resolution
N_SEGMENTS = 72           # segments per full circle (5° per segment)


# ================================================================
#  MESH HELPER FUNCTIONS
# ================================================================

def annular_face_triangles(inner_r, outer_r, z, normal_up=True, n_seg=N_SEGMENTS):
    """Generate triangles for a flat ring (annulus) at height z."""
    angles = np.linspace(0, 2 * np.pi, n_seg, endpoint=False)
    tris = []
    for i in range(n_seg):
        j = (i + 1) % n_seg
        a0, a1 = angles[i], angles[j]
        # Quad corners: inner0, outer0, outer1, inner1
        p_in0 = [inner_r * np.cos(a0), inner_r * np.sin(a0), z]
        p_out0 = [outer_r * np.cos(a0), outer_r * np.sin(a0), z]
        p_out1 = [outer_r * np.cos(a1), outer_r * np.sin(a1), z]
        p_in1 = [inner_r * np.cos(a1), inner_r * np.sin(a1), z]
        if normal_up:
            tris.append([p_in0, p_out0, p_out1])
            tris.append([p_in0, p_out1, p_in1])
        else:
            tris.append([p_in0, p_out1, p_out0])
            tris.append([p_in0, p_in1, p_out1])
    return tris


def cylinder_wall_triangles(r, z_bot, z_top, facing_out=True, n_seg=N_SEGMENTS):
    """Generate triangles for a cylindrical wall surface."""
    angles = np.linspace(0, 2 * np.pi, n_seg, endpoint=False)
    tris = []
    for i in range(n_seg):
        j = (i + 1) % n_seg
        a0, a1 = angles[i], angles[j]
        p0 = [r * np.cos(a0), r * np.sin(a0), z_bot]
        p1 = [r * np.cos(a0), r * np.sin(a0), z_top]
        p2 = [r * np.cos(a1), r * np.sin(a1), z_top]
        p3 = [r * np.cos(a1), r * np.sin(a1), z_bot]
        if facing_out:
            tris.append([p0, p2, p1])
            tris.append([p0, p3, p2])
        else:
            tris.append([p0, p1, p2])
            tris.append([p0, p2, p3])
    return tris


def bolt_hole_triangles(cx, cy, r, z_bot, z_top, n_seg=24):
    """Generate triangles for a cylindrical bolt hole (top face, bottom face, wall)."""
    angles = np.linspace(0, 2 * np.pi, n_seg, endpoint=False)
    tris = []

    # Cylinder wall (facing inward = toward hole center)
    for i in range(n_seg):
        j = (i + 1) % n_seg
        a0, a1 = angles[i], angles[j]
        p0 = [cx + r * np.cos(a0), cy + r * np.sin(a0), z_bot]
        p1 = [cx + r * np.cos(a0), cy + r * np.sin(a0), z_top]
        p2 = [cx + r * np.cos(a1), cy + r * np.sin(a1), z_top]
        p3 = [cx + r * np.cos(a1), cy + r * np.sin(a1), z_bot]
        # Normals face inward (toward hole axis)
        tris.append([p0, p1, p2])
        tris.append([p0, p2, p3])

    return tris


# ================================================================
#  BUILD THE COLLAR MESH
# ================================================================

outer_r = OUTER_DIA / 2.0
bore_r = BORE_DIA / 2.0
recess_r = BEARING_RECESS_DIA / 2.0
bolt_r = BOLT_HOLE_DIA / 2.0

all_triangles = []

# --- Top face: full annulus from bore to outer at z=COLLAR_HEIGHT ---
all_triangles += annular_face_triangles(bore_r, outer_r, COLLAR_HEIGHT, normal_up=True)

# --- Bottom face (outer ring): annulus from recess_r to outer_r at z=0 ---
all_triangles += annular_face_triangles(recess_r, outer_r, 0.0, normal_up=False)

# --- Recess bottom face: annulus from bore_r to recess_r at z=BEARING_RECESS_DEPTH ---
all_triangles += annular_face_triangles(bore_r, recess_r, BEARING_RECESS_DEPTH, normal_up=False)

# --- Outer wall: cylinder at outer_r from z=0 to COLLAR_HEIGHT ---
all_triangles += cylinder_wall_triangles(outer_r, 0.0, COLLAR_HEIGHT, facing_out=True)

# --- Bore wall: cylinder at bore_r from z=0 to COLLAR_HEIGHT ---
all_triangles += cylinder_wall_triangles(bore_r, 0.0, COLLAR_HEIGHT, facing_out=False)

# --- Recess inner wall: cylinder at recess_r from z=0 to BEARING_RECESS_DEPTH ---
all_triangles += cylinder_wall_triangles(recess_r, 0.0, BEARING_RECESS_DEPTH, facing_out=False)

# --- Bolt holes ---
for i in range(N_BOLTS):
    angle = np.radians(i * 360.0 / N_BOLTS + BOLT_ANGLE_OFFSET)
    bx = BOLT_RADIUS * np.cos(angle)
    by = BOLT_RADIUS * np.sin(angle)

    # Bolt hole goes all the way through (z=0 to COLLAR_HEIGHT)
    # At this radius (16mm), the bolt hole is in the outer ring (recess_r=12.25 < 16 < outer_r=19)
    # So it goes from z=0 to z=COLLAR_HEIGHT
    all_triangles += bolt_hole_triangles(bx, by, bolt_r, 0.0, COLLAR_HEIGHT)


# ================================================================
#  WRITE BINARY STL
# ================================================================

n_tris = len(all_triangles)
triangles = np.array(all_triangles, dtype=np.float32)

# Calculate face normals
v0 = triangles[:, 0, :]
v1 = triangles[:, 1, :]
v2 = triangles[:, 2, :]
edge1 = v1 - v0
edge2 = v2 - v0
normals = np.cross(edge1, edge2)
# Normalize
lengths = np.linalg.norm(normals, axis=1, keepdims=True)
lengths[lengths == 0] = 1  # avoid division by zero
normals = normals / lengths

output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, "thrust_bearing_collar.stl")

with open(output_path, 'wb') as f:
    # 80-byte header
    header = b'ARTIC-6 Thrust Bearing Collar - 51100 - PETG' + b'\0' * 35
    f.write(header[:80])
    # Number of triangles
    f.write(struct.pack('<I', n_tris))
    # Triangle data
    for i in range(n_tris):
        # Normal
        f.write(struct.pack('<3f', normals[i, 0], normals[i, 1], normals[i, 2]))
        # 3 vertices
        for j in range(3):
            f.write(struct.pack('<3f', triangles[i, j, 0], triangles[i, j, 1], triangles[i, j, 2]))
        # Attribute byte count
        f.write(struct.pack('<H', 0))


# ================================================================
#  SUMMARY
# ================================================================

print()
print("=" * 60)
print("  ARTIC-6 THRUST BEARING COLLAR — STL GENERATED")
print("=" * 60)
print(f"  File:     {output_path}")
print(f"  Triangles: {n_tris}")
print()
print("  DIMENSIONS:")
print(f"    Outer diameter:      {OUTER_DIA}mm")
print(f"    Total height:        {COLLAR_HEIGHT}mm")
print(f"    Center bore:         {BORE_DIA}mm")
print(f"    Bearing recess:      {BEARING_RECESS_DIA}mm dia × {BEARING_RECESS_DEPTH}mm deep")
print(f"    Bolt holes:          {N_BOLTS}× M3 ({BOLT_HOLE_DIA}mm) at R={BOLT_RADIUS}mm")
print()
print("  FITS:")
print(f"    51100 thrust bearing (10mm bore, 24mm OD, 9mm thick)")
print(f"    Bearing drops into {BEARING_RECESS_DIA}mm recess ({(BEARING_RECESS_DIA-24.0)/2:.1f}mm clearance per side)")
print(f"    Bolts match baseplate collar holes (3× M3 at R=16mm, 120° apart)")
print()
print("  PRINT SETTINGS:")
print("    Material:    PETG")
print("    Layer:       0.2mm")
print("    Infill:      60%+")
print("    Walls:       4 minimum")
print("    Orientation: Recess facing DOWN (bed surface = smooth bearing contact)")
print()
print("  ASSEMBLY:")
print("    1. Drop 51100 thrust bearing into recess")
print("    2. Place collar on baseplate (bearing between collar and plate)")
print("    3. Align 3× M3 holes with baseplate collar holes")
print("    4. Bolt down with M3×8mm screws (through collar into baseplate)")
print("    5. Turntable sits on TOP of bearing")
print()
print("  NOTE: Bolt holes are modeled as wall geometry only.")
print("  Your slicer should handle them correctly, but if holes")
print("  don't look right, drill with a 3.5mm bit after printing.")
print("=" * 60)
