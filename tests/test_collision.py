import unittest
from itertools import product
from types import SimpleNamespace
import numpy as np
from collision import CompoundCollider,overlap_mask
from simulation import Simulation,MAX_COLLISION_STEP
from py3d.core_ext.object3d import Object3D
from py3d.core.matrix import Matrix

class CollisionTests(unittest.TestCase):
    def test_separated_touching_and_penetrating_boxes(self):
        a=np.array([[0.,0,0]]);b=np.array([[1.,1,1]])
        self.assertFalse(overlap_mask(a,b,a+2,b+2)[0,0])
        self.assertFalse(overlap_mask(a,b,a+1,b+1)[0,0])
        self.assertTrue(overlap_mask(a,b,a+.5,b+.5)[0,0])
        self.assertTrue(overlap_mask(a,b,a+1.02,b+1.02,.10)[0,0])

    def test_height_is_considered(self):
        a=np.array([[0.,0,0]]);b=np.array([[1.,1,1]])
        self.assertFalse(overlap_mask(a,b,a+[0,2,0],b+[0,2,0])[0,0])

    def test_hierarchy_rotation_and_scale_change_part_bounds(self):
        root=Object3D();pivot=Object3D();mesh=Object3D()
        root.add(pivot);pivot.add(mesh)
        positions=[list(p) for p in product((-1,1),repeat=3)]
        mesh.geometry=SimpleNamespace(attribute_dict={'vertexPosition':SimpleNamespace(data=positions)})
        mesh.local_matrix=Matrix.make_translation(0,0,-2)@np.diag([.2,.3,1.,1.])
        collider=CompoundCollider(root,'modelo')
        low,high=collider.boxes();self.assertAlmostEqual(low[0,2],-3)
        root.rotate_y(np.pi/2);root.set_position([5,0,0])
        low,high=collider.boxes()
        np.testing.assert_allclose(low[0],[2,-.3,-.2],atol=1e-12)
        np.testing.assert_allclose(high[0],[4,.3,.2],atol=1e-12)

    def test_large_dt_does_not_skip_a_blocking_region(self):
        sim=Simulation();positions=[]
        def guard(pose):
            positions.append(pose.rover_x)
            return not (-5.01<pose.rover_x<-4.99)
        sim.update(16,guard)
        self.assertTrue(sim.collision_blocked)
        self.assertLessEqual(sim.rover_x,-5.01)
        self.assertEqual(sim.stage,0)
        self.assertLess(sim.time,5)
        self.assertEqual(sim.prevented_collisions,1)
        self.assertLess(np.max(np.abs(np.diff(positions))),.02)

    def test_rejected_transition_restores_clock_wheels_and_state(self):
        sim=Simulation();sim.update(4.999)
        before=(sim.time,sim.elapsed,sim.stage,sim.pose())
        sim.update(.02,lambda pose: False)
        self.assertEqual(before,(sim.time,sim.elapsed,sim.stage,sim.pose()))
        sim.paused=True;sim.update(10,lambda pose: self.fail('Paused simulation must not move'))
        sim.reset();self.assertEqual(sim.prevented_collisions,0)

    def test_unblocked_guard_preserves_timing(self):
        sim=Simulation();count=0
        def guard(pose):
            nonlocal count
            count+=1
            return True
        sim.update(16,guard)
        self.assertEqual(sim.name,'CONCLUIDO')
        self.assertAlmostEqual(sim.time,16)
        self.assertGreaterEqual(count,round(16/MAX_COLLISION_STEP))
