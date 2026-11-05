# Órbita — Parque Jurássico 1.1

Rover explorador + dinossauro de blocos. Versão aprimorada; a entrega anterior permanece separada.

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

1. **0–5 s — aproximação:** o rover percorre cinco unidades; rodas giram proporcionalmente ao percurso. O dinossauro movimenta a cauda enquanto aguarda.
2. **5–7 s — reconhecimento:** atingida a distância longitudinal de duas unidades, o rover para e gira seu sensor. Um anel de reconhecimento animado identifica o alvo e o dinossauro vira a cabeça em resposta.
3. **7–9 s — resposta:** concluída a varredura, o dinossauro gira 90 graus e movimenta a mandíbula. O rover continua parado.
4. **9–16 s — acompanhamento:** somente depois da virada ambos percorrem 4,55 unidades, em faixas laterais distintas, com aceleração e desaceleração suaves (velocidade média de 0,65 unidade/s; não constante). O rover mantém duas unidades de separação longitudinal; o dinossauro alterna as pernas e oscila a cauda.
5. **Após 16 s — conclusão:** a cena permanece visível. Pressione R para repetir; L habilita repetição automática opcional.

As condições de conclusão de cada estado liberam o próximo. O movimento usa segundos decorridos, não incrementos fixos por quadro. Não há física, colisões, IA de personagens nem busca de caminhos; não são exigidas pelo trabalho.

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

## Onde está cada requisito

| Recurso | Arquivos / classes / funções |
|---|---|
| Rover com rodas e sensor | `models.py`: `Models.rover` |
| Dinossauro de blocos articulado | `models.py`: `Models.dinosaur` |
| Ambiente e textura PNG com UV repetidas | `main.py`: `Application.environment`; `assets/terreno.png` |
| Estados e animação por tempo | `simulation.py`: `Simulation.update`, `Simulation.pose` |
| Hierarquia, translação, rotação e escala | `models.py`: `transform`, `Models.pivot`; `py3d/core_ext/object3d.py` |
| Câmera perspectiva e controle de teclado | `main.py`: `Application.controls`; `py3d/core_ext/camera.py` |
| Pausa e retomada | `main.py`: `Application.run`; `simulation.py`: `Simulation.paused` |
| Luz direcional e ambiente | `main.py`: `Application.__init__`; `py3d/light/` |
| Phong, normais e textura | `py3d/material/phong.py`; `shaders/phong.vert`, `shaders/phong.frag` |
| Shadow mapping em duas passagens | `py3d/core_ext/renderer.py`: `Renderer.render`; `py3d/light/shadow.py`; `shaders/depth.vert`, `shaders/depth.frag` |
| Textura de profundidade e framebuffer | `py3d/core_ext/render_target.py`: `RenderTarget` |
| Painel de estado e linha do tempo em textura 2D | `main.py`: `HUD`; `py3d/material/texture.py` |
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

Resultados medidos e limites estão em `VALIDACAO.md`. Os arquivos JSON e imagens acompanham a entrega. As evidências registram esta máquina, não garantem compatibilidade com todos os computadores. A versão 1.1 acrescenta filtragem PCF 3×3 às sombras e bias dependente da inclinação, preservando o shadow mapping em duas passagens. Não solicita automaticamente pontuação de bônus; esse enquadramento depende do professor. Terreno e placa são imagens PNG carregadas de arquivo.

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
- `assets/terreno.png` e `assets/placa.png`: imagens originais produzidas por Python/Pillow, sem imagens externas. Fontes da geração: `tools/gerar_textura.py` e `tools/gerar_placa.py`. A placa rasteriza uma fonte disponível no sistema, sem distribuir o arquivo de fonte.

## Declaração de uso de inteligência artificial

Foi utilizada a ferramenta **OpenAI Codex** para planejar a cena; escrever `main.py`, `models.py`, `simulation.py`, scripts de instalação, testes e documentação; gerar as texturas PNG por scripts; adaptar componentes e shaders de `py3d/`; executar validações e analisar capturas. O framework de terceiros foi atribuído separadamente e não é declarado como autoria da dupla ou da IA. Os integrantes devem revisar o código, testar na máquina da apresentação, registrar suas contribuições reais e compreender os trechos antes da entrega. Não afirmar que os testes automáticos substituem sua revisão individual.

## Melhorias da versão 1.1

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
