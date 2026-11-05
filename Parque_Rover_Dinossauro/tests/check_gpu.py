"""Verificação real da GPU: mapa dinâmico, sombra visível, câmera durante pausa."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from types import SimpleNamespace
import json
import numpy as np
import pygame
import OpenGL.GL as GL
from main import Application, ROOT
from py3d.core_ext.mesh import Mesh

app=Application(SimpleNamespace(validate=False))
def draw():
    app.controls(0); app.apply_pose(); app.renderer.render(app.scene,app.camera)
    return np.frombuffer(GL.glReadPixels(0,0,*app.size,GL.GL_RGB,GL.GL_UNSIGNED_BYTE),dtype=np.uint8).copy()

def shadow():
    GL.glBindTexture(GL.GL_TEXTURE_2D,app.renderer.shadow_object.render_target.texture.texture_ref)
    return np.array(GL.glGetTexImage(GL.GL_TEXTURE_2D,0,GL.GL_RGBA,GL.GL_FLOAT)).copy()

draw(); first=shadow()
app.sim.update(12); lit=draw(); second=shadow()
changed=int(np.count_nonzero(np.abs(first-second)>1e-5))
assert changed>100, changed
materials={id(n.material):n.material for n in app.scene.descendant_list if isinstance(n,Mesh)}
for m in materials.values(): m.uniform_dict['useShadow'].data=False
no_shadow=draw()
diff=np.abs(lit.astype(int)-no_shadow.astype(int))
visible=int(np.count_nonzero(np.max(diff.reshape(-1,3),axis=1)>8))
assert visible>100, visible
for m in materials.values(): m.uniform_dict['useShadow'].data=True
app.sim.paused=True; pose=app.sim.pose(); app.sim.update(2)
assert pose==app.sim.pose()
app.azimuth+=.4; camera=draw()
assert np.count_nonzero(camera!=lit)>1000
app.capture(ROOT/'evidencias/06_camera_durante_pausa.png')
assert GL.glGetError()==GL.GL_NO_ERROR
report={'shadow_map_components_changed':changed,'pixels_affected_by_shadow':visible,
        'camera_during_pause':'PASS','gl_error':0}
(ROOT/'evidencias/teste_sombras.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report)
pygame.quit()
