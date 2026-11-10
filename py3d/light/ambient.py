# Representa a parcela uniforme da iluminação da cena.
from py3d.light.light import Light


class AmbientLight(Light):
    # Define o tipo ambiente e sua cor.
    def __init__(self, color=(1, 1, 1)):
        super().__init__(Light.AMBIENT)
        self._color = color
