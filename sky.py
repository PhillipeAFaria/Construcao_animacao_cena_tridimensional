# Desenha um fundo ortográfico antes da cena tridimensional.
"""Fundo de céu estilizado, desenhado antes da cena tridimensional."""
from pathlib import Path
import OpenGL.GL as GL
from py3d.material.material import Material
from py3d.geometry.rectangle import RectangleGeometry
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.scene import Scene
from py3d.core_ext.camera import Camera
from py3d.core_ext.renderer import Renderer

# Material de fundo calculado no fragment shader.
class SkyMaterial(Material):
    # Lê o par de shaders do céu e localiza as matrizes do programa.
    def __init__(self):
        path=Path(__file__).resolve().parent/'shaders'
        super().__init__((path/'sky.vert').read_text(),(path/'sky.frag').read_text())
        self.locate_uniforms()
    # Desenha o retângulo preenchido e visível pelos dois lados.
    def update_render_settings(self):
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK,GL.GL_FILL)

# Mantém a cena e a câmera ortográfica usadas exclusivamente pelo fundo.
class Sky:
    # Cria um retângulo que cobre a janela no intervalo de −1 a 1.
    def __init__(self):
        self.renderer=Renderer()
        self.scene=Scene();self.camera=Camera()
        self.camera.set_orthographic(-1,1,-1,1,-1,1)
        self.scene.add(Mesh(RectangleGeometry(width=2,height=2),SkyMaterial()))
    # Desenha o fundo e reativa o teste de profundidade para a cena principal.
    def render(self):
        GL.glDisable(GL.GL_DEPTH_TEST)
        try:self.renderer.render(self.scene,self.camera)
        finally:GL.glEnable(GL.GL_DEPTH_TEST)
