"""Comparações visuais baseadas nas aulas: atributos, UV, amostragem e atenção."""
from pathlib import Path
import OpenGL.GL as GL
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.texture import Texture

class Appearance:
    FILTER_NAMES=('NEAREST','LINEAR','MIPMAP')

    def __init__(self,scene,focal_nodes):
        self.gradients=True
        self.uv_debug=False
        self.filter_mode=2
        self.focus=False
        self.gray=False
        self.panel=False
        self.wireframe=False
        self.materials={id(n.material):n.material for n in scene.descendant_list if isinstance(n,Mesh)}
        self.focal={id(n.material) for root in focal_nodes for n in root.descendant_list if isinstance(n,Mesh)}
        self.original_colors={key:mat.uniform_dict['useVertexColors'].data for key,mat in self.materials.items()}
        self.original_textures={key:list(mat.uniform_dict['textureSampler'].data)
            for key,mat in self.materials.items() if 'textureSampler' in mat.uniform_dict}
        self.grid=Texture(str(Path(__file__).resolve().parent/'assets/grade_uv.png'))

    @property
    def state(self):
        return (self.panel,self.gradients,self.uv_debug,self.filter_mode,self.focus,self.gray,self.wireframe)

    def refresh(self):
        for key,material in self.materials.items():
            uniforms=material.uniform_dict
            material.setting_dict['wireframe']=self.wireframe
            uniforms['useVertexColors'].data=self.gradients and self.original_colors[key]
            uniforms['focusFactor'].data=1.0 if not self.focus or key in self.focal else .30
            uniforms['grayScale'].data=self.gray
            if key in self.original_textures:
                uniforms['textureSampler'].data=([self.grid.texture_ref,1] if self.uv_debug
                                                  else self.original_textures[key])
        # Altera apenas texturas de cor da cena. O mapa de sombras e o HUD não mudam.
        active=GL.glGetIntegerv(GL.GL_ACTIVE_TEXTURE)
        GL.glActiveTexture(GL.GL_TEXTURE1)
        refs={v[0] for v in self.original_textures.values()} | {self.grid.texture_ref}
        for ref in refs:
            GL.glBindTexture(GL.GL_TEXTURE_2D,ref)
            GL.glTexParameteri(GL.GL_TEXTURE_2D,GL.GL_TEXTURE_MAG_FILTER,
                GL.GL_NEAREST if self.filter_mode==0 else GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D,GL.GL_TEXTURE_MIN_FILTER,
                (GL.GL_NEAREST,GL.GL_LINEAR,GL.GL_LINEAR_MIPMAP_LINEAR)[self.filter_mode])
        GL.glActiveTexture(active)
