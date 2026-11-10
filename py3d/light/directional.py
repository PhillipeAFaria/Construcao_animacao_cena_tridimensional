# Representa luz com raios paralelos e direção definida pela orientação do nó.
from py3d.light.light import Light


class DirectionalLight(Light):
    # Define o tipo direcional, a cor e a orientação inicial.
    def __init__(self, color=(1, 1, 1), direction=(0, -1, 0)):
        super().__init__(Light.DIRECTIONAL)
        self._color = color
        self.set_direction(direction)
