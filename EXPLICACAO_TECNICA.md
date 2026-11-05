# Explicação técnica

## Organização e relação com o livro

A cena usa uma implementação pública baseada no framework do livro, com adaptações identificadas em `FONTES_FRAMEWORK.md`. Não é uma reconstrução integral nem um motor de jogos externo. A progressão dos conteúdos é: fundamentos de representação 3D; programação gráfica/OpenGL; transformações e matrizes; estrutura do framework e geometria; texturas e renderização em textura; iluminação e sombras. Para a apresentação, conferir os títulos exatos dos capítulos na edição usada pela turma.

| Núcleo de conteúdo | Aplicação nesta cena |
|---|---|
| Fundamentos | Vértices, triângulos, espaço local, espaço de mundo, câmera e projeção |
| Python/OpenGL | Janela Pygame, contexto 3.3, compilação GLSL, buffers e desenho de triângulos |
| Transformações | Matrizes de translação, rotação, escala, perspectiva e inversa da câmera |
| Framework e modelos | Object3D, Scene, Mesh, Camera, Geometry, Material, Renderer e grafo de cena |
| Texturas | Imagem PNG, UV, repetição, mipmaps e painel em textura |
| Iluminação e efeitos | Phong, luz direcional, luz ambiente e shadow mapping em duas passagens |

## Transformações e hierarquias

`transform` calcula `T @ Ry @ Rx @ Rz @ S`. Com vetores coluna, a escala atua primeiro, depois as rotações e por último a translação. Uma parte do personagem herda a matriz global de seu pai: `M_global = M_pai @ M_local`. O rover é pai dos pivôs das rodas e do sensor; o dinossauro é pai dos pivôs das pernas e da cauda. Cada peça tem dimensões por escala não uniforme de uma geometria reutilizada. Os pivôs são nós sem geometria e tornam a rotação uma articulação, em vez de uma órbita ao redor da origem global.

A frente do rover é +X; a do dinossauro no modelo local é +Z. A virada de 90 graus em Y passa a frente do dinossauro para +X. As posições laterais são diferentes, por isso a separação de duas unidades é longitudinal e não a distância euclidiana total.

## Tempo e coordenação

Na execução normal `Clock.tick(60)/1000` mede o intervalo real entre quadros. O limite de 60 FPS regula o consumo; não define a velocidade. A aproximação segue `x = -7 + 5*smoothstep(t/5)`. O acompanhamento segue `x_dino = 4.55*smoothstep(t_estado/7)` e `x_rover = x_dino - 2`. A função smoothstep é `u²(3-2u)`, com u limitado a [0,1]; sua derivada é nula nas extremidades. Assim os deslocamentos continuam independentes de FPS, com arranque e chegada suaves.

`Simulation.update` consome o dt até a fronteira de um estado e reaproveita o excedente no seguinte. Isso evita que a troca de estados acumule atrasos diferentes conforme o FPS. O rover só libera a resposta após concluir o reconhecimento; só acompanha depois que termina a virada do dinossauro. A relação é programada por estados, sem detecção de colisões.

Rodas: `ângulo = -distância / raio`, com raio 0,38. Pernas: seno em oposição de fase durante o acompanhamento. Cauda: seno do tempo acumulado da simulação. Sensor: varredura senoidal ao quadrado durante o reconhecimento. A cabeça reage ao sensor; a mandíbula abre e fecha durante a resposta. O corpo apresenta leve oscilação vertical na caminhada, e a amplitude das pernas é atenuada no início e no fim para evitar saltos de pose. Na pausa, o tempo da simulação não avança; o relógio usado na câmera continua ativo.

## Atributos de vértice efetivamente utilizados

| Atributo | Tipo | Uso |
|---|---|---|
| vertexPosition | vec3 | Posição local; passa pelas matrizes M, V e P. Location 0 fixada em Phong e depth para reutilizar corretamente o VAO na passagem de sombras. |
| vertexNormal | vec3 | Normal local por face ou superfície; usada na iluminação Phong. |
| vertexUV | vec2 | Coordenada de textura; usada no chão e no painel. |

As geometrias também fornecem `vertexColor` e `faceNormal`, mas os shaders usados nesta cena não os consomem; a associação ignora atributos sem localização ativa. A cor das peças vem do uniform `baseColor`.

## Uniforms e shaders

`Attribute` envia arrays para VBOs; `Mesh` cria VAO e associa atributos ao programa; `Uniform` envia os valores por objeto ou material antes do desenho. Um uniform não precisa variar por vértice.

| Uniform | Função |
|---|---|
| modelMatrix | Leva o modelo local ao mundo, incluindo a hierarquia |
| viewMatrix | Inversa da matriz global da câmera; mundo para câmera |
| projectionMatrix | Perspectiva na câmera principal; ortográfica na câmera da luz e no painel |
| baseColor | Cor de cada material |
| useTexture / textureSampler | Ativa e amostra PNG ou textura do painel; unidade 1 |
| viewPosition | Posição da câmera para o brilho especular |
| specularStrength / shininess | Intensidade e concentração do brilho |
| light0 / light1 | Estruturas com tipo e cor; luz ambiente e direcional. Direção é usada na luz direcional; posição/atenuação estão no suporte a luz pontual, não ativado nesta cena. |
| useShadow | Habilita comparação com o mapa de profundidade |
| shadow0.viewMatrix / projectionMatrix | Transformam cada fragmento para o espaço da câmera da luz |
| shadow0.depthTextureSampler | Mapa produzido na primeira passagem; unidade 3 |
| shadow0.lightDirection / strength / bias | Direção da luz, intensidade da sombra e tolerância contra auto-sombreamento |
| repeatUV / offsetUV | Escala e deslocamento das UV do painel; valores padrão 1 e 0 |

O Phong herdado também envia `useBumpTexture=False`. Bump mapping não é usado; seus ramos ficam desativados. Os uniforms de luz pontual e bump sem uso podem ser eliminados pelo compilador GLSL. Não alegar esses recursos como implementados.

No vertex shader Phong: `gl_Position = P * V * M * vec4(posição,1)`. A normal usa `transpose(inverse(mat3(M)))`, necessário para preservar sua perpendicularidade sob escala não uniforme. No fragment shader, a normal interpolada é normalizada novamente. O termo difuso usa o produto escalar entre a normal e a direção para a luz; o especular usa reflexão e direção para a câmera. A luz ambiente evita faces totalmente pretas.

O painel usa seus próprios shaders de textura, sem iluminação; é desenhado por último com teste de profundidade desativado e transparência. Não participa da renderização de sombras.

## Sombreamento de superfície versus sombra projetada

**Sombreamento de superfície** é a variação de cor e brilho produzida pela orientação das normais, pelas luzes e pelo material. Pode existir em uma esfera isolada sem qualquer objeto bloqueando a luz.

**Sombra projetada** ocorre quando uma superfície fica atrás de outra na direção da luz. Normais e Phong sozinhos não identificam esse bloqueio. Neste projeto ele é calculado por shadow mapping:

1. A câmera ortográfica da luz vê a cena. `DepthMaterial` transforma os vértices para essa câmera e grava `gl_FragCoord.z` nos canais RGB de uma textura RGBA32F. O framebuffer tem também um renderbuffer de profundidade que resolve a visibilidade dessa primeira passagem. Esse armazenamento de profundidade como cor segue a abordagem do framework consultado; não é uma sombra plana simulada.
2. A câmera principal desenha a cena com Phong. Cada ponto é também transformado para a câmera da luz. As coordenadas passam de [-1,1] para [0,1] e amostram a profundidade mais próxima. Se a profundidade atual excede a armazenada mais o bias, há um bloqueador à frente. A região recebe o fator `1 - strength * cobertura`, em que cobertura é a média de nove comparações de profundidade em uma vizinhança 3×3 (PCF). A suavização ocorre na comparação, não por uma média simples dos valores de profundidade.

A textura tem 2048×2048, amostragem nearest por consulta (nove consultas PCF por fragmento), bias-base 0,0018 e região ortográfica de X [-14,14], Y [-12,12], profundidade [0,1;40]. O shader verifica os limites do mapa. A divisão por W não é necessária aqui porque a câmera de sombras é ortográfica, com W=1. Para luz projetiva/perspectiva seria necessária.

A passagem de sombras é recalculada a cada quadro com as matrizes atuais, inclusive rodas, pernas e cauda. Na pausa, recalculá-la mantém a imagem estável. O teste de GPU verifica que o mapa muda entre duas poses e que desativar a comparação altera pixels da imagem.

Limites: PCF 3×3 reduz bordas serrilhadas, mas não simula uma penumbra física. O bias efetivo é `max(bias_base*(1-cosseno), bias_base*0.35)` e reduz auto-sombreamento em ângulos rasantes; ainda pode haver pequenos artefatos dependendo da câmera e da resolução. As câmeras e o volume de sombras foram dimensionados para a pista desta cena, não para um mundo ilimitado. As rochas e os marcos também podem projetar sombras.

## Decisões de escopo

Modelos feitos por caixas e cilindros, sem OBJ, Blender ou malhas externas. Textura de imagem original, sem dependência de download durante execução. Pista plana simplifica o contato visual das rodas e dos pés. Dinossauro de brinquedo com caminhada estilizada, sem cinemática inversa. Não há áudio porque não é requisito. O PNG gerado por script não é apresentado como efeito procedural de shader nem como bônus.

## Novos recursos da versão 1.1

`Application.handle_event` concentra comandos discretos de teclado e mouse, permitindo testar os mesmos caminhos usados pela interface. `controls` continua processando teclas mantidas pressionadas. `1`, `2` e `3` selecionam vistas predefinidas; `C` acompanha o ponto médio entre os personagens. Ao usar as teclas de câmera livre, o acompanhamento é desligado para que o controle não dispute o alvo com o usuário. A roda do mouse ajusta a distância, respeitando os limites de 5 a 32 unidades.

O fator de velocidade multiplica somente o dt da simulação, preservando a velocidade da câmera e o processamento de eventos. A linha do tempo mostra tempo de simulação, não o tempo real do computador. `R` reinicia a missão e remove a pausa, preservando as preferências de velocidade e câmera. `L` é opcional e reinicia a sequência após a conclusão; essa repetição faz uma reposição instantânea explícita das posições, sem simular um trajeto de retorno.

O anel de reconhecimento é composto por 24 caixas finas, com translação e rotação controladas pelo tempo da simulação. É um indicador visual, não uma luz real nem bloom. Seu `cast_shadow=False` é respeitado somente na passagem de sombras; a geometria continua sendo renderizada e iluminada normalmente. F2 alterna o uniform `useShadow` dos materiais para demonstrar a diferença entre Phong e sombra projetada; não desliga a luz direcional.

`HUD.draw` usa cache do texto e atualiza a textura quando muda o estado, uma preferência ou o décimo de segundo exibido. A geometria da linha do tempo é desenhada na superfície Pygame do painel. A captura F12 é adiada até o fim da renderização do quadro atual para evitar salvar o buffer de um quadro anterior.

O renderizador calcula as matrizes globais de todos os nós uma vez por quadro e as reutiliza nas duas passagens. Os uniforms que não variam por objeto são enviados uma vez por material a cada chamada de renderização; a matriz de modelo continua sendo enviada para cada malha. Uniforms pertencem ao programa e sobrevivem à troca de programa, mas bindings de textura são globais; por isso os samplers são religados quando um material texturizado é reutilizado. O cache não atravessa quadros, permitindo mudar materiais, câmeras e luzes sem invalidadores adicionais. A ordem de desenho original é mantida.
