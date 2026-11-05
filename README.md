# Órbita — Parque Jurássico 1.3

Rover explorador + dinossauro de blocos. Versão com colisões entre os personagens e folga para a cauda, preservando as melhorias baseadas nos três PDFs das aulas; as versões anteriores permanecem separadas. Consulte `APLICACAO_DOS_PDFS.md` para a relação entre páginas, conceitos e código.

Aplicação 3D acadêmica em Python, Pygame e OpenGL, usando componentes de uma implementação pública do framework de Stemkoski e Pascale. Os modelos e a coreografia desta cena foram construídos especificamente para esta atividade, com apoio de IA declarado abaixo.

## Identificação a completar antes da entrega

| Campo | Preenchimento |
|---|---|
| Integrante 1 / matrícula | PREENCHER |
| Tema do integrante 1 | Rover explorador (18) |
| Integrante 2 / matrícula | PREENCHER |
| Tema do integrante 2 | Dinossauro de blocos (28) |
| Disciplina / professor / turma | PREENCHER |

Os temas foram definidos pelo solicitante; o programa não comprova a realização do sorteio previsto no enunciado.

## Cena e interação

Um rover entra em uma pista de testes de um parque de demonstração e reconhece um dinossauro de blocos. Não existe terceiro personagem. O ambiente é um diorama com terreno texturizado, pista, árvores de blocos, cerca, placa texturizada, rochas e marcos de destino.

1. **0–5 s — aproximação:** o rover percorre 3,2 unidades; rodas giram proporcionalmente ao percurso. O dinossauro movimenta a cauda enquanto aguarda.
2. **5–7 s — reconhecimento:** atingida a distância longitudinal de 3,8 unidades, o rover para e gira seu sensor. Um anel de reconhecimento animado identifica o alvo e o dinossauro vira a cabeça em resposta.
3. **7–9 s — resposta:** concluída a varredura, o dinossauro gira 90 graus e movimenta a mandíbula. O rover continua parado.
4. **9–16 s — acompanhamento:** somente depois da virada ambos percorrem 4,55 unidades, em faixas laterais distintas, com aceleração e desaceleração suaves (velocidade média de 0,65 unidade/s; não constante). O rover mantém 3,8 unidades de separação longitudinal; o dinossauro alterna as pernas e oscila a cauda.
5. **Após 16 s — conclusão:** a cena permanece visível. Pressione R para repetir; L habilita repetição automática opcional.

As condições de conclusão de cada estado liberam o próximo. O movimento usa segundos decorridos, não incrementos fixos por quadro. Há detecção cinemática de colisões entre as peças do rover e do dinossauro, com bloqueio preventivo de movimentos. Não há motor de física, IA de personagens ou busca de caminhos. Leia `COLISOES.md` para a implementação e os limites.

## Instalação e execução

Requisitos: Windows com driver gráfico que suporte **OpenGL 3.3**, Python **3.10 a 3.13** de 64 bits (recomendado: 3.12). A instalação inicial das dependências requer acesso à internet. Não é necessário instalar PyOpenGL_accelerate.

**No Windows:** extraia o ZIP inteiro. Dê dois cliques em `PREPARAR_AMBIENTE.bat` e aguarde a mensagem de sucesso; depois abra `INICIAR.bat`. O instalador procura Python utilizável, cria `.venv` dentro desta pasta e instala `requirements.txt`. A aplicação funciona sem internet depois disso.

**Instalação manual**, em um terminal aberto nesta pasta:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Em Linux/macOS: `python3 -m venv .venv`, `.venv/bin/python -m pip install -r requirements.txt`, `.venv/bin/python main.py`. Essas plataformas não foram verificadas nesta entrega.

Se a janela falhar antes de aparecer, confira a versão do Python e atualize o driver da GPU pelo fabricante. Não use o driver genérico do Windows. Execute pelo terminal para ler a mensagem de erro. Rodar com `SDL_VIDEODRIVER=dummy` não permite validar OpenGL.

## Controles

| Tecla | Ação |
|---|---|
| Espaço | Pausar/retomar a animação; a câmera continua disponível |
| Setas | Orbitar a câmera horizontal e verticalmente |
| W / S | Aproximar / afastar |
| A / D | Deslocar o alvo da câmera no eixo X |
| Q / E | Baixar / elevar o alvo |
| Home | Restaurar a câmera |
| R | Reiniciar a sequência e remover a pausa |
| H | Mostrar/ocultar ajuda |
| F12 | Salvar `evidencias/captura.png` |
| Esc | Fechar |
| 1 / 2 / 3 | Câmeras geral, próxima e superior, acompanhando a dupla |
| C | Alternar acompanhamento automático e câmera livre |
| [ / ] | Diminuir / aumentar velocidade: 0,25×, 0,5×, 1× ou 2× |
| L | Alternar repetição automática (desligada por padrão) |
| F2 | Comparar cena com/sem sombra projetada; iluminação permanece ativa |
| Roda do mouse | Aproximar / afastar a câmera |
| F1 | Abrir/fechar laboratório visual; não redefine os modos |
| F3 | Alternar contribuição das cores por vértice |
| F4 | Alternar imagens originais e grade UV nas superfícies texturizadas |
| F5 | Percorrer NEAREST → LINEAR → MIPMAP; padrão MIPMAP |
| F6 | Destacar personagens reduzindo saturação/brilho do ambiente |
| F7 | Comparar materiais da cena em cinza; HUD e fundo permanecem independentes |
| F8 | Alternar preenchimento e malha de triângulos |

## Onde está cada requisito

| Recurso | Arquivos / classes / funções |
|---|---|
| Rover com rodas e sensor | `models.py`: `Models.rover` |
| Dinossauro de blocos articulado | `models.py`: `Models.dinosaur` |
| Ambiente e textura PNG com UV repetidas | `main.py`: `Application.environment`; `assets/terreno.png`; `repeatUV` no shader |
| Estados e animação por tempo | `simulation.py`: `Simulation.update`, `Simulation.pose` |
| Hierarquia, translação, rotação e escala | `models.py`: `transform`, `Models.pivot`; `py3d/core_ext/object3d.py` |
| Câmera perspectiva e controle de teclado | `main.py`: `Application.controls`; `py3d/core_ext/camera.py` |
| Pausa e retomada | `main.py`: `Application.run`; `simulation.py`: `Simulation.paused` |
| Luz direcional e ambiente | `main.py`: `Application.__init__`; `py3d/light/` |
| Phong, normais e textura | `py3d/material/phong.py`; `shaders/phong.vert`, `shaders/phong.frag` |
| Shadow mapping em duas passagens | `py3d/core_ext/renderer.py`: `Renderer.render`; `py3d/light/shadow.py`; `shaders/depth.vert`, `shaders/depth.frag` |
| Textura de profundidade e framebuffer | `py3d/core_ext/render_target.py`: `RenderTarget` |
| Painel de estado e linha do tempo em textura 2D | `main.py`: `HUD`; `py3d/material/texture.py` |
| Colisões e folga para a cauda | `collision.py`; `simulation.py`: `Simulation.update`; `main.py`: `Application.can_advance`; `COLISOES.md` |
| Cores por vértice e gradientes | `geometry_tools.py`; `shaders/phong.vert`, `shaders/phong.frag` |
| Laboratório de UV, filtros e contraste | `appearance.py`; `main.py`: `Application.handle_event`, `HUD.draw` |
| Envio de atributos e uniforms | `py3d/core/attribute.py`, `py3d/core/uniform.py` |

Os shaders externos são carregados em tempo de execução. O compilador do framework acrescenta `#version 330`. Os shaders do painel são entregues em `shaders/hud.vert` e `shaders/hud.frag` e carregados por `TextureMaterial`.

Leia `EXPLICACAO_TECNICA.md` para atributos/uniforms, diferenças entre iluminação e sombra projetada, adaptações do framework e relações com os seis capítulos. `ROTEIRO_APRESENTACAO.md` organiza a demonstração de dez minutos.

## Verificação

Execute nesta pasta, após a instalação:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests/check_gpu.py
.\.venv\Scripts\python.exe main.py --validate
```

O primeiro comando verifica a lógica sem abrir janela. O segundo abre OpenGL para verificar mapa de sombras dinâmico, influência visível das sombras e câmera durante a pausa. O terceiro executa 1.000 quadros com passo de simulação de 1/60 s, salva cinco imagens e `evidencias/validacao_gpu.json`, e fecha. O passo fixo existe somente nesse modo de validação; a execução normal usa o relógio real.

Para validar as melhorias baseadas nos PDFs, execute também `.\.venv\Scripts\python.exe tests/check_lessons.py`. O teste verifica interpolação RGB na GPU, origem/repetição/deslocamento UV, diferenças entre filtros, foco, cinza, malha e preservação da animação e do filtro de sombras.

Resultados medidos e limites estão em `VALIDACAO.md`. Os arquivos JSON e imagens acompanham a entrega. As evidências registram esta máquina, não garantem compatibilidade com todos os computadores. A versão 1.1 acrescenta filtragem PCF 3×3 às sombras e bias dependente da inclinação, preservando o shadow mapping em duas passagens. Não solicita automaticamente pontuação de bônus; esse enquadramento depende do professor. Terreno, pista, painel solar, escamas e placa são imagens PNG carregadas de arquivo.

## Contribuições individuais

**Preencher com o que cada integrante realmente revisou e realizou.** A divisão abaixo é uma sugestão para organizar o estudo, não uma declaração de trabalho já executado por vocês.

- Integrante 1: revisar rover, rodas, sensor, câmera e controle por tempo; registrar as alterações efetivamente feitas.
- Integrante 2: revisar dinossauro, hierarquia, ambiente, textura e iluminação; registrar as alterações efetivamente feitas.
- Ambos: revisar a interação integrada, shadow mapping, shaders, testes e documentação. Cada integrante deve explicar também a aplicação completa.

## Fontes e atribuição

- Enunciado fornecido: `Trabalho - Computacao Grafica.pdf`, especialmente temas 18 e 28 e requisitos de desenvolvimento.
- STEMKOSKI, Lee; PASCALE, Michael. *Developing Graphics Frameworks with Python and OpenGL*. CRC Press. DOI: https://doi.org/10.1201/9781003181378. Referência principal, em especial shadow mapping, seção 6.9 indicada no enunciado.
- Implementação pública de apoio: https://github.com/ax-va/PyOpenGL-Pygame-Stemkoski-Pascale-2021 — componentes em `py3d/`, baseada no livro. Foram consultados `examples/6-5--shadows.py`, classes de cena, geometria, materiais, renderização e sombras. O nome desse exemplo no repositório não altera a referência à seção 6.9 do enunciado. Consulte `FONTES_FRAMEWORK.md` para snapshot e adaptações.
- Pygame: https://www.pygame.org/docs/ ; PyOpenGL: https://pyopengl.sourceforge.net/documentation/ ; NumPy: https://numpy.org/doc/ .
- Materiais das aulas: `Computação Gráfica - Desenhando Formas com preenchimento.pdf` (27 páginas), `2026 - Computação Gráfica - Trabalhando Texturas.pdf` (28 páginas) e `Visâo - Computação Gráfica.pdf` (20 páginas). Consulte `APLICACAO_DOS_PDFS.md` e `FONTES_PDFS.json` para conteúdo efetivamente utilizado e identificação das fontes.
- `assets/*.png`: imagens originais, sem copiar figuras dos PDFs. Geração de terreno/asfalto/solar/escamas/grade em `tools/gerar_materiais.py`; placa em `tools/gerar_placa.py`. A placa rasteriza uma fonte do sistema sem distribuir o arquivo da fonte.

## Declaração de uso de inteligência artificial

Foi utilizada a ferramenta **OpenAI Codex** para planejar a cena; escrever `collision.py`, `main.py`, `models.py`, `simulation.py`, `appearance.py`, `geometry_tools.py`, scripts de instalação, testes e documentação; gerar as texturas PNG por scripts; adaptar componentes e shaders de `py3d/`; executar validações e analisar capturas. O framework de terceiros foi atribuído separadamente e não é declarado como autoria da dupla ou da IA. Os integrantes devem revisar o código, testar na máquina da apresentação, registrar suas contribuições reais e compreender os trechos antes da entrega. Não afirmar que os testes automáticos substituem sua revisão individual.

## Base preservada da versão 1.1

- Rover com detalhes de pneus, cubos, antena, duas lentes e acabamento do chassi.
- Dinossauro com cabeça e mandíbula articuladas, dentes, garras e encaixes de blocos.
- Arrancada, chegada e virada com smoothstep; caminhada suavizada nas extremidades; leve movimento vertical do corpo.
- Anel de reconhecimento giratório, ativo somente nos estados de inspeção/resposta e sem projetar sombra.
- Parque com vegetação geométrica, cerca, placa com textura de imagem e plataforma.
- Linha do tempo, relógio da missão, indicação de pausa, velocidade e câmera.
- Câmeras predefinidas, acompanhamento, velocidade ajustável, repetição opcional e comparação de sombras.
- F12 captura o quadro atual depois da renderização; criação automática da pasta de evidências.
- Dez testes da simulação e teste gráfico dos novos comandos da interface.
- Renderização otimizada: reutilização das matrizes globais e redução do envio repetido de uniforms. O benchmark da mesma cena passou de 10,3 para 34,1 FPS nesta máquina; é uma medição específica, sem garantia em outros computadores.

As novas partes dos modelos e o acabamento também foram elaborados com apoio do Codex. O README continua exigindo o preenchimento dos dados e das contribuições reais da dupla.

## Melhorias da versão 1.2 e relação com as aulas

- Atributo `vertexColor` efetivamente usado e interpolado; gradientes nos personagens e terreno, com comparação F3.
- Materiais PNG para pista, painel solar e escamas; nova textura de terreno menos carregada visualmente.
- UV escaladas/deslocadas por uniforms, grade UV identificada e comparação de três filtros de amostragem.
- Paleta que diferencia rover alaranjado e dinossauro verde-azulado; modo de foco e comparação em cinza inspirados nos tópicos de atenção/contraste.
- Inspeção da triangulação por F8 e validação dos tamanhos dos atributos antes da criação do VAO.
- Rodapé com fundo opaco para preservar a leitura sobre imagens detalhadas, inclusive no diagnóstico UV.
- Treze testes unitários, testes reais de GPU dos conceitos e documentação com correspondência às páginas dos PDFs.
- Benchmark curto da versão 1.2: 34,5 FPS na máquina registrada, sem HUD/limitador. O histórico de 10,3 → 34,1 FPS acima se refere à otimização da versão 1.1; não é uma nova medição antes/depois da versão 1.2.

As novas comparações são opcionais e vêm desativadas; o laboratório é aberto por F1. Cores por vértice e filtro trilinear com mipmaps fazem parte do visual padrão. Reiniciar com R não redefine preferências visuais. Nenhuma melhoria retira a interação, a câmera, a pausa ou o shadow mapping obrigatório.

## Correção da versão 1.3 — colisões

- O rover para mais longe (3,8 unidades) e deixa a cauda completar a virada sem atravessar o veículo.
- Colisores compostos por peça acompanham a hierarquia real; a proteção inclui cauda e sensor.
- Subpassos de no máximo 1/120 s verificam o percurso antes de aceitar o movimento, inclusive em FPS baixo ou velocidade 2×.
- Uma colisão rejeita o subpasso e restaura tempo, posições, articulações e rodas. A interface mostra BLOQUEADO; R reinicia, e a câmera continua disponível.
- 19 testes unitários e um teste integrado com 3.841 poses, reprodução do defeito antigo e bloqueio de uma colisão forçada.
- `tests/check_performance.py` agora inclui o guardião de colisões; benchmark curto nesta máquina: 28,6 FPS sem HUD/limitador. As medições de versões anteriores acima são históricas e não representam o custo desta versão.

Use o novo ZIP em uma pasta separada e prepare o ambiente dessa pasta. O detector protege o rover e o dinossauro; não acrescenta física à câmera ou aos objetos estáticos. Consulte `COLISOES.md` e `evidencias/validacao_colisoes.json`.
