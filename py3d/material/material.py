# Armazena programa, uniforms e opções de desenho de um material.
import OpenGL.GL as GL

from py3d.core.uniform import Uniform
from py3d.core.utils import Utils


class Material:
    # Cria o programa e registra as matrizes comuns de transformação.
    def __init__(self, vertex_shader_code, fragment_shader_code):
        self._program_ref = Utils.initialize_program(vertex_shader_code, fragment_shader_code)
        # Store Uniform objects, indexed by name of associated variable in shader.
        # Each shader typically contains these uniforms; values will be set during render process from Mesh / Camera.
        self._uniform_dict = {
            "modelMatrix":      Uniform("mat4", None),
            "viewMatrix":       Uniform("mat4", None),
            "projectionMatrix": Uniform("mat4", None),
        }
        # Store OpenGL render settings, indexed by variable name
        self._setting_dict = {
            "drawStyle": GL.GL_TRIANGLES
        }

    # Retorna o seguinte dado — identificador do programa GLSL.
    @property
    def program_ref(self):
        return self._program_ref

    # Retorna o seguinte dado — opções de desenho do material.
    @property
    def setting_dict(self):
        return self._setting_dict

    # Retorna o seguinte dado — uniforms registrados por nome.
    @property
    def uniform_dict(self):
        return self._uniform_dict

    # Registra o tipo e o valor inicial que serão enviados ao programa.
    def add_uniform(self, data_type, variable_name, data):
        self._uniform_dict[variable_name] = Uniform(data_type, data)

    # Resolve as localizações após compilar e vincular o programa.
    def locate_uniforms(self):
        """ Initialize all uniform variable references """
        for variable_name, uniform_object in self._uniform_dict.items():
            uniform_object.locate_variable(self._program_ref, variable_name)

    # Aplica ao OpenGL as opções de desenho próprias deste material.
    def update_render_settings(self):
        """ Configure OpenGL with render settings """
        pass

    # Aplica valores fornecidos pelo chamador às opções conhecidas.
    def set_properties(self, property_dict):
        """
        Convenience method for setting multiple material "properties"
        (uniform and render setting values) from a dictionary
        """
        if property_dict:
            for name, data in property_dict.items():
                # Update uniforms
                if name in self._uniform_dict.keys():
                    self._uniform_dict[name].data = data
                # Update render settings
                elif name in self._setting_dict.keys():
                    self._setting_dict[name] = data
                # Unknown property type
                else:
                    raise Exception("Material has no property named: " + name)
