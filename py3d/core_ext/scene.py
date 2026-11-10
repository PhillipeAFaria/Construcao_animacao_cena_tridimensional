# Fornece o nó raiz do grafo de cena.
from py3d.core_ext.object3d import Object3D


class Scene(Object3D):
    """  Represents the root node of the tree """

    # Inicializa o nó que contém os objetos e luzes.
    def __init__(self):
        super().__init__()
