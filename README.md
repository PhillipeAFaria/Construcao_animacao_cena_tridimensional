<div align="center">

# 🦖 Órbita — Parque Jurássico

**Um encontro coordenado entre um rover explorador e um dinossauro de blocos.**

Computação Gráfica · Modelagem 3D · Animação · Iluminação · Shadow mapping

</div>

| Tecnologia | Ambiente verificado | Execução |
|:---:|:---:|:---:|
| Python · Pygame · OpenGL | Windows · Python 3.12 x64 · OpenGL 3.3 | Local, após instalar as dependências |

**Navegação:** [Equipe](#equipe) · [Contribuições](#contribuições-individuais) · [Cena](#cena-e-interação) · [Execução](#execução) · [Controles](#controles) · [Implementação](#implementação) · [Fontes](#fontes-e-créditos)

## Equipe

| Integrante | Tema | Organização das responsabilidades |
|---|---|---|
| **Phillipe Almeida Faria** | 🦖 Dinossauro de blocos | Corpo e articulações; caminhada, cauda e reação ao reconhecimento; materiais e folga na virada. |
| **Thiago Ferreira de Souza Junior** | 🛞 Rover explorador | Chassi, rodas e sensor; deslocamento, luz de reconhecimento e controles; aproximação e acompanhamento. |
| **Dupla** | Integração | Cenário, ação coordenada, iluminação, sombras, revisão da execução e documentação. |

### Phillipe Almeida Faria — Dinossauro de blocos

- **Modelagem:** composição do corpo, pernas, cabeça, mandíbula e cauda com formas geométricas (`models.py`, `Models.dinosaur`).
- **Hierarquia e animação:** organização dos pivôs e movimentos de caminhada, cabeça, mandíbula e cauda (`models.py` e `simulation.py`).
- **Aparência:** revisão das cores por vértice, textura de escamas, materiais e normais do dinossauro (`geometry_tools.py`, `assets/escamas.png` e shaders Phong).
- **Interação e segurança:** conferência da resposta ao reconhecimento e da folga da cauda durante a virada (`simulation.py` e `collision.py`).

### Thiago Ferreira de Souza Junior — Rover explorador

- **Modelagem:** composição do chassi, rodas, painel solar, antena e sensor (`models.py`, `Models.rover`).
- **Animação:** rotação das rodas proporcional ao percurso e varredura do sensor em função do tempo (`simulation.py` e `main.py`).
- **Reconhecimento luminoso:** integração do feixe, halo e iluminação focal direcionada ao dinossauro (`scanner.py` e `shaders/scanner.*`).
- **Controles e deslocamento:** revisão da câmera, pausa, reinício, aproximação e acompanhamento com distância de segurança (`main.py` e `simulation.py`).

### Atividades compartilhadas

- Integração dos personagens e das etapas coordenadas na cena.
- Revisão do cenário, texturas, iluminação direcional e shadow mapping.
- Conferência da execução, das colisões e da documentação.
- Estudo da aplicação integrada para a demonstração e as perguntas individuais.

## Cena e interação

O rover percorre a pista de um parque de pesquisa, para diante do dinossauro e emite um **feixe azul-ciano de reconhecimento**. O dinossauro reage, gira o corpo e começa a caminhar. **O rover só parte após a conclusão da virada**, mantendo distância para a cauda.

```text
  APROXIMAR       RECONHECER        RESPONDER       ACOMPANHAR
    0–5 s            5–7 s             7–9 s           9–16 s
  Rover avança → Sensor ilumina → Dinossauro gira → Ambos avançam
                   Rover para       Rover aguarda     juntos
```

O cenário inclui estação de pesquisa, portal, vegetação, calçada, bancos e lago ornamental. Ao terminar, a cena continua visível; **R** reinicia a sequência.

| Recurso | Comportamento |
|---|---|
| **Animação por tempo** | Velocidade independente do número de quadros, com aceleração/desaceleração suaves. |
| **Interação** | Cada etapa libera a seguinte; os movimentos são coordenados. |
| **Reconhecimento luminoso** | Feixe preso à lente, iluminação focal e resposta da cabeça. |
| **Colisões** | Distância longitudinal de 3,8 unidades; caixas por peça, incluindo cauda e sensor. |
| **Pausa** | Congela personagens e scanner; câmera e visualização continuam disponíveis. |

## Execução

1. **Extraia** a pasta completa do ZIP.
2. Abra **`PREPARAR_AMBIENTE.bat`** e aguarde a confirmação de sucesso.
3. Abra **`INICIAR.bat`**.

> **Requisitos:** Python 3.10–3.13 x64 e GPU/driver com OpenGL 3.3. Recomendado: Python 3.12 x64. A preparação requer internet e cria `.venv` automaticamente; o uso posterior é local.

<details>
<summary><strong>Instalação manual e solução de problemas</strong></summary>

No terminal, dentro da pasta do projeto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Se não houver Python compatível, instale Python 3.12 x64 com o launcher `py`. Se a janela não abrir, execute pelo terminal para consultar o erro e confira o suporte a OpenGL do driver. Não é necessário instalar PyOpenGL_accelerate. Outras plataformas não foram verificadas.

</details>

## Controles

| Teclas | Ação | Teclas | Ação |
|---|---|---|---|
| **Espaço** | Pausar/retomar | **R** | Reiniciar |
| **Setas** | Orbitar a câmera | **W / S** ou roda do mouse | Aproximar/afastar |
| **A / D** | Deslocar o alvo em X | **Q / E** | Baixar/elevar o alvo |
| **1 / 2 / 3** | Vistas geral, próxima e superior | **C** | Alternar acompanhamento |
| **Home** | Restaurar a câmera | **[ / ]** | Velocidade de 0,25× a 2× |
| **L** | Repetição automática | **H** | Mostrar/ocultar ajuda |
| **F11** | Alternar entre janela e tela cheia | | |
| **F12** | Salvar captura¹ | **Esc** | Encerrar |

¹ Captura criada sob demanda em `evidencias/captura.png`. Reiniciar preserva as preferências de câmera e aparência.

<details>
<summary><strong>Laboratório visual — comparações para a apresentação</strong></summary>

| Tecla | Comparação |
|---|---|
| **F1** | Abrir/fechar o laboratório |
| **F2** | Com/sem sombra projetada, mantendo a iluminação |
| **F3** | Com/sem contribuição das cores por vértice |
| **F4** | Texturas originais ou grade UV |
| **F5** | Filtros NEAREST, LINEAR e mipmaps |
| **F6** | Foco nos personagens, reduzindo brilho/saturação do ambiente |
| **F7** | Materiais da cena em cinza |
| **F8** | Superfícies preenchidas ou malha triangulada |

Os modos são opcionais e não alteram a coreografia. Para demonstrar, pause durante o reconhecimento, mova a câmera e compare os recursos.

</details>

## Implementação

### Estrutura da pasta

```text
Entrega_Final_Rover_Dinossauro/
├── README.md                 Guia da entrega, controles, explicações e créditos
├── PREPARAR_AMBIENTE.bat     Abre a preparação do ambiente no Windows
├── preparar.ps1              Localiza Python, cria .venv e instala dependências
├── INICIAR.bat               Executa main.py com o Python do ambiente local
├── requirements.txt          Versões de Pygame, PyOpenGL e NumPy
├── main.py                   Entrada, câmera, eventos, cena e painel
├── models.py                 Rover, dinossauro e transformações de suas peças
├── simulation.py             Etapas, tempo e cálculo da pose
├── collision.py              Caixas de colisão e verificação de contatos
├── scanner.py                Luz e feixe de reconhecimento
├── scenery.py                Decoração e agrupamento das malhas estáticas
├── sky.py                    Fundo de céu
├── appearance.py             Opções do laboratório visual
├── geometry_tools.py         Gradientes por vértice
├── py3d/
│   ├── core/                 Matrizes, atributos, uniforms e compilação
│   ├── core_ext/             Grafo, câmeras, malhas, texturas e renderização
│   ├── geometry/             Construção e organização das primitivas
│   ├── light/                Dados de luz e recursos de sombra
│   └── material/             Programas e parâmetros de aparência
├── shaders/                  Cinco pares GLSL de vértice e fragmento
└── assets/                   Sete PNGs carregados durante a execução
```

`.venv/` é criada pela preparação. `evidencias/` é criada sob demanda quando se salva uma captura ou se executa a opção `--validate`.

### Como acompanhar um quadro

1. **Entrada.** `INICIAR.bat` chama `main.py`. A classe `Application` abre o contexto OpenGL antes de alocar buffers, texturas e programas.
2. **Atualização.** `Application.run` lê eventos, obtém o intervalo do relógio Pygame e chama `Simulation.update`. O fator de velocidade afeta o tempo da simulação. A câmera continua usando o tempo real.
3. **Pose e colisão.** `Simulation.pose` calcula posições e ângulos. `Application.apply_pose` aplica as matrizes às raízes e aos pivôs. `can_advance` consulta `CollisionWorld` a cada subpasso. Uma colisão rejeita a pose candidata e restaura o estado anterior.
4. **Desenho.** `Application.draw_scene` atualiza o scanner, desenha o céu e chama `Renderer.render` para as passagens de sombras e cor. O feixe usa a profundidade já desenhada para respeitar a oclusão da cena.
5. **Apresentação.** `HUD.draw` compõe o painel e `pygame.display.flip` apresenta o quadro. F12 lê os pixels do quadro completo para salvar a captura.

<details>
<summary><strong>Arquivos internos do framework e imagens</strong></summary>

| Pasta | Arquivos e papel |
|---|---|
| `py3d/core/` | `matrix.py` gera matrizes. `attribute.py` carrega VBOs e configura atributos. `uniform.py` envia valores ao GLSL. `utils.py` compila e vincula os shaders. |
| `py3d/core_ext/` | `object3d.py` mantém a hierarquia. `scene.py` define a raiz. `mesh.py` une geometria e material no VAO. `camera.py` calcula vista e projeção. `texture.py` carrega imagens e filtros. `render_target.py` prepara o framebuffer. `renderer.py` executa as passagens de desenho. |
| `py3d/geometry/` | `geometry.py` organiza atributos. `box.py` e `rectangle.py` geram caixas e retângulos. `parametric.py` amostra superfícies. `cylindrical.py` e `cylinder.py` geram laterais e tampas. `polygon.py` triangula as tampas. |
| `py3d/light/` | `light.py` define dados comuns. `ambient.py` e `directional.py` configuram as duas luzes. `shadow.py` reúne câmera da luz, material de profundidade e mapa. |
| `py3d/material/` | `material.py` registra programa, uniforms e opções. `lighted.py` registra as luzes. `phong.py` parametriza a cena. `depth.py` grava profundidade. `texture.py` parametriza o HUD. |

Os arquivos `__init__.py` identificam os pacotes Python. O código de `py3d/` tem a atribuição indicada em **Fontes e créditos**.

| Imagem | Aplicação |
|---|---|
| `terreno.png` e `asfalto.png` | Piso do parque e superfície da pista, com UV repetidas. |
| `solar.png` e `escamas.png` | Painel solar do rover e superfície do dinossauro. |
| `placa.png` e `estacao.png` | Sinalização do parque e da estação de pesquisa. |
| `grade_uv.png` | Padrão de diagnóstico mostrado com F4. |

**Termos de leitura.** O VBO guarda dados de vértices na GPU. O VAO descreve como o shader lê esses dados. Uniforms recebem parâmetros como matrizes e cores. UV indicam a posição amostrada na imagem. Uma AABB é uma caixa alinhada aos eixos usada como aproximação da peça. O framebuffer organiza os buffers de uma passagem de desenho.

</details>


### Mapa do projeto

| Arquivo ou pasta | Recursos principais |
|---|---|
| `main.py` | `Application`: integração, câmera, eventos e loop; `HUD`: painel e linha do tempo. |
| `models.py` | `Models.rover`, `Models.dinosaur` e `transform`: primitivas e hierarquias. |
| `simulation.py` | `Simulation`: estados, tempo, pausa, poses e rejeição de movimentos inseguros. |
| `collision.py` | `CompoundCollider` e `CollisionWorld`: caixas das peças em coordenadas de mundo. |
| `scanner.py` | `Scanner`: feixe, halo e luz focal presos ao sensor. |
| `scenery.py` · `sky.py` | Parque, agrupamento estático e fundo de céu. |
| `geometry_tools.py` · `appearance.py` | Gradientes por vértice e laboratório visual. |
| `py3d/` | Componentes utilizados do framework: matrizes, buffers, uniforms, cena, geometria, materiais, luzes e renderização. |
| `shaders/` · `assets/` | Fontes GLSL e sete imagens PNG necessárias à execução. |
| `requirements.txt` · arquivos BAT · `preparar.ps1` | Dependências e preparação/inicialização no Windows. |

<details>
<summary><strong>Transformações, shaders, atributos e uniforms</strong></summary>

**Hierarquia:** matriz local `T × Ry × Rx × Rz × S`; matriz global `M_pai × M_local`. Rodas e sensor herdam o movimento do rover; pernas, cabeça, mandíbula e cauda têm pivôs no dinossauro. O agrupamento do ambiente preserva as partes animadas independentes.

| Par de shaders | Função |
|---|---|
| `phong.vert` / `phong.frag` | Transformações, textura, cores, iluminação, sombra e luz focal. |
| `depth.vert` / `depth.frag` | Profundidade da primeira passagem de sombras. |
| `scanner.vert` / `scanner.frag` | Cone translúcido, núcleo e halo emissivo. |
| `sky.vert` / `sky.frag` | Gradiente e formas suaves do céu. |
| `hud.vert` / `hud.frag` | Painel em textura transparente. |

O framework acrescenta `#version 330`. Os atributos usados são `vertexPosition`, `vertexNormal`, `vertexUV` e `vertexColor`. `Attribute` envia os dados aos VBOs; `Mesh` associa os atributos ao VAO e valida suas quantidades. Cores e UV chegam interpoladas ao fragment shader.

| Uniforms | Uso |
|---|---|
| `modelMatrix`, `viewMatrix`, `projectionMatrix` | `P × V × M × posição`; perspectiva na câmera principal e projeção ortográfica na câmera da luz. |
| `baseColor`, `useVertexColors`, `useTexture`, `textureSampler` | Cor-base, cor interpolada e imagem na unidade de textura 1. |
| `repeatUV`, `offsetUV` | `UV = vertexUV × repeatUV + offsetUV`; repetição [9,7] no terreno e [9,2.3] na pista. |
| `light0`, `light1`, `viewPosition`, `specularStrength`, `shininess` | Luz ambiente/direcional e brilho Phong. |
| `shadow0` | Matrizes da luz, profundidade na unidade 3, direção, intensidade e bias. |
| `scannerActive`, `scannerPosition`, `scannerDirection`, `scannerColor` | Intensidade, origem, direção e cor da luz de reconhecimento. |
| `intensity`, `effectTime`, `glowColor`, `beamMode` | Representação emissiva do feixe. |
| `focusFactor`, `grayScale` | Comparações de foco e cinza. |

As normais usam a **inversa transposta** da matriz de modelo para suportar escala não uniforme. O suporte herdado a bump mapping está desativado.

</details>

### Iluminação ≠ sombra projetada

| Sombreamento da superfície | Sombra projetada |
|---|---|
| Resposta do material à luz, conforme as normais e os termos ambiente, difuso e especular. | Bloqueio da luz por uma geometria antes de alcançar outra superfície. |
| Calculado pelo material Phong. | Calculada por **shadow mapping**, conforme a seção 6.9 indicada no enunciado. |

```text
  1. CÂMERA DA LUZ                   2. CÂMERA PRINCIPAL
  Cena → mapa de profundidade  ───→  Comparação de profundidades → sombra
```

O mapa **2048×2048**, com profundidade gravada como cor **RGBA32F** e renderbuffer de profundidade, é atualizado a cada quadro. **PCF 3×3 e bias** reduzem artefatos. Ordem de desenho: céu → cena iluminada com sombras → feixe → painel.

**Colisões:** AABBs compostas por peça, margem de 0,10 unidade e subpassos de até 1/120 s. Um avanço inseguro restaura tempo, estado, rodas e articulações à última pose aceita.

**Limites:** não há motor de física, quique ou colisão da câmera com o cenário. Lago e céu são estilizados. O feixe usa mistura aditiva e teste de profundidade, sem uma segunda sombra focal, bloom ou dispersão física no ar. O modo cinza não é um modelo fisiológico de visão.

## Fontes e créditos

- **Livro:** Stemkoski, L.; Pascale, M. *Developing Graphics Frameworks with Python and OpenGL*. CRC Press. [DOI](https://doi.org/10.1201/9781003181378).
- **Framework:** [PyOpenGL-Pygame-Stemkoski-Pascale-2021](https://github.com/ax-va/PyOpenGL-Pygame-Stemkoski-Pascale-2021), componentes de `py3d/` e exemplo `examples/6-5--shadows.py`.
- **Disciplina:** enunciado *Trabalho - Computacao Grafica.pdf* e aulas *Desenhando Formas com preenchimento*, *Trabalhando Texturas* e *Visâo - Computação Gráfica*: interpolação, UV, filtros, atenção e contraste.
- **Bibliotecas:** [Pygame](https://www.pygame.org/docs/), [PyOpenGL](https://pyopengl.sourceforge.net/documentation/) e [NumPy](https://numpy.org/doc/).
- **Texturas:** os sete PNGs são originais, gerados previamente por scripts Python/Pillow com apoio de IA, sem copiar figuras dos PDFs. As fontes das placas foram rasterizadas; seus arquivos não são distribuídos.

### Uso de inteligência artificial

A documentação e os comentários explicativos do código também foram preparados com apoio de IA.

Foi utilizado **OpenAI ChatGPT** no planejamento, desenvolvimento e revisão dos módulos principais, componentes adaptados de `py3d/` e shaders; geração de texturas por scripts; documentação, instalação e validações automatizadas e gráficas. O framework possui atribuição própria. O apoio de IA não substitui a revisão dos integrantes nem o domínio do código na apresentação.
