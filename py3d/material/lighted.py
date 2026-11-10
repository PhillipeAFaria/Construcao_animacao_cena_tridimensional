# Registra as luzes e fornece a interface de um material iluminado.
from py3d.material.material import Material


class LightedMaterial(Material):
    # Compila o material e registra os uniforms das luzes.
    def __init__(self, number_of_light_sources=1):
        self._number_of_light_sources = number_of_light_sources
        # Properties vertex_shader_code and fragment_shader_code
        # will be defined in inherited classes FlatMaterial, LambertMaterial,
        # and PhongMaterial
        super().__init__(self.vertex_shader_code, self.fragment_shader_code)
        # Add light uniforms to self._uniform_dict
        for i in range(self._number_of_light_sources):
            self.add_uniform("Light", f"light{i}", None)

    # Gera as declarações GLSL para a quantidade configurada de luzes.
    @property
    def declaring_light_uniforms_in_shader_code(self):
        """ Create a text line with light uniforms to be inserted into a shader code """
        return "\n" + "\n".join(f"\t\t\tuniform Light light{i};"
                                for i in range(self._number_of_light_sources)) + "\n"

    # Gera as instruções GLSL que somam as contribuições das luzes.
    @property
    def adding_lights_in_shader_code(self):
        return "\n" + "\n".join(f"\t\t\t\tlight += calculateLight(light{i}, position, calcNormal);"
                                for i in range(self._number_of_light_sources))

    # Fornece o código GLSL da etapa de vértices para este material.
    @property
    def vertex_shader_code(self):
        raise NotImplementedError("Implement this property for an inheriting class")

    # Fornece o código GLSL da etapa de fragmentos para este material.
    @property
    def fragment_shader_code(self):
        raise NotImplementedError("Implement this property for an inheriting class")
