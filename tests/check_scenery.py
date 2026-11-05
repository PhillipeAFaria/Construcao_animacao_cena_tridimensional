"""Verifica batching estático, imagem e passagem completa de céu/scanner/HUD."""
import sys,json
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pygame
import OpenGL.GL as GL
from main import Application,ROOT
from scenery import batch_static
from py3d.core_ext.object3d import Object3D
from py3d.core_ext.mesh import Mesh

app=Application(SimpleNamespace(validate=False))
try:
    report=app.environment_batch
    assert report['static_meshes_after']<report['static_meshes_before']/3,report
    for node in app.environment_root.descendant_list:
        if isinstance(node,Mesh):
            node.geometry.validate_attributes()
            assert np.isfinite(node.geometry.attribute_dict['vertexPosition'].data).all()
    # Controlled before/after image detects broken transforms/normals in batching.
    temp=Object3D();app.scene.add(temp)
    for i in range(3):
        mesh=app.models.part(temp,(-2+i,2.5,-2),(0.4,.6,.3),(.67,.41,.26))
        mesh.rotate_y(.25*i);mesh.rotate_z(.16)
    app.sim.update(6);app.apply_pose();app.controls(0)
    app.draw_scene()
    before=np.frombuffer(GL.glReadPixels(0,0,*app.size,GL.GL_RGB,GL.GL_UNSIGNED_BYTE),dtype=np.uint8).copy()
    batch_static(temp);app.draw_scene()
    after=np.frombuffer(GL.glReadPixels(0,0,*app.size,GL.GL_RGB,GL.GL_UNSIGNED_BYTE),dtype=np.uint8).copy()
    delta=abs(before.astype(int)-after.astype(int))
    changed=int(np.count_nonzero(np.max(delta.reshape(-1,3),axis=1)>5))
    assert changed<100,changed
    app.scene.remove(temp)
    app.draw_scene();app.hud.draw(app.sim,True,appearance=app.appearance)
    app.capture(ROOT/'evidencias/14_cenario_parque.png')
    assert GL.glGetError()==GL.GL_NO_ERROR
    data={**report,'batch_comparison_pixels_above_5':changed,'gl_error':0}
    (ROOT/'evidencias/validacao_cenario.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(data)
finally:pygame.quit()
