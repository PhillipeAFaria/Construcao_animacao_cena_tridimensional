"""Colisores compostos: AABBs de cada peça, recalculadas pelas matrizes da hierarquia.

Não depende de OpenGL. As caixas envolvem os vértices reais de cada malha e
incluem a cauda e o sensor; são conservadoras para peças giradas/cilindros.
"""
from itertools import product
import numpy as np

SAFETY_MARGIN = .10

def overlap_mask(a_min,a_max,b_min,b_max,margin=0.0):
    return np.all((a_min[:,None,:] < b_max[None,:,:]+margin) &
                  (b_min[None,:,:] < a_max[:,None,:]+margin),axis=2)

class CompoundCollider:
    def __init__(self,root,name):
        self.root=root
        self.name=name
        self.meshes=[node for node in root.descendant_list if hasattr(node,'geometry')]
        self.corners=[]
        for mesh in self.meshes:
            vertices=np.asarray(mesh.geometry.attribute_dict['vertexPosition'].data,dtype=float)
            low,high=vertices.min(axis=0),vertices.max(axis=0)
            corners=np.array([[*(high[k] if bit[k] else low[k] for k in range(3)),1.]
                              for bit in product((0,1),repeat=3)])
            self.corners.append(corners)
        self.corners=np.asarray(self.corners)

    def boxes(self):
        matrices={}
        for node in self.root.descendant_list:
            parent=matrices.get(id(node.parent))
            matrices[id(node)]=node.global_matrix if parent is None else parent@node.local_matrix
        transforms=np.asarray([matrices[id(mesh)] for mesh in self.meshes])
        points=np.einsum('nij,nkj->nki',transforms,self.corners)[:,:,:3]
        return points.min(axis=1),points.max(axis=1)

    def part_name(self,index):
        node=self.meshes[index]
        labels=[]
        while node is not None and node is not self.root:
            if hasattr(node,'collision_name'):labels.append(node.collision_name)
            node=node.parent
        return self.name+'/'+('/'.join(reversed(labels)) if labels else f'peca_{index}')

class CollisionWorld:
    def __init__(self,rover,dinosaur,margin=SAFETY_MARGIN):
        self.rover=CompoundCollider(rover,'rover')
        self.dinosaur=CompoundCollider(dinosaur,'dinossauro')
        self.margin=margin
        self.last_contacts=[]
        self.checks=0

    def contacts(self,margin=None):
        self.checks+=1
        margin=self.margin if margin is None else margin
        a_min,a_max=self.rover.boxes();b_min,b_max=self.dinosaur.boxes()
        # Broad phase: envelopes of the two complete models.
        if not overlap_mask(a_min.min(axis=0,keepdims=True),a_max.max(axis=0,keepdims=True),
                            b_min.min(axis=0,keepdims=True),b_max.max(axis=0,keepdims=True),margin)[0,0]:
            self.last_contacts=[]
            return []
        pairs=np.argwhere(overlap_mask(a_min,a_max,b_min,b_max,margin))
        self.last_contacts=[(self.rover.part_name(i),self.dinosaur.part_name(j)) for i,j in pairs]
        return self.last_contacts

    def clearance(self):
        a_min,a_max=self.rover.boxes();b_min,b_max=self.dinosaur.boxes()
        delta=np.maximum(np.maximum(a_min[:,None,:]-b_max[None,:,:],
                                     b_min[None,:,:]-a_max[:,None,:]),0)
        return float(np.linalg.norm(delta,axis=2).min())
