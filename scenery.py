"""Cenário estático autoral de parque de pesquisa, por composição de primitivas."""
from math import sin,cos,pi
from pathlib import Path
import numpy as np
from models import transform
from py3d.core_ext.object3d import Object3D
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.texture import Texture
from py3d.geometry.geometry import Geometry
from py3d.geometry.rectangle import RectangleGeometry
from py3d.material.phong import PhongMaterial

def decorate(root,models):
    """Todos os obstáculos ficam fora do corredor dos personagens."""
    part=models.part
    # Calçada e meio-fio; o centro da pista permanece completamente livre.
    for z in (-2.45,2.45):
        part(root,(-.8,.085,z),(18.2,.17,.18),(.57,.61,.52))
    for i in range(15):
        color=(.59,.57,.46) if i%2 else (.65,.63,.51)
        part(root,(-9.2+i*1.25,.05,3.12),(1.19,.10,.92),color)
    # Estação de pesquisa ao fundo, sem terceiro personagem.
    part(root,(5.1,.10,-6.1),(4.0,.20,3.0),(.48,.55,.49))
    part(root,(5.1,1.03,-6.1),(3.4,1.66,2.35),(.72,.76,.66))
    part(root,(5.1,1.91,-6.1),(3.85,.18,2.7),(.16,.32,.34))
    part(root,(5.1,.45,-4.88),(3.45,.20,.12),(.18,.36,.36))
    for x in (4.05,5.05):
        part(root,(x,1.18,-4.90),(.78,.68,.055),(.12,.31,.37))
        part(root,(x,1.25,-4.86),(.63,.45,.025),(.39,.69,.72))
        part(root,(x,1.25,-4.84),(.025,.46,.025),(.77,.82,.69))
    part(root,(6.2,.91,-4.89),(.58,1.42,.07),(.18,.36,.36))
    part(root,(6.0,.90,-4.82),(.045,.12,.025),(.88,.76,.40))
    part(root,(6.2,2.34,-6.4),(.065,.78,.065),(.69,.73,.67))
    part(root,(6.2,2.65,-6.4),(.75,.055,.055),(.69,.73,.67))
    part(root,(6.2,2.77,-6.4),(.13,.16,.13),(.90,.53,.20))
    texture=Texture(str(Path(__file__).resolve().parent/'assets/estacao.png'))
    sign_material=PhongMaterial(texture=texture,number_of_light_sources=2,use_shadow=True,
        property_dict={'specularStrength':.02})
    sign=Mesh(RectangleGeometry(width=2.7,height=.35),sign_material)
    sign.set_position([5.1,1.68,-4.905]);root.add(sign)
    # Portal de chegada no fim da pista, além do alcance da cabeça do dinossauro.
    for z in (-2.65,2.65):
        part(root,(7.9,1.6,z),(.25,3.2,.25),(.17,.34,.33))
        part(root,(7.9,.30,z),(.48,.60,.48),(.62,.65,.53))
        part(root,(7.9,2.65,z),(.29,.12,.29),(.83,.68,.30))
    part(root,(7.9,3.20,0),(.32,.28,5.65),(.17,.34,.33))
    part(root,(7.9,3.38,0),(.45,.10,5.9),(.69,.73,.57))
    # Bancos de observação nas laterais da calçada.
    for x in (-8.1,7.2):
        for dx in (-.55,.55):
            part(root,(x+dx,.24,4.1),(.13,.48,.56),(.20,.29,.27))
        for z in (3.92,4.12,4.32):
            part(root,(x,.52,z),(1.65,.11,.16),(.59,.40,.22))
        part(root,(x,.88,4.4),(1.65,.51,.10),(.59,.40,.22))
    # Lago ornamental e bordas, fora do corredor de circulação.
    part(root,(8.5,.025,6.7),(4.0,.05,2.5),(.12,.40,.44))
    water=models.material((.12,.40,.44))
    water.set_properties({'specularStrength':.8,'shininess':96})
    for z in (5.35,8.05):
        part(root,(8.5,.15,z),(4.35,.30,.24),(.51,.55,.45))
    for x in (6.35,10.65):
        part(root,(x,.15,6.7),(.24,.30,2.5),(.51,.55,.45))
    for x,z in ((7.1,6.1),(9.5,7.3),(8.3,7.0)):
        part(root,(x,.061,z),(.38,.018,.25),(.38,.61,.37))
    # Palmas estilizadas com folhas segmentadas e samambaias baixas.
    for x,z,scale in ((-11,-4.8,1.1),(11,3.7,.9),(-7,-8.0,1.0)):
        tree=Object3D();root.add(tree);transform(tree,(x,0,z),scale=(scale,scale,scale))
        part(tree,(0,1.3,0),(.14,2.6,.14),(.46,.35,.21),True)
        for i in range(7):
            a=2*pi*i/7
            for r,y,pitch in ((.38,2.78,-.18),(1.0,2.72,.20),(1.56,2.40,.58)):
                leaf=part(tree,(sin(a)*r,y,cos(a)*r),(.31,.075,.76),
                    (.31,.51,.31) if i%2 else (.39,.59,.34))
                transform(leaf,leaf.local_position,yaw=a,pitch=pitch,scale=(.31,.075,.76))
    for x,z in ((-10,3.6),(-6,5.0),(-2,-5.5),(1,5.8),(10,-4.8),(-11,-1)):
        part(root,(x,.035,z),(1.3,.07,.9),(.33,.37,.25))
        for i in range(6):
            a=2*pi*i/6
            leaf=part(root,(x+.27*sin(a),.27,z+.27*cos(a)),(.16,.08,.65),(.35,.54,.30))
            transform(leaf,leaf.local_position,yaw=a,pitch=-.5,scale=(.16,.08,.65))
    # Relevo em degraus: linguagem geométrica consistente com os brinquedos.
    for x,z,w,h in ((-11,-8.3,4.4,3.0),(0,-9,4.5,2.8),(10.5,-8.5,4.1,3.5)):
        for level in range(3):
            width=w*(1-.23*level)
            part(root,(x+.25*level,h*(level+.5)/3,z),
                 (width,h/3,width*.55),(.30+.04*level,.39+.04*level,.35+.035*level))

def batch_static(root,exclude=()):
    """Bakes only static meshes, grouping triangles by material/shadow behavior."""
    excluded={id(mesh) for mesh in exclude}
    meshes=[n for n in root.descendant_list if isinstance(n,Mesh) and id(n) not in excluded]
    groups={}
    for mesh in meshes:
        key=(id(mesh.material),getattr(mesh,'cast_shadow',True))
        group=groups.setdefault(key,{'material':mesh.material,'shadow':key[1],'arrays':{}})
        matrix=mesh.global_matrix
        normal_matrix=np.linalg.inv(matrix[:3,:3]).T
        for name,attribute in mesh.geometry.attribute_dict.items():
            data=np.array(attribute.data,dtype=float)
            if name=='vertexPosition':data=data@matrix[:3,:3].T+matrix[:3,3]
            elif name in ('vertexNormal','faceNormal'):
                data=data@normal_matrix.T
                data/=np.maximum(np.linalg.norm(data,axis=1,keepdims=True),1e-12)
            group['arrays'].setdefault(name,[]).append(data)
        mesh.parent.remove(mesh)
    for group in groups.values():
        geometry=Geometry()
        for name,arrays in group['arrays'].items():
            data=np.concatenate(arrays)
            geometry.add_attribute('vec2' if name=='vertexUV' else 'vec3',name,data.tolist())
        merged=Mesh(geometry,group['material']);merged.cast_shadow=group['shadow'];root.add(merged)
    return {'static_meshes_before':len(meshes),'static_meshes_after':len(groups),
            'triangles':sum(n.geometry.vertex_count//3 for n in root.descendant_list if isinstance(n,Mesh) and id(n) not in excluded)}
