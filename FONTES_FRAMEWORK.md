# Proveniência do framework

Fonte: https://github.com/ax-va/PyOpenGL-Pygame-Stemkoski-Pascale-2021

Snapshot: ZIP da branch main obtido em 04/11/2026 por https://codeload.github.com/ax-va/PyOpenGL-Pygame-Stemkoski-Pascale-2021/zip/refs/heads/main . SHA-256 do arquivo-fonte baixado: `485be3a402fbde37b045421177a1eba822ea6dbf48e7da9e008a4b7fa0a50d20`. A branch é mutável; o hash identifica o conteúdo consultado. Não foi registrada uma revisão Git específica.

O README original identifica os exemplos como baseados no livro de Lee Stemkoski e Michael Pascale. Esta entrega preserva essa atribuição. Não foi encontrado arquivo LICENSE na raiz do snapshot consultado; esta documentação não atribui ao código de terceiros uma licença que a fonte não declarou. O material é incluído como referência acadêmica identificada, conforme o enunciado permite adaptação de exemplos; não é declarado domínio público nem autoria da dupla.

Foram mantidos apenas os módulos Python transitivamente utilizados e os inicializadores de pacotes. A aplicação usa diretamente Object3D, Matrix, Scene, Camera, Mesh, Renderer, Texture, RectangleGeometry, BoxGeometry, CylinderGeometry, PhongMaterial, TextureMaterial, AmbientLight e DirectionalLight; seus módulos de apoio incluem Attribute, Uniform, Geometry, geometria cilíndrica e polígonos das tampas, Material, LightedMaterial, Light, Shadow, RenderTarget, DepthMaterial e Utils.

## Adaptações realizadas com apoio do Codex

- `core_ext/object3d.py`: atribuição indexada de posição para compatibilidade com NumPy 2, que removeu ndarray.itemset.
- `core_ext/renderer.py`: preservar/restaurar cor de limpeza após a passagem de sombras; garantir estado de preenchimento e culling na passagem de sombras.
- `core_ext/render_target.py`: textura RGBA32F e nearest para preservar precisão da profundidade armazenada como cor; mantém renderbuffer de profundidade, como na arquitetura original.
- `material/phong.py`: shaders extraídos para arquivos GLSL efetivamente carregados em tempo de execução; nesta cena os shaders declaram duas fontes de luz (ambiente e direcional).
- `shaders/phong.vert`: localização explícita de vertexPosition=0, compartilhada com a passagem depth; matriz inversa transposta para normais sob escala não uniforme.
- `shaders/phong.frag`: verificação dos limites do mapa de sombras. Permanecem os ramos de suporte a bump e luz pontual, desativados nesta cena.
- `material/depth.py` e `shaders/depth.*`: fontes externas e localização explícita de posição.
- `material/texture.py` e `shaders/hud.*`: fontes externas para o painel.
- `main.py`: volume ortográfico da câmera da luz, resolução e bias configurados para este ambiente; execução Pygame própria em vez de copiar a classe Base não utilizada.

## Arquivos específicos desta atividade

`main.py`, `models.py`, `simulation.py`, `tests/`, `tools/`, scripts de preparação, terreno PNG e documentação foram elaborados para esta solicitação com apoio do Codex. As imagens em evidencias são capturas reais da aplicação, não imagens geradas como substituição da renderização 3D.

## Adaptações adicionais da versão 1.1

- `shaders/phong.frag`: PCF de nove comparações (3×3) e bias ajustado pelo ângulo entre a normal e a luz. Mantém a arquitetura de shadow mapping do framework.
- `core_ext/renderer.py`: atributo opcional `cast_shadow` exclui apenas indicadores da passagem de sombras.
- `core_ext/renderer.py`: matrizes globais calculadas uma vez por quadro; uniforms de material e câmera enviados uma vez por material/passagem; apenas a matriz de modelo varia por objeto. Samplers são religados quando necessário. A ordem de desenho é preservada e o cache é recriado a cada chamada de renderização.
- `core_ext/mesh.py`: setter público de `visible` permite ocultar e reexibir os indicadores.
- `models.py`, `simulation.py` e `main.py`: acabamento dos modelos, smoothstep, cabeça e mandíbula articuladas, anel de reconhecimento, parque, comandos e painel ampliados, com apoio do Codex.
- `assets/placa.png`: nova textura original, gerada por `tools/gerar_placa.py` com Pillow e uma fonte do sistema. Não foi usado gerador de imagens para substituir modelos 3D.

## Adaptações adicionais da versão 1.2 com apoio do Codex

- `material/phong.py` e `shaders/phong.*`: atributo de cor, passagem interpolada, `useVertexColors`, `repeatUV`, `offsetUV`, `focusFactor` e `grayScale`.
- `geometry/geometry.py` e `core_ext/mesh.py`: validação dos comprimentos dos atributos e da contagem de vértices antes de montar o VAO.
- `geometry_tools.py`, `appearance.py`, modelos, texturas originais e laboratório de comparações: aplicação específica dos conteúdos dos PDFs, não componentes originalmente atribuídos aos autores do framework.
- Fontes de aula, páginas, decisões e limites: `APLICACAO_DOS_PDFS.md`; identificação por hash em `FONTES_PDFS.json`.
