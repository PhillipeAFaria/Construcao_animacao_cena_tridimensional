# Registro de validação — 04/11/2026

## Ambiente medido

- Windows; Python 3.12.14, Pygame 2.6.1, PyOpenGL 3.1.10, NumPy 2.2.6, Pillow 11.3.0.
- GPU: NVIDIA GeForce GTX 1660 Ti/PCIe/SSE2.
- Contexto OpenGL: 3.3.0 NVIDIA 610.88.
- Renderização: janela de 1200×760; mapa de sombras 2048×2048.

## Resultados

| Verificação | Resultado |
|---|---|
| Lógica sem GPU | 6 testes aprovados |
| Independência de FPS | Poses equivalentes a 30, 60 e 144 FPS em cinco instantes; tolerância de sete casas decimais |
| Coordenação | Rover espera durante reconhecimento e resposta; acompanhamento liberado após virada |
| Pausa/retomada e reinício | Estado e pose preservados durante pausa; retomada e reset aprovados |
| Passos grandes | Intervalo que cruza vários estados termina corretamente sem acumular atraso de quadro |
| Execução gráfica | 1.000 quadros, estado final CONCLUIDO, nenhum erro reportado por glGetError |
| Shadow mapping dinâmico | 226.278 componentes do mapa mudaram entre poses distintas |
| Efeito visível das sombras | 8.834 pixels mudaram mais de oito níveis em pelo menos um canal ao desligar a comparação de sombras |
| Câmera durante pausa | Pose da simulação permanece igual e imagem muda ao alterar a câmera |
| Shaders | Phong, depth e painel compilados e vinculados na GPU real |
| Instalador Windows | Criação de ambiente virtual e instalação das quatro dependências verificadas |
| Sintaxe Python | compileall aprovado para aplicação, framework usado, testes e gerador de textura |
| Revisão visual | Capturas reais de acompanhamento e câmera durante pausa inspecionadas |

Arquivos de evidência: `evidencias/validacao_gpu.json`, `evidencias/teste_sombras.json` e capturas PNG. A imagem de câmera durante pausa vem do teste de GPU e omite intencionalmente o painel 2D.

## Limites da verificação

Foi executada renderização real com contexto OpenGL, não apenas análise estática ou modo headless. Não foi feito um teste manual completo de todos os atalhos por uma pessoa nem uma apresentação em sala. Os integrantes devem conferir os controles e o desempenho na máquina de apresentação. Sombras duras e modelagem estilizada são decisões de escopo. Não há garantia de nota ou comprovação de domínio individual.

O pacote não inclui intérprete Python, bibliotecas instaladas ou executável autônomo. As dependências são reproduzidas pelo requirements.txt. A primeira instalação requer internet. O uso em outras GPUs, versões de driver ou sistemas operacionais ainda precisa de verificação local.
