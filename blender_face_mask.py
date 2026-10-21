import bpy, math, os
# Blender > Scripting > open this file > Run Script.
# Creates a stylized sage-green geometric face mask and exports face_mask_ar.glb.
OUT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else (bpy.path.abspath("//") or os.getcwd())
os.makedirs(OUT, exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def material(name, color):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*color,1)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value=.72
    return m
sage=material("Sage Green",(0.40,.55,.49)); ivory=material("Warm Ivory",(.91,.87,.77)); plum=material("Deep Plum",(.20,.10,.19)); dark=material("Dark Sage",(.16,.27,.24)); coral=material("Coral",(.78,.35,.36)); berry=material("Berry",(.43,.13,.25)); peach=material("Peach",(.96,.66,.49))
def cube(n,loc,dim,ma,bevel=.05):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=n; o.dimensions=dim
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(ma)
    if bevel:
        b=o.modifiers.new("Soft edges","BEVEL"); b.width=bevel; b.segments=3
        o.modifiers.new("Weighted normals","WEIGHTED_NORMAL")
    return o
def ball(n,loc,scale,ma):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=loc); o=bpy.context.object; o.name=n; o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(ma); bpy.ops.object.shade_smooth(); return o
# Front is -Y. Polygon silhouette with tapered jaw.
p=[(-.78,1),(-.58,1.18),(.58,1.18),(.78,1),(.82,.45),(.72,-.42),(.45,-.78),(0,-.88),(-.45,-.78),(-.72,-.42),(-.82,.45)]
n=len(p); v=[(x,0,z) for x,z in p]+[(x,.18,z) for x,z in p]
f=[tuple(range(n)),tuple(range(n,2*n))]
for i in range(n): j=(i+1)%n; f.append((i,j,j+n,i+n))
me=bpy.data.meshes.new("MaskMesh"); me.from_pydata(v,[],f); me.materials.append(sage)
head=bpy.data.objects.new("SAGE_MASK_HEAD",me); bpy.context.collection.objects.link(head)
b=head.modifiers.new("Rounded silhouette","BEVEL"); b.width=.07; b.segments=3; head.modifiers.new("Normals","WEIGHTED_NORMAL")
for side,x in (("L",-.34),("R",.34)):
    cube(side+"_EyeSocket",(x,-.075,.24),(.43,.13,.36),dark,.07)
    cube(side+"_Eye",(x,-.16,.22),(.34,.09,.25),ivory,.05)
    ball(side+"_Pupil",(x+.025,-.222,.22),(.075,.035,.085),plum)
    ball(side+"_EyeGlint",(x+.045,-.253,.25),(.022,.012,.022),ivory)
    br=cube(side+"_Brow",(x,-.14,.53),(.39,.10,.11),dark,.04); br.rotation_euler[1]=math.radians(7 if side=="L" else -7)
ball("NoseBridge",(0,-.14,-.02),(.105,.10,.20),sage)
ball("NoseTip",(0,-.235,-.13),(.12,.07,.075),peach)
for side,x in (("L",-.53),("R",.53)):
    for i in range(3): ball(f"{side}_CheekMark_{i}",(x+(i-1)*.065,-.12,-.18-(i%2)*.055),(.025,.018,.025),coral)
cube("Mouth_Upper",(0,-.16,-.43),(.40,.12,.12),berry,.04)
cube("Mouth_Lower",(0,-.17,-.55),(.31,.10,.085),coral,.03)
for x in (-.16,0,.16): ball("Forehead_Dot",(x,-.105,.84),(.035,.025,.035),peach)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,"face_mask_ar.glb"),export_format='GLB',use_selection=True)
print("Exported face_mask_ar.glb to",OUT)
