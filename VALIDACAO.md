# Registro de validação — versão 1.3 — 04/11/2026

## Ambiente medido

- Windows; Python 3.12.14, Pygame 2.6.1, PyOpenGL 3.1.10, NumPy 2.2.6, Pillow 11.3.0.
- GPU: NVIDIA GeForce GTX 1660 Ti/PCIe/SSE2.
- Contexto OpenGL: 3.3.0 NVIDIA 610.88.
- Renderização: janela de 1200×760; mapa de sombras 2048×2048.

## Resultados

| Verificação | Resultado |
|---|---|
| Lógica sem GPU | 19 testes aprovados |
| Independência de FPS | Poses equivalentes a 30, 60 e 144 FPS em cinco instantes; tolerância de sete casas decimais |
| Coordenação | Rover espera durante reconhecimento e resposta; acompanhamento liberado após virada |
| Pausa/retomada e reinício | Estado e pose preservados durante pausa; retomada e reset aprovados |
| Passos grandes | Intervalo que cruza vários estados termina corretamente sem acumular atraso de quadro |
| Execução gráfica | 1.000 quadros, estado final CONCLUIDO, nenhum erro reportado por glGetError |
| Shadow mapping dinâmico | 264.003 componentes do mapa mudaram entre poses distintas |
| Efeito visível das sombras | 37.735 pixels mudaram mais de oito níveis em pelo menos um canal ao desligar a comparação de sombras |
| Câmera durante pausa | Pose da simulação permanece igual e imagem muda ao alterar a câmera |
| Shaders | Phong, depth e painel compilados e vinculados na GPU real |
| Instalador Windows | Mesmo instalador já verificado na versão anterior; mesmas quatro dependências, sem alteração |
| Sintaxe Python | compileall aprovado para aplicação, framework usado, testes e gerador de textura |
| Revisão visual | Capturas reais de reconhecimento, acompanhamento, laboratório UV e foco visual inspecionadas |
| Continuidade da animação | Poses contínuas nas quatro transições; chegada com velocidade tendendo a zero |
| Comandos da interface | Pausa, câmeras, acompanhamento, velocidade, repetição, sombras, captura, Home, zoom por mouse, reinício e saída exercitados pelo tratador de eventos real |
| Pacote de entrega | ZIP extraido e executado em OpenGL; integridade SHA-256 conferida para todos os arquivos |
| Cores interpoladas na GPU | Amostras RGB [64,64,51], [128,128,51] e [191,191,51], dentro da tolerância de dois níveis |
| UV e samplers | Origem inferior esquerda, quatro quadrantes, repetição e offset conferidos com textura controlada 2×2 |
| Filtros de textura | NEAREST/LINEAR/MIPMAP produzem diferenças visíveis; filtro do mapa de sombras preservado |
| Comparações das aulas | Cores, grade UV, foco, cinza e malha alteram a imagem e preservam a pose pausada |
| Streams de atributos | Tamanhos incompatíveis rejeitados antes de montar o VAO |
| Guardião no loop real | 1.920 verificações em 1.000 quadros; sequência concluída com a trajetória corrigida e sem bloqueios |
| Colisões no percurso | 3.841 poses amostradas a 1/240 s; sem contatos e folga mínima AABB de 0,432 unidade |
| FPS e velocidade | Percurso protegido a 15, 30, 60 e 144 FPS, incluindo 2×; todos concluídos |
| Regressão e bloqueio | Sobreposição antiga da cauda reproduzida; colisão forçada rejeitada sem avanço do tempo |
| Robustez do tempo | Rejeição de dt infinito, NaN e negativo |
| Desempenho da cena 1.3 | 40 quadros com guardião de colisões, sem limitador e sem HUD: 1,401 s / 28,6 FPS |

Arquivos de evidência: `evidencias/validacao_gpu.json`, `evidencias/teste_sombras.json` e capturas PNG. As comparações das aulas estão em `evidencias/validacao_aulas.json`. A imagem de câmera durante pausa vem do teste de GPU e omite intencionalmente o painel 2D.

A medição de desempenho é curta e sujeita a variações de carga da máquina. Não equivale à taxa garantida da aplicação completa. O roteiro reproduzível está em `tests/check_performance.py`; a referência atual inclui o custo das colisões. Os números anteriores no README são históricos.

## Limites da verificação

Foi executada renderização real com contexto OpenGL, não apenas análise estática ou modo headless. Não foi feito um teste manual completo de todos os atalhos por uma pessoa nem uma apresentação em sala. Os integrantes devem conferir os controles e o desempenho na máquina de apresentação. A filtragem PCF suaviza bordas de sombras, sem simular penumbra física. A modelagem é deliberadamente estilizada. Não há garantia de nota ou comprovação de domínio individual.

O pacote não inclui intérprete Python, bibliotecas instaladas ou executável autônomo. As dependências são reproduzidas pelo requirements.txt. A primeira instalação requer internet. O uso em outras GPUs, versões de driver ou sistemas operacionais ainda precisa de verificação local.

As colisões são cinemáticas entre os dois personagens, por AABBs conservadoras das peças. A câmera e os elementos estáticos não têm resposta física. Evidência: `evidencias/validacao_colisoes.json`.
