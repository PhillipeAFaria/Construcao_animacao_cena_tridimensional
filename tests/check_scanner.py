"""Valida feixe, iluminação sobre a superfície, origem no sensor e pausa."""
import sys,json
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pygame
import OpenGL.GL as GL
from main import Application,ROOT

app=Application(SimpleNamespace(validate=False))
def pixels():return np.frombuffer(GL.glReadPixels(0,0,*app.size,GL.GL_RGB,GL.GL_UNSIGNED_BYTE),dtype=np.uint8).copy()
def difference(a,b):return int(np.count_nonzero(np.max(abs(a.astype(int)-b.astype(int)).reshape(-1,3),axis=1)>3))
try:
    app.sim.update(6);app.apply_pose();app.controls(0)
    app.renderer.render(app.scene,app.camera);baseline=pixels()
    app.scanner.update(app.sim)
    assert app.scanner.active and app.scanner.intensity>.99
    expected=(app.sensor.global_matrix@np.array([.455,0,0,1]))[:3]
    np.testing.assert_allclose(app.scanner.origin,expected)
    app.renderer.render(app.scene,app.camera);spot=pixels()
    spot_diff=difference(baseline,spot);assert spot_diff>50,spot_diff
    app.scanner.render(app.camera);beam=pixels()
    beam_diff=difference(spot,beam);assert beam_diff>100,beam_diff
    assert GL.glGetBooleanv(GL.GL_DEPTH_WRITEMASK)
    app.hud.draw(app.sim,True,appearance=app.appearance)
    app.capture(ROOT/'evidencias/13_reconhecimento_luminoso.png')
    app.sim.paused=True;time=app.sim.time;origin=app.scanner.origin.copy()
    app.sim.update(10,app.can_advance);app.scanner.update(app.sim)
    assert app.sim.time==time
    np.testing.assert_allclose(app.scanner.origin,origin)
    for instant in (0,4,8,12,16):
        app.sim.reset();app.sim.update(instant);app.apply_pose();app.scanner.update(app.sim)
        assert not app.scanner.active and all(not m.visible for m in app.scanner.meshes)
        assert all(m.uniform_dict['scannerActive'].data==0 for m in app.scanner.materials.values())
    assert GL.glGetError()==GL.GL_NO_ERROR
    report={'pixels_illuminated':spot_diff,'pixels_changed_by_beam':beam_diff,
        'origin_tracks_sensor':True,'pause_preserves_scan':True,'only_recognition_stage':True,
        'depth_write_restored':True,'gl_error':0}
    (ROOT/'evidencias/validacao_scanner.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(report)
finally:pygame.quit()
