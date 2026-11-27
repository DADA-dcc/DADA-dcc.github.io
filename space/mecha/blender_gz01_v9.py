# -*- coding: utf-8 -*-
"""GZ-01 v5：Sentinel 静态姿态 + 电影级雨夜港口（雾/雨丝/火花/湿地反射/城市剪影）。
用法: ... -- test|full
"""
import bpy, os, sys, math, random
from mathutils import Vector, Quaternion, Matrix
MODE = sys.argv[-1] if sys.argv[-1] in ('test','full') else 'test'
SRC=r"C:\Users\Krilenxs\Documents\默认项目\_tools\render\mecha_zhanyue.blend"
GLB=r"C:\Users\Krilenxs\Documents\默认项目\_ref\atlas-09.glb"
OUT=r"C:\Users\Krilenxs\Documents\默认项目\_tools\render"
VER='gz01'
random.seed(7)

bpy.ops.wm.open_mainfile(filepath=SRC)
sc=bpy.context.scene
KEEP=('Dock','Ring','Water','city','cb','SKY','cont','human')
for o in list(bpy.data.objects):
    if o.type=='MESH' and not o.name.startswith(KEEP): bpy.data.objects.remove(o,do_unlink=True)
    elif o.type in ('LIGHT','CAMERA'): bpy.data.objects.remove(o,do_unlink=True)
# 隐藏城市/方块道具 + 人类参照物 + 橙色地台环（Smart：去掉黄圈与白色小人）
PROPS=[o for o in bpy.data.objects if o.name.startswith(('cb','cont','city','human','Ring','SKY'))]
for o in PROPS: o.hide_render=True
before=set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=GLB)
for o in list(bpy.data.objects):
    if o.name.startswith('Icosphere'): bpy.data.objects.remove(o,do_unlink=True)
ATL=[o for o in bpy.context.scene.objects if o not in before]
AMESH=[o for o in ATL if o.type=='MESH']
ARIG=[o for o in ATL if o.type=='ARMATURE']
rig=ARIG[0] if ARIG else None
if rig and rig.animation_data is None: rig.animation_data_create()

def bbox(objs):
    mn=Vector((1e9,)*3); mx=Vector((-1e9,)*3)
    for o in objs:
        for c in o.bound_box:
            w=o.matrix_world @ Vector(c)
            for i in range(3): mn[i]=min(mn[i],w[i]); mx[i]=max(mx[i],w[i])
    return mn,mx
mn,mx=bbox(AMESH); cx=(mn.x+mx.x)/2; cy=(mn.y+mx.y)/2
for o in ATL:
    if o.parent is None: o.location.x-=cx; o.location.y-=cy; o.location.z-=mn.z
bpy.context.view_layer.update()
# Sentinel 姿态
if rig:
    act=bpy.data.actions.get('Sentinel_ATLAS_09_RIG')
    if act:
        rig.animation_data.action=act; sc.frame_set(48); bpy.context.view_layer.update()
mn,mx=bbox(AMESH); CZ=(mn.z+mx.z)/2; H=mx.z-mn.z
print('H',round(H,2),'CZ',round(CZ,2))

def hx(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c)

# ---- 材质：橙核 + 钢蓝灰 ----
for m in bpy.data.materials:
    if not m.use_nodes: continue
    nt=m.node_tree; b=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
    if not b: continue
    nm=m.name.lower()
    if 'reactor' in nm or 'emission' in nm:
        ec=b.inputs['Emission Color']; links=list(ec.links)
        if links:
            src=links[0].from_node; bw=nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(src.outputs[0],bw.inputs['Color'])
            mx2=nt.nodes.new('ShaderNodeMixRGB'); mx2.blend_type='MULTIPLY'; mx2.inputs['Fac'].default_value=1.0
            mx2.inputs['Color2'].default_value=(1.0,0.40,0.06,1.0)
            nt.links.new(bw.outputs['Val'],mx2.inputs['Color1']); nt.links.new(mx2.outputs[0],ec)
        else: ec.default_value=(1.0,0.42,0.07,1.0)
        b.inputs['Emission Strength'].default_value=2.4
    bc=b.inputs['Base Color']
    if bc.links:
        s2=bc.links[0].from_node
        mx3=nt.nodes.new('ShaderNodeMixRGB'); mx3.blend_type='MULTIPLY'; mx3.inputs['Fac'].default_value=0.5
        mx3.inputs['Color2'].default_value=(0.78,0.86,1.02,1.0)
        nt.links.new(s2.outputs[0],mx3.inputs['Color1']); nt.links.new(mx3.outputs[0],bc)

# 平滑（EdgeSplit 30）
for o in AMESH:
    for p in o.data.polygons: p.use_smooth=True
    es=o.modifiers.new('ES','EDGE_SPLIT'); es.use_edge_angle=True; es.split_angle=math.radians(30); es.use_edge_sharp=True

# ---- 湿地面反射：Water 低粗糙 ----
for nm in ('Water','Dock'):
    ob=bpy.data.objects.get(nm)
    if ob and ob.data.materials:
        for m in ob.data.materials:
            if not m.use_nodes: continue
            b=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
            if b:
                try:
                    b.inputs['Roughness'].default_value=0.60
                    b.inputs['Metallic'].default_value=0.20
                except: pass

def newmat(name, base, rough=0.5, metal=0.0, emit=None, estr=0.0):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; nt.nodes.clear()
    o=nt.nodes.new('ShaderNodeOutputMaterial'); b=nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value=(*base,1); b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal
    if emit:
        b.inputs['Emission Color'].default_value=(*emit,1); b.inputs['Emission Strength'].default_value=estr
    nt.links.new(b.outputs[0], o.inputs['Surface']); return m

def mesh_from(name, verts, faces, mat):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    ob=bpy.data.objects.new(name,me); sc.collection.objects.link(ob); ob.data.materials.append(mat); return ob

# ---- 雨丝：700 条细短、带倾斜、粗细/长短不一 ----
rain_mat=newmat('RAIN',(0.55,0.68,0.85),0.4,0.0,(0.30,0.45,0.72),0.10)
V=[];F=[];i=0
for _ in range(700):
    x=random.uniform(-38,38); y=random.uniform(-38,38); z=random.uniform(0.5,36)
    ln=random.uniform(0.25,0.8); w=random.uniform(0.003,0.010)
    tx=random.uniform(-0.45,0.45); ty=random.uniform(-0.30,0.30)  # 倾斜更大
    base=i*8
    for k,dz in enumerate((0,ln)):
        ox=tx*dz; oy=ty*dz
        for dx in (-w,w):
            for dy in (-w,w):
                V.append((x+ox+dx,y+oy+dy,z+dz))
    F += [(base+0,base+1,base+3,base+2),(base+4,base+6,base+7,base+5),
          (base+0,base+4,base+5,base+1),(base+2,base+3,base+7,base+6),
          (base+0,base+2,base+6,base+4),(base+1,base+5,base+7,base+3)]
    i+=1
rain=mesh_from('RAIN_MESH',V,F,rain_mat)

# ---- 火花粒子：脚下/周身 ----
spark_mat=newmat('SPARK',(1.0,0.45,0.1),0.3,0.0,(1.0,0.42,0.08),4.5)
V=[];F=[]
def add_cube(V,F,x,y,z,s):
    b=len(V)
    for dx in (-s,s):
        for dy in (-s,s):
            for dz in (-s,s): V.append((x+dx,y+dy,z+dz))
    F += [(b+0,b+1,b+3,b+2),(b+4,b+6,b+7,b+5),(b+0,b+4,b+5,b+1),(b+2,b+3,b+7,b+6),(b+0,b+2,b+6,b+4),(b+1,b+5,b+7,b+3)]
for _ in range(34):
    add_cube(V,F, random.uniform(-8,8), random.uniform(-8,8), random.uniform(0.02,0.6), random.uniform(0.015,0.04))
# 少量上扬火星
for _ in range(18):
    add_cube(V,F, random.uniform(-7,7), random.uniform(-7,7), random.uniform(0.8,5.0), random.uniform(0.012,0.028))
sparks=mesh_from('SPARK_MESH',V,F,spark_mat)

# ---- 远景城市剪影 + 窗灯 ----
city_mat=newmat('CITY',(0.02,0.03,0.05),0.9,0.0,(0.02,0.03,0.05),0.15)
win_mat=newmat('WIN',(1.0,0.75,0.4),0.6,0.0,(1.0,0.7,0.35),6.0)
V=[];F=[];WV=[];WF=[];ci=0
for _ in range(26):
    ang=random.uniform(0,math.tau); r=random.uniform(70,110)
    x=math.cos(ang)*r; y=math.sin(ang)*r
    w=random.uniform(6,14); d=random.uniform(6,14); ht=random.uniform(10,40)
    b=len(V)
    for dx in (-w/2,w/2):
        for dy in (-d/2,d/2):
            for dz in (0,ht): V.append((x+dx,y+dy,dz))
    F += [(b+0,b+1,b+3,b+2),(b+4,b+6,b+7,b+5),(b+0,b+4,b+5,b+1),(b+2,b+3,b+7,b+6),(b+0,b+2,b+6,b+4),(b+1,b+5,b+7,b+3)]
    # 几条窗灯条
    for _k in range(3):
        wb=len(WV); zz=random.uniform(2,ht-2); ww=random.uniform(1,3)
        cz=zz; cxx=x+random.uniform(-w/2+1,w/2-1); cyy=y+random.uniform(-d/2+1,d/2-1)
        for dx in (-ww/2,ww/2):
            for dz in (0,0.6):
                pass
        add_cube(WV,WF,cxx,cyy,cz,0.35)
city=mesh_from('CITY_MESH',V,F,city_mat)
wins=mesh_from('WIN_MESH',WV,WF,win_mat)

# ---- 体积雾 ----
bpy.ops.mesh.primitive_cube_add(size=460, location=(0,0,46))
fog=bpy.context.active_object; fog.name='FOG'
fm=bpy.data.materials.new('FOGMAT'); fm.use_nodes=True; fnt=fm.node_tree; fnt.nodes.clear()
fo=fnt.nodes.new('ShaderNodeOutputMaterial'); pv=fnt.nodes.new('ShaderNodeVolumePrincipled')
pv.inputs['Density'].default_value=0.0011
try: pv.inputs['Color'].default_value=(0.42,0.52,0.68,1.0)
except: pass
fnt.links.new(pv.outputs[0], fo.inputs['Volume']); fog.data.materials.append(fm)

# ---- 灯光 ----
def area(name,loc,tgt,power,sx,sy,hexcol,spread=180):
    d=bpy.data.lights.new(name,'AREA'); d.energy=power; d.shape='RECTANGLE'; d.size=sx; d.size_y=sy; d.color=hx(hexcol)
    try: d.spread=math.radians(spread)
    except: pass
    ob=bpy.data.objects.new(name,d); sc.collection.objects.link(ob); ob.location=loc
    ob.rotation_euler=(Vector(tgt)-Vector(loc)).to_track_quat('-Z','Y').to_euler(); return ob
area('KEY',(-26,46,40),(0,0,CZ),12000,30,30,'#FFE9CC',150)
area('FILL',(10,-58,22),(0,0,CZ),2500,50,44,'#BFD8FF',160)
area('RIMB',(0,36,26),(0,0,CZ+3),72000,10,0.6,'#5E9BFF',50)    # 后上方细条擦边勾轮廓
area('RIMB2',(-20,32,22),(0,0,CZ),55000,8,0.6,'#6FA8FF',50)
area('RIMB3',(20,32,22),(0,0,CZ),55000,8,0.6,'#6FA8FF',50)
area('RIMC',(-18,-48,30),(0,0,CZ),5000,22,22,'#9FC4FF',110)
area('TOP',(0,-8,60),(0,0,CZ),2000,40,6,'#EAF2FF',140)
area('PORT',(60,-70,10),(0,0,10),3600,20,10,'#FF9A4A',120)

# ---- 世界/渲染 ----
w=sc.world or bpy.data.worlds.new('W'); sc.world=w; w.use_nodes=True; nt=w.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
bg=nt.nodes.new('ShaderNodeBackground'); bg.inputs['Color'].default_value=(*hx('#0a1018'),1); bg.inputs['Strength'].default_value=0.12
wo=nt.nodes.new('ShaderNodeOutputWorld'); nt.links.new(bg.outputs['Background'],wo.inputs['Surface'])
sc.render.engine='CYCLES'; sc.cycles.samples=200; sc.cycles.use_denoising=True
try: sc.cycles.denoiser='OPENIMAGEDENOISE'
except: pass
sc.render.resolution_x=1920; sc.render.resolution_y=1080
try:
    sc.use_nodes=True; ntc=sc.node_tree; ntc.nodes.clear()
    rl=ntc.nodes.new('CompositorNodeRLayers'); gl=ntc.nodes.new('CompositorNodeGlare')
    gl.glare_type='FOG_GLOW'; gl.quality='HIGH'; gl.threshold=0.9; gl.size=8; gl.mix=-0.4
    cp=ntc.nodes.new('CompositorNodeComposite')
    ntc.links.new(rl.outputs['Image'],gl.inputs['Image']); ntc.links.new(gl.outputs['Image'],cp.inputs['Image'])
except Exception as e: print('comp skip',e)
vs=sc.view_settings
try:
    vs.view_transform='Filmic'
    for lk in ('Filmic - Medium High Contrast','Medium High Contrast'):
        try: vs.look=lk; break
        except: pass
    vs.exposure=-0.70
except: pass

def mkcam(loc,tgt,lens,roll=0.0):
    c=bpy.data.cameras.new('C'); c.lens=lens
    ob=bpy.data.objects.new('C',c); sc.collection.objects.link(ob); ob.location=loc
    q=(Vector(tgt)-Vector(loc)).to_track_quat('-Z','Y')
    if roll: q=q@Quaternion(Vector((0,0,1)),math.radians(roll))
    ob.rotation_mode='QUATERNION'; ob.rotation_quaternion=q; return ob
D=H*2.6
SHOTS=[
 ('battlewide',(-D*0.44,-D*0.62,3.0),(0,0,CZ*0.95),26,0),
 ('battleclose',(D*0.26,-D*0.56,2.0),(0,0,CZ*1.12),32,3),
]
todo=SHOTS if MODE=='full' else [SHOTS[0]]
for tag,loc,tgt,lens,roll in todo:
    cam=mkcam(loc,tgt,lens,roll); sc.camera=cam
    fp=os.path.join(OUT,f'{VER}_{tag}.png'); sc.render.filepath=fp
    print('=== render',tag,'==='); bpy.ops.render.render(write_still=True); print('done',fp)
print('=== DONE',MODE,'===')

