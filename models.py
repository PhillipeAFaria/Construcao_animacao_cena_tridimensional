"""Modelos autorais por composição das geometrias do framework do livro."""
from math import pi, sin, cos
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
                hub=self.part(p,(0,0,.16 if z>0 else -.16),(.14,.035,.14),orange,True)
                hub.rotate_x(pi/2)
                for angle in range(0,360,60):
                    a=angle*pi/180
                    tread=self.part(p,(.36*cos(a),.36*sin(a),0),(.13,.07,.28),(.16,.21,.23))
                    tread.rotate_z(a)
        self.part(root,(.4,1.55,0),(.10,.95,.10),white)
        sensor=self.pivot(root,(.4,2.02,0))
        self.part(sensor,(.12,0,0),(.48,.27,.42),orange)
        self.part(sensor,(.37,0,0),(.04,.16,.27),(.1,.85,.86))
        # Duas lentes e antena distinguem o sensor de uma simples caixa.
        for z in (-.11,.11):
            lens=self.part(sensor,(.40,0,z),(.075,.035,.075),dark,True)
            lens.rotate_z(pi/2)
            self.part(sensor,(.424,0,z),(.012,.08,.08),(.28,.93,.89))
        self.part(root,(-.62,1.57,.35),(.035,.60,.035),dark)
        self.part(root,(-.62,1.9,.35),(.08,.08,.08),orange)
        for z in (-.58,.58):
            self.part(root,(0,.69,z),(1.25,.10,.065),white)
        self.part(root,(.86,.68,0),(.10,.13,1.13),dark)
        self.part(root,(.84,.93,.36),(.03,.16,.23),white)
        self.part(root,(.84,.93,-.36),(.03,.16,.23),white)
        return root, wheels, sensor

    def dinosaur(self, scene):
        root=self.pivot(scene,(0,0,0))
        green=(.25,.54,.31); light=(.54,.72,.34); dark=(.12,.28,.19)
        self.part(root,(0,1.38,0),(1.0,1.13,1.5),green)
        self.part(root,(0,1.25,.76),(.68,.75,.08),light)
        self.part(root,(0,2.05,.42),(.70,.65,.72),green)
        head=self.pivot(root,(0,2.15,.51)); self.head=head
        self.part(head,(0,.33,.32),(.94,.69,1.05),green)
        jaw=self.pivot(head,(0,.09,.40)); self.jaw=jaw
        self.part(jaw,(0,0,.28),(.92,.18,.64),light)
        self.part(head,(0,.17,.86),(.75,.06,.04),dark)
        for x in (-.31,-.1,.1,.31):
            self.part(head,(x,.13,.83),(.08,.14,.09),(.96,.91,.68))
        for x in (-.48,.48):
            self.part(head,(x,.46,.51),(.04,.23,.27),(.95,.96,.81))
            self.part(head,(x*1.05,.46,.57),(.025,.13,.12),(.04,.07,.06))
            self.part(head,(x,.61,.50),(.09,.08,.31),dark)
            self.part(head,(x*.7,.44,.85),(.09,.07,.04),dark)
            self.part(root,(x*1.1,1.66,.72),(.22,.20,.55),green)
        legs=[]
        for x in (-.42,.42):
            p=self.pivot(root,(x,.92,-.12)); legs.append(p)
            self.part(p,(0,-.38,0),(.35,.73,.43),green)
            self.part(p,(0,-.78,.22),(.41,.20,.83),light)
            for dx in (-.12,0,.12):
                self.part(p,(dx,-.77,.66),(.075,.10,.16),(.93,.86,.60))
        tail=self.pivot(root,(0,1.30,-.72))
        self.part(tail,(0,0,-.58),(.57,.52,1.2),green)
        self.part(tail,(0,.08,-1.35),(.34,.31,.60),light)
        self.part(tail,(0,.13,-1.76),(.17,.17,.32),green)
        # Encaixes de brinquedo reforçam a identidade do dinossauro de blocos.
        for x in (-.24,.24):
            for z in (-.35,.05):
                self.part(root,(x,1.99,z),(.11,.10,.11),light,True)
        for z,y in ((-.45,2.02),(-.1,2.04),(-1.0,1.65),(-1.6,1.58)):
            self.part(root if z>-.6 else tail,(0,y,z) if z>-.6 else (0,y-1.3,z+.72),(.16,.30,.24),dark)
        return root, legs, tail
