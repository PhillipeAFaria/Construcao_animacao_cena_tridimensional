# Como os três PDFs foram usados na versão 1.2

Esta versão usa os PDFs como fontes de estudo para aprimorar o projeto existente, mantendo a atividade original: Python/Pygame/OpenGL, framework do livro, dois temas modelados pela dupla, movimento por tempo, interação coordenada, câmera, pausa, textura, iluminação e shadow mapping. Os exemplos e exercícios internos das aulas não foram tratados como novos pedidos de entrega nem substituem esses requisitos.

## Fontes analisadas

1. **Computação Gráfica - Desenhando Formas com preenchimento.pdf** — 27 páginas. Texto completo extraído e figuras/código das páginas relevantes conferidos visualmente. Os conteúdos utilizados são atributos de vértice, passagem de dados entre shaders e interpolação na rasterização.
2. **2026 - Computação Gráfica - Trabalhando Texturas.pdf** — 28 páginas. A maior parte do conteúdo está em imagens; as páginas foram renderizadas e inspecionadas visualmente. Foram utilizados os slides sobre geometria, material, texels, upload, filtros, UV e samplers. As páginas **22–27** contêm apenas o modelo visual vazio; não foram inventadas explicações ou exercícios para elas.
3. **Visâo - Computação Gráfica.pdf** — 20 páginas, título interno “Visão Humana”. Texto extraído e figuras pertinentes inspecionadas. Foram aproveitados os conceitos de cor do objeto/cor percebida, interpretação, atenção e contraste de vizinhança. Não foram implementadas afirmações anatômicas ou uma simulação do sistema visual humano.

Os números abaixo são as páginas físicas do PDF, contando a capa como página 1. Nenhuma figura dos slides foi copiada para as texturas da aplicação. Os hashes das fontes consultadas estão em `FONTES_PDFS.json`; os PDFs não são redistribuídos no ZIP.

## Do conteúdo à implementação

| Fonte e páginas | Conceito | Aplicação concreta | Onde conferir |
|---|---|---|---|
| Formas, 2–5 e 14–17 | Atributos de posição/cor em buffers e comunicação `in/out` | `vertexColor` é associado ao VAO, passado como `interpolatedColor` e consumido no fragment shader | `shaders/phong.vert`, `shaders/phong.frag`, `core/attribute.py` |
| Formas, 4 e 14–17 | Streams devem descrever a mesma quantidade de vértices | Validação antes de criar o VAO rejeita atributos com comprimentos incompatíveis | `py3d/geometry/geometry.py`: `validate_attributes`; `Mesh.__init__` |
| Formas, 21–27 | Rasterização e cores interpoladas em superfícies preenchidas | Gradientes no terreno e nas peças dos personagens; F3 alterna esse canal | `geometry_tools.py`, `models.py`, `main.py`: `environment` |
| Formas, 24–27 | Primitivas preenchidas e linhas | F8 compara a malha triangulada com o preenchimento, mantendo as mesmas posições | `appearance.py`; propriedade `wireframe` dos materiais |
| Texturas, 3–9 | Geometria define forma; material e textura definem aparência | Pista, painel solar e dinossauro recebem texturas PNG sem depender de malhas externas | `models.py`, `main.py`; `assets/` |
| Texturas, 10–13 | Carregamento local e upload RGBA | Imagens acompanham o projeto, localizadas a partir de `__file__`; `Texture` faz upload e gera mipmaps | `py3d/core_ext/texture.py`; `assets/ORIGEM.txt` |
| Texturas, 14 | NEAREST, LINEAR, mipmaps e REPEAT | F5 compara os três filtros nas texturas de cor; o padrão é trilinear com mipmaps | `appearance.py`: `refresh` |
| Texturas, 15–19 | Coordenadas UV e interpolação | `UV = vertexUV * repeatUV + offsetUV`; repetição do terreno e da pista | `shaders/phong.vert`; uniforms dos materiais |
| Texturas, 16–17 | Origem inferior esquerda e referência na imagem | Grade UV com células A1–D4, U horizontal e V vertical; F4 permite verificar o mapeamento | `assets/grade_uv.png`; `tools/gerar_materiais.py` |
| Texturas, 20–21 | Sampler recebe unidade de textura, não o identificador da imagem | Textura de cor usa unidade 1, mapa de sombras usa unidade 3; troca de imagem preserva a geometria | `py3d/core/uniform.py`, `appearance.py` |
| Visão, 2, 4 e 11 | Aparência observada envolve objeto, luz e interpretação | Rover quente/alaranjado, dinossauro frio/verde-azulado e fundo menos saturado ajudam a separar os elementos | Paletas em `models.py`; materiais da cena |
| Visão, 16 e 19 | Atenção e contraste dependem do contexto | F6 reduz saturação/brilho do ambiente, preservando personagens; o rodapé tem fundo opaco para manter legibilidade até no modo UV | `appearance.py`; `shaders/phong.frag`; `HUD.draw` |
| Visão, 19 | A percepção de intensidade depende da vizinhança | F7 oferece comparação ilustrativa em cinza, para avaliar separação sem depender somente da cor | `grayScale` no fragment shader |

## Limites e distinções importantes

- A aula mostra `GL_TRIANGLE_FAN` para um polígono simples. A cena utiliza `GL_TRIANGLES` para malhas já trianguladas. Ambos permitem preenchimento e interpolação; não foi feita uma substituição indevida de toda malha 3D por um único fan.
- F8 usa `glPolygonMode(GL_LINE)` para inspecionar as arestas dos triângulos. Isso não equivale a desenhar apenas um contorno externo com `GL_LINE_LOOP`. A passagem de sombras continua usando triângulos preenchidos.
- O projeto usa VBOs separados para os atributos, como a classe `Attribute` do framework. Não mistura esse layout com o exemplo de um buffer intercalado sem atualizar strides e offsets.
- `baseColor` uniforme, cor por vértice e imagem são fatores separados que podem ser multiplicados. Cor-base uniforme não significa ausência de iluminação ou sombra.
- Repetição de UV e filtragem são mecanismos diferentes. As UV podem exceder [0,1] quando `GL_REPEAT` está ativo. O filtro escolhe como amostrar os texels, não altera o número de vértices.
- A inversão vertical de `pygame.image.tostring(..., True)` alinha a origem da imagem carregada ao sistema UV usado. O teste de GPU confere os quatro quadrantes com uma imagem 2×2.
- As texturas de escamas, asfalto e painel solar modificam a cor. Não adicionam relevo, volume nem deslocamento de vértices; não são bump mapping.
- O modo de foco é uma decisão de apresentação inspirada nos tópicos de atenção/contraste. Não comprova ganho perceptivo em um estudo com usuários.
- A conversão ilustrativa em cinza usa uma combinação ponderada dos canais RGB. Não é uma medição fotométrica nem uma simulação clínica de daltonismo. Ela afeta os materiais da cena; o painel e a cor de fundo da janela permanecem independentes.
- As imagens são geradas previamente por Pillow e carregadas de arquivos PNG. Isso não é textura procedural calculada no shader e não é apresentado automaticamente como bônus.

## Demonstração sugerida em aproximadamente um minuto

1. Execute a cena normalmente; durante o reconhecimento, pause com Espaço.
2. Abra o laboratório com F1 e use F3 para mostrar a contribuição de cores por vértice.
3. Use F4 para mostrar as UV na mesma geometria; F5 compara filtros. Use W/S se precisar aproximar a câmera para observar os texels.
4. Volte às imagens com F4. Use F6 para destacar os personagens e F7 para observar os materiais em cinza. Desative ambos para voltar ao visual normal.
5. F8 mostra a triangulação. Volte ao preenchimento, feche o laboratório com F1 e retome com Espaço.

F1 só mostra ou oculta o painel: os modos selecionados continuam ativos até serem alternados novamente. R reinicia a coreografia e remove a pausa; não apaga as preferências de visualização.

## Evidência de funcionamento

`tests/check_lessons.py` executa os mesmos comandos usados pela interface e compara imagens renderizadas. Em um experimento ortográfico controlado, valores de cor esperados de 25%, 50% e 75% produziram os pixels RGB `[64,64,51]`, `[128,128,51]` e `[191,191,51]`. Isso verifica a interpolação real na GPU, não apenas a presença de um nome de variável no código.

O mesmo teste verifica origem UV, `repeatUV`, `offsetUV`, diferenças entre filtros, comparação de foco/cinza, preservação da pose e preservação do filtro do mapa de sombras. Os resultados e capturas estão em `evidencias/validacao_aulas.json` e nos PNGs correspondentes. Consulte `VALIDACAO.md` para ambiente e limites.
