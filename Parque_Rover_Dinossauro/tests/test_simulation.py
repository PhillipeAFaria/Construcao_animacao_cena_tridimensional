import unittest
from simulation import Simulation

class SimulationTests(unittest.TestCase):
    def advance(self,fps,seconds):
        sim=Simulation()
        for _ in range(round(seconds*fps)):
            sim.update(1/fps)
        return sim

    def test_frame_rate_independence(self):
        for seconds in (3,6,8,12,17):
            reference=self.advance(30,seconds)
            for fps in (60,144):
                actual=self.advance(fps,seconds)
                self.assertEqual(actual.stage,reference.stage)
                for key,value in vars(actual.pose()).items():
                    self.assertAlmostEqual(value,getattr(reference.pose(),key),places=7)

    def test_causal_sequence(self):
        sim=Simulation(); sim.update(5)
        self.assertEqual(sim.name,'RECONHECIMENTO'); self.assertAlmostEqual(sim.rover_x,-2)
        sim.update(1)
        self.assertAlmostEqual(sim.dino_x,0); self.assertAlmostEqual(sim.rover_x,-2)
        sim.update(1)
        self.assertEqual(sim.name,'RESPOSTA')
        sim.update(1)
        self.assertGreater(sim.pose().dino_yaw,0); self.assertEqual(sim.dino_x,0)
        sim.update(1)
        self.assertEqual(sim.name,'ACOMPANHAMENTO')
        sim.update(3)
        self.assertGreater(sim.dino_x,0); self.assertAlmostEqual(sim.dino_x-sim.rover_x,2)

    def test_pause_resume(self):
        sim=Simulation(); sim.update(6); before=sim.pose()
        sim.paused=True; sim.update(40)
        self.assertEqual(sim.pose(),before)
        sim.paused=False; sim.update(1)
        self.assertEqual(sim.name,'RESPOSTA')

    def test_large_step_and_end(self):
        sim=Simulation(); sim.update(100)
        self.assertEqual(sim.name,'CONCLUIDO'); self.assertAlmostEqual(sim.time,16)
        pose=sim.pose(); sim.update(50); self.assertEqual(sim.pose(),pose)

    def test_reset(self):
        sim=Simulation(); sim.update(12); sim.paused=True; sim.reset()
        self.assertEqual(sim.name,'APROXIMACAO'); self.assertFalse(sim.paused)
        self.assertEqual(sim.rover_x,-7)

    def test_negative_dt_rejected(self):
        with self.assertRaises(ValueError): Simulation().update(-1)

if __name__=='__main__': unittest.main()
