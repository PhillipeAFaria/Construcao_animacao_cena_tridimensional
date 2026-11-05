import unittest
from geometry_tools import gradient_colors
from types import SimpleNamespace
from py3d.geometry.geometry import Geometry

class GradientTests(unittest.TestCase):
    def test_shared_positions_get_same_colors(self):
        points=[[0,-2,0],[1,0,1],[0,2,0],[0,-2,0]]
        colors=gradient_colors(points,low=(0,0,0),high=(1,1,1))
        self.assertEqual(colors[0],colors[3])
        self.assertEqual(colors[1],[.5,.5,.5])
        self.assertEqual(len(colors),len(points))

    def test_flat_geometry_does_not_divide_by_zero(self):
        colors=gradient_colors([[0,0,0],[1,0,0]],low=(0,0,0),high=(1,1,1))
        self.assertEqual(colors,[[.5,.5,.5],[.5,.5,.5]])

    def test_mismatched_vertex_streams_are_rejected_before_rendering(self):
        geometry=Geometry()
        geometry._vertex_count=3
        geometry._attribute_dict={'vertexPosition':SimpleNamespace(data=[[0,0,0]]*3),
                                  'vertexColor':SimpleNamespace(data=[[1,1,1]]*2)}
        with self.assertRaisesRegex(ValueError,'vertexColor'):
            geometry.validate_attributes()
