# Demonstração de dez minutos

Antes da aula: preencher nomes e contribuições no README; instalar as dependências; executar a aplicação na máquina que será usada; confirmar OpenGL, legibilidade, pausa e sombra. Ambos devem ler o código integrado. O roteiro é uma proposta de distribuição, não prova de participação.

| Tempo | Responsável sugerido | Conteúdo |
|---|---|---|
| 0:00–1:00 | Ambos | Identificar dupla e temas. Explicar parque de demonstração e objetivo do reconhecimento. |
| 1:00–2:00 | Integrante 1 | Mostrar o ciclo completo. Apontar rover aguardando o sensor e a virada do dinossauro. |
| 2:00–3:00 | Integrante 1 | Pausar com Espaço, mover a câmera com setas e W/S, alternar vistas com 1/2/3 e retomar. Use [ para desacelerar se necessário. Explicar tempo decorrido. |
| 3:00–4:00 | Integrante 2 | Mostrar composição dos modelos e pivôs de cauda, pernas, rodas e sensor em models.py. |
| 4:00–5:00 | Integrante 1 | Abrir simulation.py: estados, transições e reaproveitamento do dt. |
| 5:00–6:00 | Integrante 2 | Mostrar textura do terreno, UV, materiais, luz direcional e normais. |
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
