"""Mede 40 quadros da cena com GPU sincronizada; sem HUD ou limitador de FPS."""
import sys
import time
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pygame
import OpenGL.GL as GL
from main import Application

app=Application(SimpleNamespace(validate=False))
try:
    app.controls(0)
    for _ in range(5):
        app.apply_pose(); app.renderer.render(app.scene,app.camera)
    GL.glFinish()
    start=time.perf_counter()
    for _ in range(40):
        pygame.event.pump()
        app.sim.update(1/60)
        app.apply_pose()
        app.renderer.render(app.scene,app.camera)
    GL.glFinish()
    elapsed=time.perf_counter()-start
    print({'frames':40,'seconds':round(elapsed,3),'fps':round(40/elapsed,1)})
finally:
    pygame.quit()
