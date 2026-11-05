"""Modelos autorais por composição das geometrias do framework do livro."""
from math import pi
import numpy as np
from py3d.core.matrix import Matrix
from py3d.core_ext.object3d import Object3D
from py3d.core_ext.mesh import Mesh
from py3d.geometry.box import BoxGeometry
from py3d.geometry.cylinder import CylinderGeometry
from py3d.material.phong import PhongMaterial

def transform(node, pos=(0,0,0), yaw=0, pitch=0, roll=0, scale=(1,1,1)):
    node.local_matrix = (Matrix.make_translation(*pos) @ Matrix.make_rotation_y(yaw)
                         @ Matrix.make_rotation_x(pitch) @ Matrix.make_rotation_z(roll)
                         @ np.diag([*scale,1]))

class Models:
    def __init__(self):
        self.box = BoxGeometry()
        self.cylinder = CylinderGeometry(radius=1, height=1, radial_segments=20)
        self.materials = {}

    def material(self, color):
        key = tuple(color)
        if key not in self.materials:
            self.materials[key] = PhongMaterial(number_of_light_sources=2, use_shadow=True,
                property_dict={'baseColor':color, 'specularStrength':.18, 'shininess':24})
        return self.materials[key]

    def part(self, parent, pos, size, color, cylinder=False, roll=0):
        mesh = Mesh(self.cylinder if cylinder else self.box, self.material(color))
        transform(mesh, pos, roll=roll, scale=size)
        parent.add(mesh)
        return mesh

    def pivot(self, parent, pos):
        node = Object3D()
        node.set_position(pos)
        parent.add(node)
        return node

    def rover(self, scene):
        root = self.pivot(scene, (0,0,0))
        orange, dark, white = (.93,.48,.10), (.10,.15,.19), (.83,.88,.86)
        self.part(root,(0,.88,0),(1.65,.48,1.18),orange)
        self.part(root,(-.18,1.20,0),(1.05,.18,1.0),dark)
        # Painel solar: pequenas células de caixas, sem modelo externo.
        for x in (-.5,-.18,.14):
            for z in (-.31,0,.31):
                self.part(root,(x,1.30,z),(.27,.025,.26),(.08,.28,.40))
        wheels=[]
        for x in (-.58,.58):
            for z in (-.73,.73):
                p=self.pivot(root,(x,.40,z)); wheels.append(p)
                self.part(p,(0,0,0),(.38,.24,.38),dark,True,pi/2)
                # cylinder y -> z; hub and spoke reveal spin on symmetric wheels
                wheels[-1].children_list[0].local_matrix = (Matrix.make_rotation_x(pi/2) @ np.diag([.38,.24,.38,1]))
                self.part(p,(0,0,.14 if z>0 else -.14),(.48,.08,.03),white)
        self.part(root,(.4,1.55,0),(.10,.95,.10),white)
        sensor=self.pivot(root,(.4,2.02,0))
        self.part(sensor,(.12,0,0),(.48,.27,.42),orange)
        self.part(sensor,(.37,0,0),(.04,.16,.27),(.1,.85,.86))
        self.part(root,(.84,.93,.36),(.03,.16,.23),white)
        self.part(root,(.84,.93,-.36),(.03,.16,.23),white)
        return root, wheels, sensor

    def dinosaur(self, scene):
        root=self.pivot(scene,(0,0,0))
        green=(.25,.54,.31); light=(.54,.72,.34); dark=(.12,.28,.19)
        self.part(root,(0,1.38,0),(1.0,1.13,1.5),green)
        self.part(root,(0,1.25,.76),(.68,.75,.08),light)
        self.part(root,(0,2.05,.42),(.70,.65,.72),green)
        self.part(root,(0,2.48,.83),(.94,.69,1.05),green)
        self.part(root,(0,2.24,1.19),(.92,.18,.56),light)
        self.part(root,(0,2.32,1.37),(.75,.035,.04),dark)
        for x in (-.48,.48):
            self.part(root,(x,2.61,1.02),(.04,.21,.24),(.95,.96,.81))
            self.part(root,(x*1.05,2.61,1.08),(.025,.11,.11),(.04,.07,.06))
            self.part(root,(x*1.1,1.66,.72),(.22,.20,.55),green)
        legs=[]
        for x in (-.42,.42):
            p=self.pivot(root,(x,.92,-.12)); legs.append(p)
            self.part(p,(0,-.38,0),(.35,.73,.43),green)
            self.part(p,(0,-.78,.22),(.41,.20,.83),light)
        tail=self.pivot(root,(0,1.30,-.72))
        self.part(tail,(0,0,-.58),(.57,.52,1.2),green)
        self.part(tail,(0,.08,-1.35),(.34,.31,.60),light)
        for z,y in ((-.45,2.02),(-.1,2.04),(-1.0,1.65),(-1.6,1.58)):
            self.part(root if z>-.6 else tail,(0,y,z) if z>-.6 else (0,y-1.3,z+.72),(.16,.30,.24),dark)
        return root, legs, tail
