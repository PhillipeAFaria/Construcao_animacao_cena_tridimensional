# Correção da interação — versão 1.3

## Problema e mudança de comportamento

A distância longitudinal de duas unidades usada nas versões anteriores não reservava espaço para a cauda durante a virada do dinossauro. A imagem fornecida pelo usuário mostrou a interpenetração. O teste `tests/check_collision_scene.py` reproduz o defeito com as peças reais do modelo, recolocando o rover na posição antiga durante a resposta.

O rover agora encerra a aproximação a **3,8 unidades longitudinais** do dinossauro e mantém essa distância durante o acompanhamento. O deslocamento inicial passa de cinco para 3,2 unidades nos mesmos cinco segundos, com smoothstep. O sensor ajusta a varredura à nova posição. O dinossauro continua respondendo à chegada e o rover só parte após a virada, preservando a interação coordenada.

Além da correção do trajeto, a aplicação agora verifica colisões antes de aceitar cada avanço. A proteção considera todas as peças dos personagens, incluindo a cauda articulada, cabeça, mandíbula, rodas, antena e sensor. Não é apenas uma verificação da distância entre os centros.

## Implementação

- `collision.py`: `CompoundCollider` extrai os limites locais dos vértices de cada malha e gera oito cantos da caixa. `boxes` transforma esses cantos pelas matrizes atuais da hierarquia e calcula AABBs de mundo.
- `CollisionWorld.contacts` primeiro compara os envelopes completos dos dois modelos. Se necessário, compara as caixas das peças em X, Y e Z, com margem de segurança de 0,10 unidade.
- A transformação utiliza as partes efetivamente desenhadas; acompanha translação, escala e rotação, inclusive o movimento da cauda. Não se baseia em uma caixa fixa enquanto o modelo gira.
- `Simulation.update(dt, can_advance)` divide o movimento em subpassos de no máximo 1/120 s quando o guardião está ativo. A aplicação passa `Application.can_advance`, que aplica a pose candidata e verifica os colisores reais.
- Se uma pose candidata fica próxima demais, todo o subpasso é rejeitado: posição, tempo, estado, ângulo das rodas e articulações voltam juntos ao último estado aceito. A cena também é restaurada, e a interface informa que o movimento está bloqueado. A câmera e a renderização continuam disponíveis; R reinicia.
- `FOLLOW_DISTANCE` em `simulation.py` centraliza a nova distância. `MAX_COLLISION_STEP` controla o intervalo de verificação. `SAFETY_MARGIN` em `collision.py` define a folga preventiva.

## Escopo e limites

São colisões **cinemáticas entre o rover e o dinossauro**, sem forças, impulsos ou quique. A câmera, o chão e os objetos estáticos não recebem resposta física. As AABBs compostas são conservadoras: podem bloquear uma aproximação que uma comparação exata entre triângulos permitiria. Essa margem é apropriada para a coreografia de demonstração.

Os subpassos e a margem foram dimensionados e verificados para as velocidades e rotações desta cena. Isso reduz o risco de atravessamento em baixa taxa de quadros; não é um algoritmo geral de colisão contínua para teletransportes ou velocidades ilimitadas. Se a geometria ou a trajetória forem alteradas, repetir os testes antes de diminuir a distância de segurança.

O callback é opcional na classe de simulação para permitir testes isolados sem OpenGL; **o loop normal da aplicação sempre o utiliza**. Os testes puramente visuais das aulas podem posicionar uma pose diretamente, mas a coreografia corrigida também foi amostrada densamente para conferir esses estados.

## Validação

- 19 testes unitários: sobreposição, toque, margem, separação vertical, hierarquia, rotação e escala; região bloqueadora estreita com dt grande; rejeição restaurando tempo/estado/rodas; preservação da lógica anterior.
- 3.841 poses verificadas ao longo dos 16 segundos, com amostragem de 1/240 s. Nenhuma colisão na trajetória corrigida. Menor distância entre AABBs de peças: aproximadamente **0,432 unidade**, superior à margem de 0,10.
- Percurso com guardião ativo a 15, 30, 60 e 144 FPS, incluindo velocidade 2×: todos chegaram ao estado CONCLUIDO, sem bloqueios na trajetória planejada.
- Configuração inválida forçada: bloqueio e restauração do estado confirmados.
- Regressão do problema antigo: contato envolvendo a cauda reproduzido com a distância anterior.

Execute nesta pasta, com o ambiente instalado:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests/check_collision_scene.py
.\.venv\Scripts\python.exe main.py --validate
```

As evidências são `evidencias/validacao_colisoes.json`, `evidencias/12_virada_sem_interpenetracao.png` e o relatório do modo `--validate`, que inclui o número de verificações de colisão executadas no loop real.
