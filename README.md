# Órbita — Parque Jurássico

Trabalho de Computação Gráfica: construção e animação de uma cena tridimensional em Python, Pygame e OpenGL, com componentes de uma implementação do framework de Lee Stemkoski e Michael Pascale.

## Integrantes e temas

| **Phillipe Almeida Faria** | **Dinossauro de blocos** |
| **Thiago Ferreira de Souza Junior** | **Rover explorador** |

## Cena e ação conjunta

Um rover explora uma pista de um parque de demonstração. Ao se aproximar do dinossauro, para a uma distância longitudinal de 3,8 unidades, gira o sensor e emite uma luz azul-ciano para reconhecê-lo. O dinossauro reage com a cabeça, gira o corpo e inicia uma caminhada. O rover aguarda a conclusão da virada para acompanhá-lo. O cenário inclui estação de pesquisa, vegetação geométrica, calçada, bancos, portal e lago ornamental.

| Tempo de simulação | Etapa | Ação coordenada |

| 0–5 s | Aproximação | O rover avança 3,2 unidades com rodas girando; o dinossauro movimenta a cauda. |
| 5–7 s | Reconhecimento | O rover para, gira o sensor e ilumina o dinossauro, que responde movimentando a cabeça. |
| 7–9 s | Resposta | O dinossauro gira 90° e movimenta a mandíbula; o rover aguarda. |
| 9–16 s | Acompanhamento | Ambos avançam 4,55 unidades com aceleração/desaceleração suaves; o rover mantém a distância de segurança. |
| Após 16 s | Conclusão | A visualização continua; R reinicia a sequência. |

A interação depende da conclusão de cada etapa: o rover não parte antes de o dinossauro terminar a virada. O movimento é calculado pelo tempo decorrido e não por incrementos fixos por quadro. Colisores compostos pelas peças dos modelos impedem a aceitação de movimentos inseguros, incluindo contatos entre cauda e sensor.

## Instalação e execução

Ambiente recomendado e verificado: **Windows, Python 3.12 de 64 bits e GPU/driver com OpenGL 3.3**. O instalador aceita Python 3.10–3.13 x64. A primeira instalação requer internet para obter as três bibliotecas de `requirements.txt`; depois a aplicação executa localmente.

1. Extraia a pasta completa do ZIP.
2. Execute **PREPARAR_AMBIENTE.bat** e aguarde a confirmação de sucesso.
3. Execute **INICIAR.bat**.

O ambiente `.venv` é criado automaticamente na pasta do projeto, não acompanha a entrega. Se não houver um Python compatível, instale Python 3.12 x64 com o launcher `py` e repita a preparação.

Instalação manual em um terminal aberto nesta pasta:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Em caso de falha na abertura da janela, execute pelo terminal para visualizar o erro e confira o suporte a OpenGL do driver gráfico. Não é necessário instalar PyOpenGL_accelerate. Outras plataformas não foram verificadas nesta entrega.

## Controles

| Tecla | Função |

| Espaço | Pausar/retomar a animação, mantendo a câmera disponível |
| Setas | Orbitar a câmera |
| W / S ou roda do mouse | Aproximar/afastar |
| A / D | Deslocar o alvo da câmera no eixo X |
| Q / E | Baixar/elevar o alvo da câmera |
| 1 / 2 / 3 | Vistas geral, próxima e superior com acompanhamento |
| C | Alternar câmera livre e acompanhamento |
| Home | Restaurar a câmera |
| R | Reiniciar a sequência e remover a pausa |
| [ / ] | Reduzir/aumentar velocidade: 0,25× a 2× |
| L | Alternar repetição automática |
| H | Mostrar/ocultar ajuda |
| F1 | Abrir/fechar laboratório visual |
| F2 | Comparar com/sem sombra projetada, preservando a iluminação |
| F3 | Alternar a contribuição das cores por vértice |
| F4 | Alternar texturas originais e grade UV |
| F5 | Alternar filtros NEAREST, LINEAR e mipmaps |
| F6 | Destacar os personagens reduzindo brilho/saturação do ambiente |
| F7 | Comparar os materiais da cena em cinza |
| F8 | Alternar superfícies preenchidas e malha triangulada |
| F12 | Salvar uma captura em `evidencias/captura.png` |
| Esc | Encerrar |

O scanner liga automaticamente durante o reconhecimento. A pausa congela também sua varredura. Reiniciar com R preserva as preferências de câmera e aparência. Os modos de laboratório são opcionais e não modificam a coreografia.

## Organização dos arquivos e recursos gráficos

| Arquivo ou pasta | Recursos principais |

| `main.py` | `Application`: janela, integração da cena, câmera, eventos e loop; `HUD`: painel e linha do tempo |
| `models.py` | `Models.rover`, `Models.dinosaur`: composição por caixas/cilindros; `transform`: translação, rotação e escala |
| `simulation.py` | `Simulation`: estados da interação, tempo, pausa, poses e rejeição de subpassos inseguros |
| `collision.py` | `CompoundCollider`, `CollisionWorld`: caixas das peças transformadas pela hierarquia |
| `scanner.py` | `Scanner`: origem na lente, orientação do feixe, halo e iluminação focal |
| `scenery.py` | `decorate`: parque; `batch_static`: agrupamento do ambiente estático por material |
| `sky.py` | Fundo de céu em uma passagem separada |
| `geometry_tools.py` | Gradientes de cor por vértice |
| `appearance.py` | Comparações de UV, filtros, cores, foco, cinza e malha |
| `py3d/` | Apenas componentes do framework utilizados: matrizes, atributos, uniforms, cena, câmera, malhas, geometrias, materiais, luzes e renderizador |
| `shaders/` | Fontes GLSL carregadas em tempo de execução |
| `assets/` | Sete imagens PNG necessárias à execução |
| `requirements.txt` | Dependências Python com versões fixadas |
| Arquivos BAT e `preparar.ps1` | Preparação e inicialização no Windows |

### Transformações e hierarquia

As matrizes locais são compostas como `T × Ry × Rx × Rz × S`, com vetores coluna. A matriz global é `M_pai × M_local`. Rodas e sensor herdam a transformação do rover; pernas, cabeça, mandíbula e cauda herdam a transformação do dinossauro, com pivôs próprios. O ambiente estático é agrupado após transformar posições e normais; as partes animadas permanecem independentes.

### Shaders, atributos e uniforms

| Shaders | Uso |

| `phong.vert` / `phong.frag` | Transformações, cores por vértice, UV, textura, materiais iluminados, sombra e luz do scanner |
| `depth.vert` / `depth.frag` | Primeira passagem do shadow mapping, gravando profundidade como cor float |
| `scanner.vert` / `scanner.frag` | Cone translúcido, núcleo e halo luminoso |
| `sky.vert` / `sky.frag` | Gradiente e formas suaves do céu |
| `hud.vert` / `hud.frag` | Textura transparente do painel 2D |

O compilador do framework acrescenta `#version 330`. `vertexPosition` fornece posição local; `vertexNormal`, a normal da superfície; `vertexUV`, a coordenada de textura; e `vertexColor`, a cor que será interpolada pelo rasterizador. A classe `Attribute` envia os dados aos VBOs e `Mesh` associa os atributos ao VAO. A quantidade de elementos dos atributos é validada antes da criação da malha.

Os uniforms `modelMatrix`, `viewMatrix` e `projectionMatrix` realizam `P × V × M × posição`. A câmera principal usa perspectiva; a câmera da luz usa projeção ortográfica. As normais são transformadas pela inversa transposta da matriz de modelo para suportar escala não uniforme.

`baseColor`, `useVertexColors`, `useTexture`, `textureSampler`, `repeatUV` e `offsetUV` controlam a aparência. As imagens são consultadas com `UV = vertexUV × repeatUV + offsetUV`; o terreno usa repetição [9,7] e a pista [9,2.3]. A textura de cor ocupa a unidade 1. `light0`/`light1`, `viewPosition`, `specularStrength` e `shininess` controlam luz ambiente/direcional e brilho Phong.

`shadow0` fornece matrizes da câmera da luz, mapa de profundidade na unidade 3, direção, intensidade e bias. `scannerActive`, `scannerPosition`, `scannerDirection` e `scannerColor` acrescentam iluminação focal no reconhecimento. O feixe usa ainda `intensity`, `effectTime`, `glowColor` e `beamMode`. `focusFactor` e `grayScale` permitem as comparações visuais. O suporte herdado a bump mapping está desativado.

### Iluminação e sombra projetada

O **sombreamento de uma superfície** é a resposta local do material à luz, calculada pelas normais e pelos termos ambiente, difuso e especular. A **sombra projetada** depende de uma geometria bloquear a luz antes que ela alcance outra superfície.

O shadow mapping segue a abordagem indicada na seção 6.9 do livro: primeiro a cena é renderizada pela câmera da luz, com profundidade gravada em uma textura RGBA32F e teste de profundidade em renderbuffer; depois a câmera principal compara a profundidade de cada fragmento com a armazenada. O mapa tem 2048×2048, é atualizado em cada quadro e utiliza PCF 3×3 e bias para reduzir artefatos. Portanto, a sombra acompanha o movimento dos modelos.

A ordem de desenho é: céu, cena com shadow mapping, feixe translúcido e painel. O feixe usa mistura aditiva com teste de profundidade e sem escrever no buffer de profundidade; o estado é restaurado em seguida. Ele não faz parte dos colisores e não projeta uma segunda sombra focal. Não há bloom ou simulação física da luz no ar.

### Colisões e limites

A proteção compara AABBs compostas pelas peças do rover e do dinossauro, incluindo a cauda e o sensor. Usa margem de 0,10 unidade e subpassos de no máximo 1/120 s. Se um avanço é inseguro, tempo, estado, rodas e articulações retornam juntos à última pose aceita. A câmera e a visualização continuam disponíveis.

Não é um motor de física: não há forças ou quique, nem resposta física com a câmera e os objetos estáticos. As caixas são conservadoras. O lago é uma superfície estática com brilho; o céu é estilizado. Os modos de cinza/foco são comparações gráficas, não modelos fisiológicos de visão.

**Phillipe Almeida Faria — Dinossauro de blocos**

- Modelagem do corpo, pernas, cabeça, mandíbula e cauda por composição de formas geométricas.
- Organização das articulações e das relações hierárquicas do dinossauro.
- Animação da caminhada, oscilação da cauda e reação ao reconhecimento do rover.
- Revisão das cores, textura de escamas, normais e materiais do personagem.
- Conferência da folga da cauda durante a virada e da resposta dos colisores.

**Thiago Ferreira de Souza Junior — Rover explorador**

- Modelagem do chassi, rodas, painel solar, antena e sensor.
- Animação das rodas e da varredura do sensor em função do tempo.
- Integração do feixe luminoso e da iluminação focal de reconhecimento.
- Revisão dos controles de câmera, pausa, velocidade e reinício.
- Conferência da aproximação, parada e acompanhamento com distância de segurança.

**Responsabilidades propostas para ambos**

- Integração dos dois modelos e da sequência coordenada no cenário.
- Revisão da iluminação direcional, texturas, shaders e shadow mapping.
- Conferência da execução, das colisões e da documentação, com estudo do código integrado para a apresentação.

## Fontes e atribuição

- STEMKOSKI, Lee; PASCALE, Michael. *Developing Graphics Frameworks with Python and OpenGL*. CRC Press. DOI: https://doi.org/10.1201/9781003181378. Referência de framework, transformações, texturas, iluminação e shadow mapping.
- Implementação pública de apoio: https://github.com/ax-va/PyOpenGL-Pygame-Stemkoski-Pascale-2021. Foram adaptados componentes de `py3d/` e o exemplo `examples/6-5--shadows.py`. O nome do exemplo no repositório não substitui a referência à seção 6.9 do enunciado.
- Snapshot da branch `main` consultado em 04/11/2026. SHA-256 do ZIP-fonte: `485be3a402fbde37b045421177a1eba822ea6dbf48e7da9e008a4b7fa0a50d20`. Não foi registrada uma revisão Git específica nem encontrada licença declarada na raiz daquele snapshot; não se atribui uma licença inexistente ao material de terceiros.
- Enunciado: *Trabalho - Computacao Grafica.pdf*, fornecido para a atividade.
- Aulas: *Computação Gráfica - Desenhando Formas com preenchimento.pdf* (atributos, interpolação e preenchimento); *2026 - Computação Gráfica - Trabalhando Texturas.pdf* (UV, samplers, filtros e imagens); *Visâo - Computação Gráfica.pdf* (cor, atenção e contraste). As páginas 22–27 do PDF de texturas não continham conteúdo didático.
- Documentação das bibliotecas: https://www.pygame.org/docs/ ; https://pyopengl.sourceforge.net/documentation/ ; https://numpy.org/doc/ .
- `assets/terreno.png`, `asfalto.png`, `solar.png`, `escamas.png`, `grade_uv.png`, `placa.png` e `estacao.png`: imagens originais geradas previamente por scripts Python/Pillow com apoio do ChatGPT. Não foram copiadas figuras dos PDFs nem usadas imagens externas. As placas rasterizam uma fonte do sistema; o arquivo da fonte não é distribuído. As texturas são carregadas de arquivos PNG, não calculadas como textura procedural no shader.

As adaptações do framework incluem compatibilidade com NumPy 2; shaders externos; localização explícita do atributo de posição; inversa transposta para normais; textura de profundidade RGBA32F; PCF e bias; validação de atributos; controle de visibilidade; reutilização de matrizes e uniforms por quadro/material. Modelos, coreografia, colisões, scanner, cenário, agrupamento estático e painel foram elaborados para este projeto com o apoio declarado abaixo.

## Declaração de uso de inteligência artificial

Foi utilizada a ferramenta **OpenAI ChatGPT** para planejar e implementar a cena; escrever/revisar `main.py`, `models.py`, `simulation.py`, `collision.py`, `scanner.py`, `scenery.py`, `sky.py`, `appearance.py` e `geometry_tools.py`; adaptar componentes de `py3d/` e os shaders; gerar texturas por scripts; preparar instalação e documentação; e executar validações automatizadas e gráficas. 

O framework de terceiros possui atribuição própria e não é apresentado como autoria da dupla ou da IA. O uso da ferramenta não substitui a revisão dos integrantes nem sua compreensão do código e das decisões de implementação.
