"""Coreografia determinística em segundos; independente de OpenGL e da taxa de quadros."""
from dataclasses import dataclass
from math import pi, sin

STAGES = ('APROXIMACAO', 'RECONHECIMENTO', 'RESPOSTA', 'ACOMPANHAMENTO', 'CONCLUIDO')

@dataclass
class Pose:
    rover_x: float
    dino_x: float
    dino_yaw: float
    sensor_yaw: float
    wheel_angle: float
    leg_angle: float
    tail_angle: float

class Simulation:
    """Transições causais: distância -> sensor concluído -> virada -> acompanhamento.

    O dt excedente é consumido pelo estado seguinte para não acumular erro por FPS.
    A animação termina; R reinicia sem teletransporte automático durante a exibição.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.stage = 0
        self.elapsed = 0.0
        self.time = 0.0
        self.paused = False
        self.rover_x = -7.0
        self.dino_x = 0.0
        self.distance = 0.0

    @property
    def name(self):
        return STAGES[self.stage]

    def update(self, dt):
        if dt < 0:
            raise ValueError('dt deve ser positivo')
        if self.paused or self.stage == 4:
            return
        while dt > 1e-10 and self.stage < 4:
            duration = (5.0, 2.0, 2.0, 7.0)[self.stage]
            step = min(dt, duration - self.elapsed)
            self.elapsed += step
            self.time += step
            dt -= step
            if self.stage == 0:
                self.rover_x = -7 + self.elapsed
                self.distance += step
            elif self.stage == 3:
                self.dino_x = self.elapsed * .65
                self.rover_x = self.dino_x - 2
                self.distance += step * .65
            if self.elapsed >= duration - 1e-9:
                # Chegada a 2 unidades; reconhecimento concluído; virada concluída;
                # e destino atingido, respectivamente. Não são movimentos desconexos.
                self.stage += 1
                self.elapsed = 0.0

    def pose(self):
        yaw = 0 if self.stage < 2 else (pi/2 * self.elapsed/2 if self.stage == 2 else pi/2)
        sensor = pi/2 if self.stage == 1 else 0
        if self.stage == 1:
            sensor *= sin(pi * self.elapsed/2)
        walking = self.stage == 3
        return Pose(self.rover_x, self.dino_x, yaw, sensor,
                    -self.distance/.38,
                    .30*sin(self.elapsed*7) if walking else 0,
                    .18*sin(self.time*3))
