# Representa a varredura com iluminação de superfície e um feixe em passagem separada.
"""Feixe emissivo e iluminação de reconhecimento presos ao sensor do rover."""
from pathlib import Path
from math import sin,pi,tan
import numpy as np
import OpenGL.GL as GL
from py3d.core.matrix import Matrix
from py3d.core_ext.scene import Scene
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.geometry.geometry import Geometry
from py3d.geometry.cylinder import CylinderGeometry
from py3d.geometry.rectangle import RectangleGeometry
from py3d.material.material import Material

SHADERS=Path(__file__).resolve().parent/'shaders'

# Cruza intervalos por eixo e retorna o primeiro contato do raio dentro do alcance.
def ray_distance(origin,direction,low,high,limit=4.8):
    # Cada caixa começa com o intervalo do raio limitado ao alcance do sensor.
    enter=np.zeros(len(low));leave=np.full(len(low),limit);valid=np.ones(len(low),dtype=bool)
    for axis in range(3):
        # Componente quase nula indica raio paralelo. Testa se ele está dentro da faixa do eixo.
        if abs(direction[axis])<1e-9:
            valid &= (origin[axis]>=low[:,axis]) & (origin[axis]<=high[:,axis])
        else:
            a=(low[:,axis]-origin[axis])/direction[axis]
            b=(high[:,axis]-origin[axis])/direction[axis]
            enter=np.maximum(enter,np.minimum(a,b));leave=np.minimum(leave,np.maximum(a,b))
    valid &= leave>=enter
    return min(limit,float(enter[valid].min())) if valid.any() else limit

# Cria uma base ortogonal com eixo Z na direção do feixe e escalas de raio e comprimento.
def beam_matrix(origin,direction,length,radius):
    direction=np.asarray(direction,dtype=float)
    norm=np.linalg.norm(direction)
    if norm<1e-9 or length<=0 or radius<=0:
        raise ValueError('O feixe precisa de direcao, comprimento e raio validos.')
    forward=direction/norm
    # Escolhe um vetor auxiliar que não seja paralelo ao feixe.
    reference=np.array([0.,1.,0.]) if abs(forward[1])<.95 else np.array([1.,0.,0.])
    right=np.cross(reference,forward);right/=np.linalg.norm(right)
    up=np.cross(forward,right)
    matrix=np.eye(4)
    matrix[:3,0]=right*radius;matrix[:3,1]=up*radius
    matrix[:3,2]=forward*length;matrix[:3,3]=origin
    return matrix

# Material emissivo usado no cone, no núcleo e no halo.
class ScanMaterial(Material):
    # Carrega os shaders do feixe e registra cor, intensidade, tempo e tipo de peça.
    def __init__(self,mode):
        super().__init__((SHADERS/'scanner.vert').read_text(),(SHADERS/'scanner.frag').read_text())
        self.add_uniform('vec3','glowColor',[.12,.85,1.0])
        self.add_uniform('float','intensity',0.)
        self.add_uniform('float','effectTime',0.)
        self.add_uniform('int','beamMode',mode)
        self.locate_uniforms()

    # Usa mistura aditiva e mantém o buffer de profundidade da cena opaca.
    def update_render_settings(self):
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA,GL.GL_ONE)
        GL.glDepthMask(GL.GL_FALSE)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK,GL.GL_FILL)

# Atualiza o efeito luminoso a partir da lente e do relógio da simulação.
class Scanner:
    # Monta as malhas ópticas numa cena separada e guarda os materiais iluminados.
    def __init__(self,sensor,scene,target):
        self.sensor=sensor
        self.target=target
        self.scene=Scene()
        self.renderer=Renderer()
        self.materials={id(n.material):n.material for n in scene.descendant_list if isinstance(n,Mesh)}
        # Triângulos ligam a ponta na lente a uma circunferência na extremidade.
        cone=Geometry();positions=[];uv=[]
        for i in range(40):
            a=i*2*pi/40;b=(i+1)*2*pi/40
            positions.extend([[0,0,0],[np.cos(a),np.sin(a),1],[np.cos(b),np.sin(b),1]])
            uv.extend([[.5,0],[i/40,1],[(i+1)/40,1]])
        cone.add_attribute('vec3','vertexPosition',positions);cone.add_attribute('vec2','vertexUV',uv)
        self.cone=Mesh(cone,ScanMaterial(0))
        # O núcleo é um cilindro fino cuja altura original em Y passa ao eixo Z.
        core=CylinderGeometry(radius=1,height=1,radial_segments=12)
        core.apply_matrix(Matrix.make_translation(0,0,.5)@Matrix.make_rotation_x(pi/2))
        self.core=Mesh(core,ScanMaterial(1))
        self.halo=Mesh(RectangleGeometry(),ScanMaterial(2))
        self.meshes=(self.cone,self.core,self.halo)
        for mesh in self.meshes:
            mesh.visible=False;mesh.cast_shadow=False;self.scene.add(mesh)
        self.active=False
        self.intensity=0.
        self.origin=np.zeros(3);self.direction=np.array([1.,0,0])

    # Ativa o feixe durante o reconhecimento e o alinha ao eixo +X local do sensor.
    def update(self,sim,gray=False):
        self.active=sim.stage==1
        # A intensidade cresce e decai dentro do intervalo de reconhecimento.
        self.intensity=sin(pi*sim.elapsed/2)**.5 if self.active else 0.
        for mesh in self.meshes:
            mesh.visible=self.active and self.intensity>.001
            mesh.material.uniform_dict['intensity'].data=self.intensity
            mesh.material.uniform_dict['effectTime'].data=sim.time
            mesh.material.uniform_dict['glowColor'].data=([.85,.85,.85] if gray else [.12,.85,1.0])
        # A matriz global fornece a posição da lente e a orientação após o giro do sensor.
        matrix=self.sensor.global_matrix
        self.origin=(matrix@np.array([.455,0,0,1]))[:3]
        self.direction=matrix[:3,0]/np.linalg.norm(matrix[:3,0])
        # A primeira caixa atingida limita o feixe. Sem contato, vale o alcance máximo.
        low,high=self.target.boxes()
        length=max(.05,ray_distance(self.origin,self.direction,low,high))
        self.length=length
        self.cone.local_matrix=beam_matrix(self.origin,self.direction,length,length*tan(.14))
        self.core.local_matrix=beam_matrix(self.origin,self.direction,length,.012)
        for material in self.materials.values():
            uniforms=material.uniform_dict
            uniforms['scannerActive'].data=self.intensity
            uniforms['scannerPosition'].data=self.origin
            uniforms['scannerDirection'].data=self.direction
            uniforms['scannerColor'].data=([.85,.85,.85] if gray else [.18,.82,1.0])

    # Orienta o halo para a câmera e restaura o estado gráfico depois da composição.
    def render(self,camera):
        if not self.active or self.intensity<=.001:return
        # Halo faces the viewer, but its center remains at the physical lens.
        self.halo.local_matrix=Matrix.make_look_at(self.origin,camera.global_position)@np.diag([.32,.32,.32,1])
        try:
            self.renderer.render(self.scene,camera,clear_color=False,clear_depth=False)
        finally:
            GL.glDepthMask(GL.GL_TRUE)
            GL.glBlendFunc(GL.GL_SRC_ALPHA,GL.GL_ONE_MINUS_SRC_ALPHA)
