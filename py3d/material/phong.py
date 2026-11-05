from pathlib import Path
import OpenGL.GL as GL

from py3d.material.lighted import LightedMaterial


class PhongMaterial(LightedMaterial):
    """
    Phong material with at least one light source (or more)
    """
    def __init__(self,
                 texture=None,
                 property_dict=None,
                 number_of_light_sources=1,
                 bump_texture=None,
                 use_shadow=False):
        super().__init__(number_of_light_sources)
        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0])

        if texture is None:
            self.add_uniform("bool", "useTexture", False)
        else:
            self.add_uniform("bool", "useTexture", True)
            self.add_uniform("sampler2D", "textureSampler", [texture.texture_ref, 1])
        self.add_uniform("vec3", "viewPosition", [0, 0, 0])
        self.add_uniform("float", "specularStrength", 1.0)
        self.add_uniform("float", "shininess", 32.0)

        if bump_texture is None:
            self.add_uniform("bool", "useBumpTexture", False)
        else:
            self.add_uniform("bool", "useBumpTexture", True)
            self.add_uniform("sampler2D", "bumpTextureSampler", [bump_texture.texture_ref, 2])
            self.add_uniform("float", "bumpStrength", 1.0)

        if not use_shadow:
            self.add_uniform("bool", "useShadow", False)
        else:
            self.add_uniform("bool", "useShadow", True)
            self.add_uniform("Shadow", "shadow0", None)

        self.locate_uniforms()

        # Render both sides?
        self.setting_dict["doubleSide"] = True
        # Render triangles as wireframe?
        self.setting_dict["wireframe"] = False
        # Set line thickness for wireframe rendering
        self.setting_dict["lineWidth"] = 1
        self.set_properties(property_dict)

    @property
    def vertex_shader_code(self):
        return (Path(__file__).resolve().parents[2] / "shaders/phong.vert").read_text(encoding="utf-8")

    @property
    def fragment_shader_code(self):
        return (Path(__file__).resolve().parents[2] / "shaders/phong.frag").read_text(encoding="utf-8")

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
