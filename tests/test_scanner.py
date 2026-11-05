import unittest
import numpy as np
from scanner import beam_matrix,ray_distance

class ScannerTests(unittest.TestCase):
    def test_beam_origin_axis_and_tip(self):
        origin=np.array([1.,2,3]);direction=np.array([1.,0,0])
        matrix=beam_matrix(origin,direction,4,.5)
        np.testing.assert_allclose((matrix@np.array([0,0,0,1]))[:3],origin)
        np.testing.assert_allclose((matrix@np.array([0,0,1,1]))[:3],origin+4*direction)

    def test_parallel_axis_and_range_limit(self):
        low=np.array([[3.,-1,-1],[1,4,4]]);high=low+2
        self.assertAlmostEqual(ray_distance(np.zeros(3),np.array([1.,0,0]),low,high),3)
        self.assertAlmostEqual(ray_distance(np.zeros(3),np.array([-1.,0,0]),low,high),4.8)

    def test_vertical_beam_and_invalid_direction(self):
        self.assertTrue(np.isfinite(beam_matrix([0,0,0],[0,1,0],2,.2)).all())
        with self.assertRaises(ValueError):beam_matrix([0,0,0],[0,0,0],2,.2)
