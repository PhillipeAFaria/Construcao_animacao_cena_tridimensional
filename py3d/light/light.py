# Define os dados comuns das luzes enviados ao shader.
from py3d.core_ext.object3d import Object3D


class Light(Object3D):
    AMBIENT = 1
    DIRECTIONAL = 2
    POINT = 3

    # Inicia tipo, cor e coeficientes de atenuação da luz.
    def __init__(self, light_type=0):
        super().__init__()
        self._light_type = light_type
        self._color = [1, 1, 1]
        self._attenuation = [1, 0, 0]

    # Retorna o seguinte dado — tipo da luz usado no shader.
    @property
    def light_type(self):
        return self._light_type

    # Retorna o seguinte dado — cor da luz.
    @property
    def color(self):
        return self._color

    # Retorna o seguinte dado — coeficientes de atenuação.
    @property
    def attenuation(self):
        return self._attenuation
