# Define projeção e vista para uma câmera posicionada no grafo de cena.
from numpy.linalg import inv

from py3d.core.matrix import Matrix
from py3d.core_ext.object3d import Object3D


class Camera(Object3D):
    """  Represents the virtual camera used to view the scene """
    # Inicia o nó de câmera e suas matrizes de perspectiva e vista.
    def __init__(self, angle_of_view=60, aspect_ratio=1, near=0.1, far=1000):
        super().__init__()
        self._projection_matrix = Matrix.make_perspective(angle_of_view, aspect_ratio, near, far)
        self._view_matrix = Matrix.make_identity()  # inverse of self._matrix

    # Retorna o seguinte dado — matriz de projeção da câmera.
    @property
    def projection_matrix(self):
        return self._projection_matrix

    # Retorna o seguinte dado — matriz de vista atual.
    @property
    def view_matrix(self):
        return self._view_matrix

    # Atualiza a projeção para uma câmera com perspectiva.
    def set_perspective(self, angle_of_view=50, aspect_ratio=1, near=0.1, far=1000):
        self._projection_matrix = Matrix.make_perspective(angle_of_view, aspect_ratio, near, far)

    # Configura projeção paralela para a luz ou uma camada bidimensional.
    def set_orthographic(self, left=-1, right=1, bottom=-1, top=1, near=-1, far=1):
        self._projection_matrix = Matrix.make_orthographic(left, right, bottom, top, near, far)

    # Inverte a transformação global da câmera para levar o mundo ao espaço da vista.
    def update_view_matrix(self):
        self._view_matrix = inv(self.global_matrix)