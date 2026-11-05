# Reconhecimento luminoso — versão 1.4

Durante o reconhecimento (5–7 segundos), a lente do rover emite um feixe azul-ciano na direção em que o sensor está apontando. O efeito acompanha a hierarquia real do sensor, cresce/desaparece suavemente e ilumina a superfície atingida do dinossauro. O anel de reconhecimento e a reação da cabeça permanecem sincronizados. A luz se desliga antes da virada e do acompanhamento.

## Implementação

- `scanner.py`: `Scanner.update` extrai a origem da lente e o eixo +X da matriz global do sensor. Não usa uma posição fixa no cenário.
- `ray_distance` limita o raio central pela primeira AABB das peças do dinossauro que ele encontra, ou pelo alcance máximo de 4,8 unidades. É uma aproximação conservadora da superfície, não uma interseção exata de triângulos.
- A representação visível combina um cone translúcido de triângulos, um núcleo fino e um halo na lente. O cone tem raio proporcional ao alcance e acompanha a varredura.
- `shaders/scanner.vert` recebe `vertexPosition`, `vertexUV` e matrizes de modelo/câmera/projeção. O fragment shader usa `glowColor`, `intensity`, `effectTime` e `beamMode` para os três componentes emissivos.
- A passagem do feixe ocorre depois da cena opaca, com teste de profundidade ativo, mistura aditiva e escrita de profundidade desativada. O estado de escrita e o blending normal são restaurados em `finally`, antes de desenhar o HUD ou o quadro seguinte. Assim o feixe não apaga o conteúdo nem atravessa visualmente superfícies na direção da câmera.
- `shaders/phong.frag` acrescenta uma contribuição de luz focal suave com os uniforms `scannerActive`, `scannerPosition`, `scannerDirection` e `scannerColor`. A contribuição usa ângulo, distância e normal da superfície: não é apenas uma linha colorida sobre a imagem.
- As malhas ópticas ficam em uma cena separada: não entram nos colisores dos personagens nem projetam sombras. A luz direcional e seu shadow mapping continuam funcionando.
- Toda a intensidade e a animação interna do feixe usam o tempo da simulação; pausar congela o reconhecimento sem impedir a câmera. O modo em cinza também ajusta a cor da emissão.

## Escopo

É um efeito estilizado, com geometria translúcida e iluminação focal local. Não simula dispersão física de luz no ar, bloom ou uma nova sombra de spotlight. A limitação pelo alvo usa as mesmas caixas conservadoras das peças; objetos estáticos não recebem uma nova passagem de sombras para o scanner. O efeito não altera a distância de 3,8 unidades nem a proteção contra colisões da versão 1.3.

## Validação

`tests/test_scanner.py` verifica origem/eixo/extremidade, direção vertical, rejeição de direção inválida e limite por raio/caixa. `tests/check_scanner.py` executa a GPU real e confere:

- influência da luz sobre a superfície, separada da representação visível do feixe;
- origem seguindo a lente e emissão ativa apenas no reconhecimento;
- pausa preservando o tempo e a origem;
- restauração da escrita de profundidade;
- ausência de erros OpenGL.

Resultados: `evidencias/validacao_scanner.json`. Captura real: `evidencias/13_reconhecimento_luminoso.png`.

Para observar com calma, use `[` para reduzir a velocidade ou Espaço para pausar no reconhecimento. Nenhum novo controle é necessário para ligar a luz: ela acompanha automaticamente a coreografia.
