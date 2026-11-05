"""Regressão da cauda e percurso inteiro usando as peças reais dos modelos."""
import sys,json
from pathlib import Path
from dataclasses import replace
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pygame
import OpenGL.GL as GL
from main import Application,ROOT
from simulation import Simulation

app=Application(SimpleNamespace(validate=False))
out=ROOT/'evidencias';out.mkdir(exist_ok=True)
try:
    app.sim.update(8)
    legacy=replace(app.sim.pose(),rover_x=-2)
    app.apply_pose(legacy)
    legacy_contacts=app.collisions.contacts(margin=0)
    assert any('cauda' in b for a,b in legacy_contacts),legacy_contacts
    app.apply_pose()
    assert not app.collisions.contacts()
    app.azimuth=-1.3;app.elevation=.30;app.radius=9
    app.target=[-1.5,1.2,0];app.controls(0)
    app.renderer.render(app.scene,app.camera)
    app.hud.draw(app.sim,True,appearance=app.appearance)
    app.capture(out/'12_virada_sem_interpenetracao.png')

    # Sample every 1/240 s, twice the collision integration frequency.
    app.sim.reset();minimum=float('inf');samples=0
    for _ in range(3841):
        app.apply_pose()
        contacts=app.collisions.contacts()
        assert not contacts,(app.sim.time,contacts)
        minimum=min(minimum,app.collisions.clearance())
        samples+=1
        app.sim.update(1/240)
    # Also exercise the real runtime guard at low/high FPS and 2x speed.
    runs=[]
    for fps,speed in ((15,2),(30,1),(60,1),(144,2)):
        app.sim.reset()
        for _ in range(round(16*fps/speed)):
            app.sim.update(speed/fps,app.can_advance)
        assert app.sim.stage==4,(fps,speed,app.sim.name)
        assert app.sim.prevented_collisions==0
        runs.append({'fps':fps,'velocidade':speed,'estado':app.sim.name})
    # Force a bad configuration: guard must reject it and restore the scene.
    app.sim.reset();app.sim.update(7.99)
    original=app.apply_pose
    def obstructed(pose=None):
        pose=app.sim.pose() if pose is None else pose
        original(replace(pose,rover_x=-2))
    app.apply_pose=obstructed
    time=app.sim.time
    app.sim.update(.5,app.can_advance)
    assert app.sim.collision_blocked and app.sim.time==time
    app.apply_pose=original
    app.apply_pose()
    assert GL.glGetError()==GL.GL_NO_ERROR
    report={'legacy_tail_overlap_reproduced':True,'samples':samples,
        'minimum_part_aabb_clearance':minimum,'collision_margin':app.collisions.margin,
        'runs':runs,'forced_collision_blocked':True,'gl_error':0}
    (out/'validacao_colisoes.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))
finally:pygame.quit()
