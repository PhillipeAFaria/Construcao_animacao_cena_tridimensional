"""Cores por vértice: dados de entrada que serão interpolados pela rasterização."""

def gradient_colors(positions, low=(.68,.78,.72), high=(1,1,1), axis=1):
    if not positions:
        return []
    values=[p[axis] for p in positions]
    start, end=min(values),max(values)
    result=[]
    for value in values:
        t=(value-start)/(end-start) if end>start else .5
        result.append([a+(b-a)*t for a,b in zip(low,high)])
    return result

def apply_gradient(geometry, low=(.68,.78,.72), high=(1,1,1), axis=1):
    positions=geometry.attribute_dict['vertexPosition'].data
    colors=geometry.attribute_dict['vertexColor']
    colors.data=gradient_colors(positions,low,high,axis)
    colors.upload_data()
