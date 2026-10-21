# Blender Python script: Low-poly rectangular face mask inspired by the supplied reference.
# Run inside Blender's Scripting workspace. It creates the model and exports face_mask_ar.glb
# to the same folder as this .blend file (or /mnt/data if the blend file has not been saved).

import bpy
import math
from mathutils import Vector

# ---------- Reset scene ----------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials):
    # Keep cleanup conservative: remove unused data only
    for block in list(datablocks):
        if block.users == 0:
            datablocks.remove(block)

def mat(name, color, roughness=0.82):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
    return m

# Muted mauve/taupe face, burgundy brows/lips, lavender eyes, black pupils.
skin = mat("Face - muted taupe mauve", (0.39, 0.32, 0.34))
browmat = mat("Eyebrows - deep burgundy", (0.16, 0.055, 0.075))
eyemat = mat("Eyes - dusty lavender", (0.43, 0.43, 0.57))
lidmat = mat("Upper eyelid - warm gray", (0.34, 0.30, 0.31))
pupilmat = mat("Pupils - near black", (0.012, 0.012, 0.015))
lipmat = mat("Lips - berry red", (0.43, 0.09, 0.15))
lipshade = mat("Lower lip - muted rose", (0.32, 0.075, 0.12))

def cube_obj(name, loc, scale, material, bevel=0.0, bevel_segments=1):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    if bevel > 0:
        mod = obj.modifiers.new("Tiny softened corners", "BEVEL")
        mod.width = bevel
        mod.segments = bevel_segments
        mod.affect = 'EDGES' if hasattr(mod, "affect") else None
        obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return obj

# Coordinate convention: front of face points toward -Y; vertical is Z.
# Broad rectangular head with clipped top corners to match the reference silhouette.
verts = [
    (-1.00, -0.28, -1.12), (1.00, -0.28, -1.12),
    (1.00, -0.28, 0.72), (0.84, -0.28, 1.00),
    (-0.84, -0.28, 1.00), (-1.00, -0.28, 0.72),
    (-1.00, 0.28, -1.12), (1.00, 0.28, -1.12),
    (1.00, 0.28, 0.72), (0.84, 0.28, 1.00),
    (-0.84, 0.28, 1.00), (-1.00, 0.28, 0.72),
]
faces = [
    (0,1,2,3,4,5), (6,11,10,9,8,7),
    (0,6,7,1), (1,7,8,2), (2,8,9,3),
    (3,9,10,4), (4,10,11,5), (5,11,6,0)
]
mesh = bpy.data.meshes.new("Flat clipped rectangle head mesh")
mesh.from_pydata(verts, [], faces)
mesh.materials.append(skin)
head = bpy.data.objects.new("HEAD - flat low-poly rectangle", mesh)
bpy.context.collection.objects.link(head)

# Brows: long, simple, dark horizontal rectangles.
cube_obj("Eyebrow_L", (-0.48, -0.355, 0.42), (0.60, 0.12, 0.22), browmat, 0.035, 1)
cube_obj("Eyebrow_R", (0.48, -0.355, 0.42), (0.60, 0.12, 0.22), browmat, 0.035, 1)

# Large squared eye panels with black square pupils.
cube_obj("Eye_L", (-0.48, -0.365, -0.02), (0.62, 0.12, 0.58), eyemat, 0.025, 1)
cube_obj("Eye_R", (0.48, -0.365, -0.02), (0.62, 0.12, 0.58), eyemat, 0.025, 1)

# Flat eyelid/bottom accent strips, like the original simple AR mask.
cube_obj("Upper_lid_L", (-0.48, -0.445, 0.25), (0.62, 0.06, 0.10), lidmat, 0.025, 1)
cube_obj("Upper_lid_R", (0.48, -0.445, 0.25), (0.62, 0.06, 0.10), lidmat, 0.025, 1)
cube_obj("Lower_lid_L", (-0.48, -0.445, -0.31), (0.62, 0.06, 0.10), lidmat, 0.025, 1)
cube_obj("Lower_lid_R", (0.48, -0.445, -0.31), (0.62, 0.06, 0.10), lidmat, 0.025, 1)

cube_obj("Pupil_L", (-0.48, -0.455, -0.01), (0.17, 0.075, 0.19), pupilmat, 0.015, 1)
cube_obj("Pupil_R", (0.48, -0.455, -0.01), (0.17, 0.075, 0.19), pupilmat, 0.015, 1)

# Small flat nose block, very subtle so the look stays close to the sample.
cube_obj("Nose", (0.0, -0.37, -0.48), (0.20, 0.13, 0.17), skin, 0.015, 1)

# Two stacked rounded-rectangle mouth blocks.
cube_obj("Upper_lip", (0.0, -0.405, -0.72), (0.57, 0.13, 0.19), lipmat, 0.045, 1)
cube_obj("Lower_lip", (0.0, -0.405, -0.88), (0.57, 0.13, 0.14), lipshade, 0.035, 1)

# Organize all model pieces under one parent at origin.
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
root = bpy.context.object
root.name = "FaceMask_Root"
for obj in list(bpy.context.scene.objects):
    if obj != root:
        obj.parent = root

# Camera/light are unnecessary for GLB AR; set viewport to front view.
for obj in list(bpy.context.scene.objects):
    if obj.type in {'CAMERA', 'LIGHT'}:
        bpy.data.objects.remove(obj, do_unlink=True)

# Select root and export GLB next to this script / saved .blend.
bpy.ops.object.select_all(action='DESELECT')
root.select_set(True)
bpy.context.view_layer.objects.active = root

blend_path = bpy.data.filepath
if blend_path:
    export_dir = bpy.path.abspath("//")
else:
    export_dir = "/mnt/data"
export_path = export_dir.rstrip("/\\") + "/face_mask_ar.glb"

bpy.ops.export_scene.gltf(
    filepath=export_path,
    export_format='GLB',
    use_selection=False,
    export_apply=True
)
print("Exported face mask to:", export_path)
