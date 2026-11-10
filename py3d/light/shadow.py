# Reúne câmera ortográfica da luz, alvo de renderização e parâmetros de sombra.
import OpenGL.GL as GL

from py3d.core_ext.camera import Camera
from py3d.core_ext.render_target import RenderTarget
from py3d.material.depth import DepthMaterial


class Shadow:
    # Configura câmera da luz, alvo de profundidade e tolerância da comparação.
    def __init__(self,
                 light_source,
                 strength=0.5,
                 resolution=(512, 512),
                 camera_bounds=(-5, 5, -5, 5, 0, 20),
                 bias=0.01):

        # Must be directional light
        self._light_source = light_source
        # Camera used to render scene from perspective of light
        self._camera = Camera()
        left, right, bottom, top, near, far = camera_bounds
        self._camera.set_orthographic(left, right, bottom, top, near, far)
        self._light_source.add(self._camera)
        # Target used during the shadow pass, contains depth texture
        self._render_target = RenderTarget(
            resolution,
            property_dict={"wrap": GL.GL_CLAMP_TO_BORDER}
        )
        # Render only depth data to target texture
        self._material = DepthMaterial()
        # Controls darkness of shadow
        self._strength = strength
        # Used to avoid visual artifacts due to
        # rounding / sampling precision issues
        self._bias = bias

    # Retorna o seguinte dado — tolerância da comparação de profundidade.
    @property
    def bias(self):
        return self._bias

    # Retorna o seguinte dado — câmera ortográfica da luz.
    @property
    def camera(self):
        return self._camera

    # Retorna o seguinte dado — material associado ao objeto.
    @property
    def material(self):
        return self._material

    # Retorna o seguinte dado — luz que origina o mapa.
    @property
    def light_source(self):
        return self._light_source

    # Retorna o seguinte dado — alvo da passagem de profundidade.
    @property
    def render_target(self):
        return self._render_target

    # Retorna o seguinte dado — intensidade da sombra.
    @property
    def strength(self):
        return self._strength

    # Atualiza os parâmetros da câmera da luz no material de profundidade.
    def update_internal(self):
        self._camera.update_view_matrix()
        self._material.uniform_dict["viewMatrix"].data = self._camera.view_matrix
        self._material.uniform_dict["projectionMatrix"].data = self._camera.projection_matrix
