# Controla as etapas e as poses sem depender do contexto gráfico.
"""Coreografia determinística em segundos; independente de OpenGL e da taxa de quadros."""
from dataclasses import dataclass
from math import pi, sin, isfinite, atan2

# Folga longitudinal em unidades da cena e duração máxima de cada teste de movimento.
FOLLOW_DISTANCE = 3.8
MAX_COLLISION_STEP = 1/120

# Interpola de zero a um com derivada nula nas extremidades.
def smoothstep(t):
    """Interpolação com velocidade nula nas extremidades, sem ultrapassar o destino."""
    t = max(0.0, min(1.0, t))
    return t*t*(3-2*t)

# A ordem determina as transições e os índices mostrados pelo HUD.
STAGES = ('APROXIMACAO', 'RECONHECIMENTO', 'RESPOSTA', 'ACOMPANHAMENTO', 'CONCLUIDO')

# Reúne posições, ângulos e deslocamentos calculados para um instante.
@dataclass
class Pose:
    rover_x: float
    dino_x: float
    dino_yaw: float
    sensor_yaw: float
    wheel_angle: float
    leg_angle: float
    tail_angle: float
    body_bob: float = 0.0
    head_yaw: float = 0.0
    jaw_angle: float = 0.0

# Máquina de estados da interação. A renderização recebe apenas a pose resultante.
class Simulation:
    """Transições causais: distância -> sensor concluído -> virada -> acompanhamento.

    O dt excedente é consumido pelo estado seguinte para não acumular erro por FPS.
    A animação termina; R reinicia sem teletransporte automático durante a exibição.
    """
    # Começa na mesma configuração usada pelo comando de reinício.
    def __init__(self):
        self.reset()

    # Recoloca os personagens no início e zera relógios, deslocamento e bloqueios.
    def reset(self):
        self.stage = 0
        self.elapsed = 0.0
        self.time = 0.0
        self.paused = False
        self.rover_x = -7.0
        self.dino_x = 0.0
        self.distance = 0.0
        self.collision_blocked = False
        self.prevented_collisions = 0

    # Traduz o índice da etapa no nome mostrado nos relatórios.
    @property
    def name(self):
        return STAGES[self.stage]

    # Consome dt em segundos. Quando há detector, valida os subpassos antes de aceitá-los.
    def update(self, dt, can_advance=None):
        if not isfinite(dt) or dt < 0:
            raise ValueError('dt deve ser finito e nao negativo')
        if self.paused or self.stage == 4:
            return
        if can_advance is not None:
            # Check the path in short intervals, not only the final frame pose.
            # Time, wheels, and state transitions are rolled back together.
            while dt > 1e-10 and self.stage < 4:
                step=min(dt,MAX_COLLISION_STEP)
                # Guarda todos os valores da simulação para restaurar um avanço recusado.
                before=vars(self).copy()
                self.update(step)
                if not can_advance(self.pose()):
                    vars(self).update(before)
                    self.collision_blocked=True
                    self.prevented_collisions+=1
                    can_advance(self.pose())  # restore the scene hierarchy too
                    return
                self.collision_blocked=False
                dt-=step
            return
        while dt > 1e-10 and self.stage < 4:
            # Cada etapa consome apenas seu tempo restante. A sobra passa à etapa seguinte.
            duration = (5.0, 2.0, 2.0, 7.0)[self.stage]
            step = min(dt, duration - self.elapsed)
            self.elapsed += step
            self.time += step
            dt -= step
            if self.stage == 0:
                self.rover_x = -7 + (7-FOLLOW_DISTANCE)*smoothstep(self.elapsed/5)
                self.distance = self.rover_x + 7
            # No acompanhamento, a posição do rover depende da posição do dinossauro.
            elif self.stage == 3:
                self.dino_x = 4.55*smoothstep(self.elapsed/7)
                self.rover_x = self.dino_x - FOLLOW_DISTANCE
                self.distance = (7-FOLLOW_DISTANCE) + self.dino_x
            if self.elapsed >= duration - 1e-9:
                # Chegada com folga para a cauda; reconhecimento e virada concluídos;
                # e destino atingido, respectivamente. Não são movimentos desconexos.
                self.stage += 1
                self.elapsed = 0.0

    # Calcula a orientação e as articulações a partir da etapa e do tempo acumulado.
    def pose(self):
        yaw = 0 if self.stage < 2 else (pi/2 * smoothstep(self.elapsed/2) if self.stage == 2 else pi/2)
        sensor = pi/2 if self.stage == 1 else 0
        if self.stage == 1:
            sensor = atan2(1.5,FOLLOW_DISTANCE-.4)*sin(pi * self.elapsed/2)**2
        # A amplitude da passada aumenta no início e diminui antes da parada.
        walking = self.stage == 3
        envelope = min(smoothstep(self.elapsed/.6),smoothstep((7-self.elapsed)/.6)) if walking else 0
        head = -.32*sin(pi*self.elapsed/2)**2 if self.stage == 1 else 0
        jaw = .20*sin(pi*self.elapsed/2)**2 if self.stage == 2 else 0
        # A roda usa distância dividida pelo raio. Senos controlam pernas, cauda e oscilação.
        return Pose(self.rover_x, self.dino_x, yaw, sensor,
                    -self.distance/.38,
                    .30*sin(self.elapsed*7)*envelope,
                    .18*sin(self.time*3),
                    .045*sin(self.elapsed*14)**2*envelope, head, jaw)
