# Demonstração de dez minutos

Antes da aula: preencher nomes e contribuições no README; instalar as dependências; executar a aplicação na máquina que será usada; confirmar OpenGL, legibilidade, pausa e sombra. Ambos devem ler o código integrado. O roteiro é uma proposta de distribuição, não prova de participação.

| Tempo | Responsável sugerido | Conteúdo |
|---|---|---|
| 0:00–1:00 | Ambos | Identificar dupla e temas. Explicar parque de demonstração e objetivo do reconhecimento. |
| 1:00–2:00 | Integrante 1 | Mostrar o ciclo completo. Apontar rover aguardando o sensor e a virada do dinossauro, agora com folga para a cauda. Explicar que os movimentos são verificados por colisores compostos. |
| 2:00–3:00 | Integrante 1 | Pausar com Espaço, mover a câmera com setas e W/S, alternar vistas com 1/2/3 e retomar. Use [ para desacelerar se necessário. Explicar tempo decorrido. |
| 3:00–4:00 | Integrante 2 | Mostrar composição dos modelos e pivôs de cauda, pernas, rodas e sensor em models.py. |
| 4:00–5:00 | Integrante 1 | Abrir simulation.py: estados, transições e reaproveitamento do dt. |
| 5:00–6:00 | Integrante 2 | Abrir F1; comparar F3 (cor interpolada), F4 (UV) e F5 (filtros). Voltar às imagens; comparar F6/F7 (foco/cinza), restaurar e explicar luz direcional/normais. Usar o roteiro curto de APLICACAO_DOS_PDFS.md. |
| 6:00–7:30 | Ambos | Explicar duas passagens do shadow mapping, câmera da luz, comparação de profundidade e filtragem PCF 3×3. Usar F2 para comparar com/sem sombra, mantendo Phong. |
| 7:30–8:30 | Ambos | Mostrar shader Phong e uniforms M/V/P; distinguir iluminação e sombra projetada. |
| 8:30–10:00 | Ambos | Apresentar contribuições reais, fontes e uso de IA; responder perguntas individuais. |

## Perguntas de preparação

1. **O que prova que há interação?** O rover para ao chegar; o sensor termina antes de liberar a virada; a virada termina antes de liberar o acompanhamento. Há dependência entre as ações.
2. **O dinossauro está animado antes de andar?** Sim, a cauda oscila durante a espera. O deslocamento e as pernas entram depois da resposta.
3. **Por que a velocidade não muda com FPS?** As posições são calculadas em função de segundos; o dt excedente é preservado nas transições.
4. **Por que usar pivôs?** A peça gira em torno da articulação e herda o movimento do personagem.
5. **Qual a ordem das matrizes?** P × V × M × posição local; na composição local, a operação à direita atua primeiro.
6. **Por que usar inversa transposta na normal?** Escala não uniforme deforma direções; essa matriz mantém a normal perpendicular à superfície transformada.
7. **A luz direcional tem posição?** A iluminação usa direção uniforme; a posição neste projeto posiciona a câmera da luz para gerar o mapa de sombras.
8. **O que há na textura de sombras?** Profundidade visível pela luz, gravada como cor float pelo shader depth, com teste de profundidade em renderbuffer.
9. **Qual a diferença entre sombra e sombreado?** Phong modela a resposta local à luz; shadow mapping verifica bloqueio da luz por geometria.
10. **Para que serve o bias?** Evita que erros numéricos façam uma superfície sombrear a si própria; um valor excessivo separa visualmente sombra e objeto.
11. **O que acontece ao pausar?** O tempo da simulação para, mas os eventos, câmera e renderização continuam funcionando.
12. **Há efeitos extras?** Há filtragem PCF 3×3 das sombras e melhorias visuais. A classificação como bônus depende do professor; não há bloom nem bump mapping. O terreno e a placa usam PNG, não textura procedural no shader.
13. **O que foi feito com IA?** Explicar a declaração do README e demonstrar que o código foi compreendido e revisado pelos integrantes.

## Perguntas adicionais sobre as aulas

- O que muda entre cor uniforme, cor de vértice e textura? Mostrar o uniform baseColor, o VBO vertexColor e o sampler da imagem; são canais distintos.
- Quem interpola as cores e UV? O rasterizador, entre os dois estágios de shader; o fragment shader recebe os valores interpolados.
- Por que todos os arrays devem ter o mesmo número de vértices? Os atributos de um mesmo índice descrevem o mesmo vértice. A validação impede streams incompletos.
- O que é um texel? Uma amostra da imagem de textura, que não precisa corresponder a um único pixel na tela.
- Por que filtros não mudam a geometria? Eles afetam a consulta de texels. Comparar F4/F5 pausado e depois F8 para inspecionar os mesmos triângulos.
- O que o sampler recebe? O número da unidade de textura; o identificador da textura é ligado a essa unidade por glBindTexture.
- Como foi usado o PDF de visão? Para escolhas de separação cromática, foco e legibilidade. A conversão em cinza é ilustrativa e não simula uma condição clínica.

## Pergunta sobre a correção de colisões

Por que apenas comparar os centros não bastava? A cauda ocupa um volume que muda durante a virada. O programa agora compara caixas das partes transformadas, incluindo cauda e sensor, e rejeita cada subpasso inseguro. A distância de 3,8 unidades evita contatos no percurso normal; o detector continua ativo como proteção. Não há quique ou forças: a resposta é interromper o movimento preservando a última pose segura.

Na etapa de reconhecimento, apontar a luz saindo da lente e a iluminação na superfície do dinossauro. Pausar para girar a câmera e mostrar a profundidade do feixe. Explicar que é um efeito emissivo mais contribuição focal no Phong, mantendo a sombra direcional existente.

Mostrar o parque de pesquisa, a separação entre a pista e as estruturas e a composição por primitivas. Explicar que o agrupamento estático reduz chamadas de desenho, preservando UV/normais e mantendo as partes animadas separadas.
