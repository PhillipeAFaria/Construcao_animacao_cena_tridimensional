# Prepara cores por vértice que serão interpoladas na rasterização.
"""Cores por vértice: dados de entrada que serão interpolados pela rasterização."""

# Normaliza a posição no eixo escolhido e interpola cada canal entre duas cores.
def gradient_colors(positions, low=(.68,.78,.72), high=(1,1,1), axis=1):
    if not positions:
        return []
    values=[p[axis] for p in positions]
    start, end=min(values),max(values)
    result=[]
    for value in values:
        # Uma extensão nula no eixo recebe a cor intermediária e evita divisão por zero.
        t=(value-start)/(end-start) if end>start else .5
        result.append([a+(b-a)*t for a,b in zip(low,high)])
    return result

# Substitui as cores na mesma ordem das posições e atualiza seu VBO.
def apply_gradient(geometry, low=(.68,.78,.72), high=(1,1,1), axis=1):
    positions=geometry.attribute_dict['vertexPosition'].data
    colors=geometry.attribute_dict['vertexColor']
    colors.data=gradient_colors(positions,low,high,axis)
    colors.upload_data()
