from pathlib import Path
from py3d.material.material import Material


class DepthMaterial(Material):

    def __init__(self):
        # vertex shader code
        vertex_shader_code = (Path(__file__).resolve().parents[2] / "shaders/depth.vert").read_text()

        # fragment shader code
        fragment_shader_code = (Path(__file__).resolve().parents[2] / "shaders/depth.frag").read_text()
        
        # Initialize shaders
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.locate_uniforms()
