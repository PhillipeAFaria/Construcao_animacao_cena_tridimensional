"""Testes reais de GPU dos conceitos aplicados a partir dos três PDFs."""
import sys,json
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pygame
import numpy as np
import OpenGL.GL as GL
from main import Application,ROOT
from py3d.core_ext.scene import Scene
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.texture import Texture
from py3d.geometry.rectangle import RectangleGeometry
from py3d.material.phong import PhongMaterial
from py3d.light.ambient import AmbientLight

app=Application(SimpleNamespace(validate=False))
out=ROOT/'evidencias';out.mkdir(exist_ok=True)
def draw(hud=False):
    app.controls(0);app.apply_pose();app.renderer.render(app.scene,app.camera)
    if hud:app.hud.draw(app.sim,True,appearance=app.appearance)
    return np.frombuffer(GL.glReadPixels(0,0,*app.size,GL.GL_RGB,GL.GL_UNSIGNED_BYTE),dtype=np.uint8).copy()

def press(key):app.handle_event(pygame.event.Event(pygame.KEYDOWN,key=key))
def difference(a,b):return int(np.count_nonzero(np.max(np.abs(a.astype(int)-b.astype(int)).reshape(-1,3),axis=1)>3))

try:
    app.sim.update(6);app.sim.paused=True;pose=app.sim.pose()
    base=draw()
    press(pygame.K_F3);plain=draw()
    color_diff=difference(base,plain);assert color_diff>200,color_diff
    press(pygame.K_F3);assert app.appearance.gradients
    press(pygame.K_F1);assert app.appearance.panel
    press(pygame.K_F4);grid=draw()
    uv_diff=difference(base,grid);assert uv_diff>1000,uv_diff
    draw(True);app.capture(out/'08_laboratorio_uv.png')
    shadow_ref=app.renderer.shadow_object.render_target.texture.texture_ref
    GL.glBindTexture(GL.GL_TEXTURE_2D,shadow_ref)
    shadow_filter=GL.glGetTexParameteriv(GL.GL_TEXTURE_2D,GL.GL_TEXTURE_MIN_FILTER)
    press(pygame.K_F5);nearest=draw();assert app.appearance.filter_mode==0
    filter_diff=difference(grid,nearest);assert filter_diff>200,filter_diff
    press(pygame.K_F5);linear=draw();assert app.appearance.filter_mode==1
    assert difference(nearest,linear)>200
    press(pygame.K_F5);assert app.appearance.filter_mode==2
    GL.glBindTexture(GL.GL_TEXTURE_2D,shadow_ref)
    assert GL.glGetTexParameteriv(GL.GL_TEXTURE_2D,GL.GL_TEXTURE_MIN_FILTER)==shadow_filter
    press(pygame.K_F4);assert not app.appearance.uv_debug
    restored=draw();assert difference(base,restored)==0
    press(pygame.K_F8);wire=draw()
    wire_diff=difference(base,wire);assert wire_diff>1000
    draw(True);app.capture(out/'11_malha_triangulos.png')
    press(pygame.K_F8);assert not app.appearance.wireframe
    press(pygame.K_F6);focus=draw()
    focus_diff=difference(base,focus);assert focus_diff>1000
    draw(True);app.capture(out/'09_foco_visual.png')
    press(pygame.K_F7);gray=draw()
    changed=np.max(np.abs(gray.astype(int)-focus.astype(int)).reshape(-1,3),axis=1)>3
    pixels=gray.reshape(-1,3)[changed].astype(int)
    assert len(pixels)>1000 and np.max(pixels.max(axis=1)-pixels.min(axis=1))<=1
    draw(True);app.capture(out/'10_contraste_cinza.png')
    assert app.sim.pose()==pose

    # Experimento controlado: interpolação de atributos, sem textura ou sombra.
    app.renderer._shadows_enabled=False
    quad=RectangleGeometry(width=2,height=2)
    quad.attribute_dict['vertexColor'].data=[[(x+1)/2,(y+1)/2,.2] for x,y,z in quad.attribute_dict['vertexPosition'].data]
    quad.attribute_dict['vertexColor'].upload_data()
    material=PhongMaterial(number_of_light_sources=2,property_dict={'useVertexColors':True,'specularStrength':0})
    camera=Camera();camera.set_orthographic(-1,1,-1,1,.1,10)
    camera.set_position([0,0,2]);camera.look_at([0,0,0])
    def experiment(mat):
        scene=Scene();scene.add(AmbientLight([.5,.5,.5]));scene.add(AmbientLight([.5,.5,.5]));scene.add(Mesh(quad,mat))
        app.renderer.render(scene,camera)
    def pixel(u,v):
        return np.frombuffer(GL.glReadPixels(int(app.size[0]*u),int(app.size[1]*v),1,1,GL.GL_RGB,GL.GL_UNSIGNED_BYTE),dtype=np.uint8).astype(int)
    experiment(material)
    samples=[]
    for u,v in ((.25,.25),(.5,.5),(.75,.75)):
        actual=pixel(u,v);expected=np.array([u,v,.2])*255
        assert np.max(abs(actual-expected))<2,(actual,expected)
        samples.append(actual.tolist())
    # UV de origem inferior esquerda, GL_REPEAT e offset, usando textura 2x2.
    texture=Texture(property_dict={'magFilter':GL.GL_NEAREST,'minFilter':GL.GL_NEAREST})
    texture.surface=pygame.Surface((2,2))
    for xy,color in (((0,0),(255,0,0)),((1,0),(0,255,0)),((0,1),(0,0,255)),((1,1),(255,255,0))):
        texture.surface.set_at(xy,color)
    texture.upload_data()
    textured=PhongMaterial(texture=texture,number_of_light_sources=2,property_dict={'specularStrength':0})
    experiment(textured)
    for u,v,color in ((.25,.25,(0,0,255)),(.75,.25,(255,255,0)),(.25,.75,(255,0,0)),(.75,.75,(0,255,0))):
        assert np.max(abs(pixel(u,v)-np.array(color)))<=1
    textured.uniform_dict['repeatUV'].data=[2,2];experiment(textured)
    assert np.array_equal(pixel(.125,.125),pixel(.625,.125))
    textured.uniform_dict['repeatUV'].data=[1,1]
    textured.uniform_dict['offsetUV'].data=[.5,0];experiment(textured)
    assert np.max(abs(pixel(.25,.25)-np.array([255,255,0])))<=1
    assert GL.glGetError()==GL.GL_NO_ERROR
    report={'vertex_color_pixels_changed':color_diff,'uv_grid_pixels_changed':uv_diff,
        'filter_pixels_changed':filter_diff,'focus_pixels_changed':focus_diff,
        'wireframe_pixels_changed':wire_diff,
        'interpolation_rgb_samples':samples,'uv_origin_repeat_offset':'PASS',
        'grayscale':'PASS','shadow_filter_preserved':'PASS','animation_unchanged':'PASS','gl_error':0}
    (out/'validacao_aulas.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(report)
finally:pygame.quit()
