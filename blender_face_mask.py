# Low-poly rectangular face mask based on the supplied reference image.
# Run in Blender > Scripting > Run Script. Exports face_mask_ar.glb beside the .blend file,
# or to /mnt/data if the .blend file has not been saved.

import bpy
import os

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def material(name, rgb):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*rgb, 1)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.85
    return m

skin = material("Muted taupe mauve face", (0.39, 0.32, 0.34))
brow = material("Deep burgundy eyebrows", (0.16, 0.055, 0.075))
eye = material("Dusty lavender eyes", (0.43, 0.43, 0.57))
lid = material("Warm gray eyelids", (0.34, 0.30, 0.31))
black = material("Black square pupils", (0.012, 0.012, 0.015))
lip = material("Berry red upper lip", (0.43, 0.09, 0.15))
lip2 = material("Muted rose lower lip", (0.32, 0.075, 0.12))

def box(name, loc, dims, mat, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    if bevel:
        mod = o.modifiers.new("Slightly softened corners", "BEVEL")
        mod.width = bevel
        mod.segments = 1
        o.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return o

# Flat rectangular head with clipped top corners, front faces toward -Y.
verts = [
    (-1,-.28,-1.12),(1,-.28,-1.12),(1,-.28,.72),(.84,-.28,1),
    (-.84,-.28,1),(-1,-.28,.72),(-1,.28,-1.12),(1,.28,-1.12),
    (1,.28,.72),(.84,.28,1),(-.84,.28,1),(-1,.28,.72)
]
faces = [(0,1,2,3,4,5),(6,11,10,9,8,7),(0,6,7,1),(1,7,8,2),
         (2,8,9,3),(3,9,10,4),(4,10,11,5),(5,11,6,0)]
mesh = bpy.data.meshes.new("Clipped rectangle head mesh")
mesh.from_pydata(verts, [], faces)
mesh.materials.append(skin)
head = bpy.data.objects.new("HEAD - flat rectangular mask", mesh)
bpy.context.collection.objects.link(head)

# Brows and squared eyes, matching the reference layout.
box("Eyebrow_L",(-.48,-.355,.42),(.60,.12,.22),brow,.035)
box("Eyebrow_R",(.48,-.355,.42),(.60,.12,.22),brow,.035)
box("Eye_L",(-.48,-.365,-.02),(.62,.12,.58),eye,.025)
box("Eye_R",(.48,-.365,-.02),(.62,.12,.58),eye,.025)
box("Upper_lid_L",(-.48,-.445,.25),(.62,.06,.10),lid,.02)
box("Upper_lid_R",(.48,-.445,.25),(.62,.06,.10),lid,.02)
box("Lower_lid_L",(-.48,-.445,-.31),(.62,.06,.10),lid,.02)
box("Lower_lid_R",(.48,-.445,-.31),(.62,.06,.10),lid,.02)
box("Pupil_L",(-.48,-.455,-.01),(.17,.075,.19),black,.012)
box("Pupil_R",(.48,-.455,-.01),(.17,.075,.19),black,.012)
box("Nose",(0,-.37,-.48),(.20,.13,.17),skin,.01)
box("Upper_lip",(0,-.405,-.72),(.57,.13,.19),lip,.04)
box("Lower_lip",(0,-.405,-.88),(.57,.13,.14),lip2,.03)

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
root = bpy.context.object
root.name = "FaceMask_Root"
for obj in list(bpy.context.scene.objects):
    if obj != root:
        obj.parent = root

blend_path = bpy.data.filepath
export_dir = bpy.path.abspath("//") if blend_path else "/mnt/data"
export_path = os.path.join(export_dir, "face_mask_ar.glb")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLB')
print("Exported:", export_path)
