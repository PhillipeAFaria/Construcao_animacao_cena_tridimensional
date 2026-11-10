# Associa uma geometria a um material através de um VAO.
import OpenGL.GL as GL

from py3d.core_ext.object3d import Object3D


class Mesh(Object3D):
    """
    Contains geometric data that specifies vertex-related properties and material data
    that specifies the general appearance of the object
    """
    # Valida os atributos e monta o VAO para o programa do material.
    def __init__(self, geometry, material):
        super().__init__()
        geometry.validate_attributes()
        self._geometry = geometry
        self._material = material
        # Should this object be rendered?
        self._visible = True
        # Set up associations between attributes stored in geometry
        # and shader program stored in material
        self._vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao_ref)
        for variable_name, attribute_object in geometry.attribute_dict.items():
            attribute_object.associate_variable(material.program_ref, variable_name)
        # Unbind this vertex array object
        GL.glBindVertexArray(0)

    # Retorna o seguinte dado — geometria da malha.
    @property
    def geometry(self):
        return self._geometry

    # Retorna o seguinte dado — material associado ao objeto.
    @property
    def material(self):
        return self._material

    # Retorna o seguinte dado — identificador do VAO.
    @property
    def vao_ref(self):
        return self._vao_ref

    # Retorna o seguinte dado — estado de visibilidade da malha.
    @property
    def visible(self):
        return self._visible

    # Atualiza o seguinte dado — estado de visibilidade da malha.
    @visible.setter
    def visible(self, value):
        self._visible = bool(value)
