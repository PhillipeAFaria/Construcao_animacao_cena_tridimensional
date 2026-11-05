# Parque de pesquisa — versão 1.5

O cenário foi ampliado para representar um parque de demonstração com infraestrutura de pesquisa. Os personagens, o scanner e a coreografia permanecem no centro da cena.

## Elementos acrescentados

- Estação de pesquisa ao fundo, com janelas, porta, cobertura, antena e placa de imagem original.
- Portal de chegada além do percurso dos personagens.
- Calçada modular, meio-fio e bancos de observação.
- Lago ornamental estático, com borda e pequenos elementos vegetais.
- Palmeiras de folhas segmentadas, samambaias e canteiros, além das árvores de blocos existentes.
- Relevo em degraus ao fundo, preservando o estilo geométrico dos modelos.
- Fundo de céu com gradiente e formas suaves de nuvens.

Os edifícios, bancos, vegetação e o portal foram posicionados fora do corredor usado pela coreografia. Não há terceiro personagem animado. O lago é uma superfície com material de brilho especular; não simula fluidos ou reflexos do ambiente. O céu é um fundo estilizado em tela, não uma atmosfera física nem uma esfera celeste.

## Organização do código

| Recurso | Local |
|---|---|
| Composição das novas estruturas | `scenery.py`: `decorate` |
| Partes básicas de caixas/cilindros | `models.py`: `Models.part` |
| Grupo do ambiente | `main.py`: `Application.environment`, `environment_root` |
| Agrupamento de malhas estáticas | `scenery.py`: `batch_static` |
| Céu em passagem separada | `sky.py`; `shaders/sky.vert`, `shaders/sky.frag` |
| Ordem de desenho | `main.py`: `Application.draw_scene` |
| Nova placa | `assets/estacao.png`; `tools/gerar_cenario.py` |

Todas as novas estruturas são composições das primitivas do framework, sem arquivos de malhas externas. A placa foi gerada com Pillow e uma fonte do sistema; nenhuma imagem externa foi usada. As novas implementações foram elaboradas com apoio do OpenAI Codex.

## Desempenho e transformações

O ambiente detalhado produziria 287 malhas estáticas individuais. `batch_static` agrupa os triângulos por material e comportamento de sombra, reduzindo esse conjunto para **49 malhas**, com 3.618 triângulos no total.

Antes do agrupamento, cada vértice é transformado para o mundo pela matriz completa da peça; normais são transformadas pela inversa transposta e normalizadas. As UV e cores de vértice são preservadas. As novas malhas ficam sob o nó de ambiente, cuja matriz é identidade. Texturas, iluminação, material e sombra continuam calculados pelo mesmo pipeline.

Somente o ambiente estático é agrupado. Rover, dinossauro, articulações, anel de reconhecimento e feixe luminoso continuam independentes. Se for necessário animar um elemento do cenário, ele deverá ser excluído do agrupamento ou reconstruído separadamente.

O teste `tests/check_scenery.py` compara imagens antes/depois de agrupar peças com escala e rotação. Nesta máquina, nenhum pixel diferiu mais de cinco níveis de cor. Isso verifica que a otimização preserva transformações e aparência no experimento controlado.

## Renderização

O céu é desenhado primeiro sem teste de profundidade; o teste é restaurado em seguida. A cena principal preserva a cor desse fundo, limpa o buffer de profundidade e executa o shadow mapping e os materiais iluminados. Depois são desenhados o feixe translúcido e o HUD.

O céu recebe apenas posição/UV e matrizes M/V/P. Seu fragment shader calcula o gradiente e as formas suaves diretamente. Os modos de laboratório continuam atuando nos materiais da cena, não nesse fundo ou no HUD.

## Verificação

Execute, após preparar o ambiente:

```powershell
.\.venv\Scripts\python.exe tests/check_scenery.py
.\.venv\Scripts\python.exe main.py --validate
```

O primeiro confere dados finitos, comprimentos dos atributos, redução das malhas, equivalência visual do agrupamento e passagem completa de céu/cena/scanner/HUD. Os resultados ficam em `evidencias/validacao_cenario.json` e `evidencias/14_cenario_parque.png`.

As colisões cinemáticas entre rover e dinossauro continuam ativas; os objetos estáticos e a câmera não receberam um novo motor de física. O benchmark histórico de versões anteriores não deve ser usado como medição deste cenário.
