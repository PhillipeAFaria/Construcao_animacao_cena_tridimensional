# Carrega o material texturizado que compõe o HUD.
from pathlib import Path
import OpenGL.GL as GL

from py3d.material.material import Material


class TextureMaterial(Material):
    # Associa a imagem e os parâmetros de cor e UV ao programa do HUD.
    def __init__(self, texture, property_dict=None):
        vertex_shader_code = (Path(__file__).resolve().parents[2] / "shaders/hud.vert").read_text()

        fragment_shader_code = (Path(__file__).resolve().parents[2] / "shaders/hud.frag").read_text()
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.add_uniform("sampler2D", "textureSampler", [texture.texture_ref, 1])
        self.add_uniform("vec2", "repeatUV", [1.0, 1.0])
        self.add_uniform("vec2", "offsetUV", [0.0, 0.0])
        self.locate_uniforms()
        # Render both sides?
        self.setting_dict["doubleSide"] = True
        # Render triangles as wireframe?
        self.setting_dict["wireframe"] = False
        # line thickness for wireframe rendering
        self.setting_dict["lineWidth"] = 1
        self.set_properties(property_dict)

    # Aplica ao OpenGL as opções de desenho próprias deste material.
    def update_render_settings(self):
        if self.setting_dict["doubleSide"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)
        if self.setting_dict["wireframe"]:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glLineWidth(self.setting_dict["lineWidth"])
