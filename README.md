<div align="center">

# 🦖 Órbita — Parque Jurássico

**Um encontro coordenado entre um rover explorador e um dinossauro de blocos.**

Computação Gráfica · Modelagem 3D · Animação · Iluminação · Shadow mapping

</div>

| Tecnologia | Ambiente verificado | Execução |
|:---:|:---:|:---:|
| Python · Pygame · OpenGL | Windows · Python 3.12 x64 · OpenGL 3.3 | Local, após instalar as dependências |

**Navegação:** [Equipe](#equipe) · [Cena](#cena-e-interação) · [Execução](#execução) · [Controles](#controles) · [Implementação](#implementação) · [Fontes](#fontes-e-créditos)

## Equipe

| Integrante | Tema | Organização das responsabilidades |
|---|---|---|
| **Phillipe Almeida Faria** | 🦖 Dinossauro de blocos | Corpo e articulações; caminhada, cauda e reação ao reconhecimento; materiais e folga na virada. |
| **Thiago Ferreira de Souza Junior** | 🛞 Rover explorador | Chassi, rodas e sensor; deslocamento, luz de reconhecimento e controles; aproximação e acompanhamento. |
| **Dupla** | Integração | Cenário, ação coordenada, iluminação, sombras, revisão da execução e documentação. |

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

<details>
<summary><strong>Proveniência e adaptações do framework</strong></summary>

Snapshot da branch `main` consultado em **04/11/2026**, sem revisão Git específica registrada. SHA-256 do ZIP-fonte:

```text
485be3a402fbde37b045421177a1eba822ea6dbf48e7da9e008a4b7fa0a50d20
```

Não foi encontrada licença declarada na raiz daquele snapshot; não se atribui uma licença inexistente ao código de terceiros. O nome do exemplo de sombras não altera a referência à seção 6.9 do enunciado.

Adaptações: NumPy 2; shaders externos; localização explícita de posição; inversa transposta para normais; profundidade RGBA32F; PCF e bias; validação de atributos; visibilidade; reutilização de matrizes e uniforms. Modelos, coreografia, colisões, scanner, cenário e painel integram a implementação específica deste projeto.

</details>

### Uso de inteligência artificial

Foi utilizado **OpenAI ChatGPT** no planejamento, desenvolvimento e revisão dos módulos principais, componentes adaptados de `py3d/` e shaders; geração de texturas por scripts; documentação, instalação e validações automatizadas e gráficas. O framework possui atribuição própria. O apoio de IA não substitui a revisão dos integrantes nem o domínio do código na apresentação.
