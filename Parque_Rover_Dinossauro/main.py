"""Parque de reconhecimento: Python/Pygame/OpenGL + framework Stemkoski/Pascale."""
import argparse
import json
import math
from pathlib import Path
import pygame
import OpenGL.GL as GL
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.texture import Texture
from py3d.geometry.rectangle import RectangleGeometry
from py3d.light.ambient import AmbientLight
from py3d.light.directional import DirectionalLight
from py3d.material.phong import PhongMaterial
from models import Models, transform
from simulation import Simulation

ROOT=Path(__file__).resolve().parent
LABELS=('01 / APROXIMACAO', '02 / RECONHECIMENTO', '03 / RESPOSTA',
        '04 / ACOMPANHAMENTO', '05 / MISSAO CONCLUIDA')
DESCRIPTIONS=('Rover avanca ate a distancia de reconhecimento.',
 'Sensor inspeciona o dinossauro; rover aguarda.',
 'Dinossauro responde a chegada e muda de direcao.',
 'Virada concluida: rover acompanha a distancia constante.',
 'Encontro finalizado. Pressione R para repetir.')

class Application:
    def __init__(self, args):
        self.args=args
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION,3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION,3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE,24)
        self.size=(1200,760)
        pygame.display.set_mode(self.size,pygame.OPENGL|pygame.DOUBLEBUF)
        pygame.display.set_caption('PARQUE / Rover + Dinossauro | Espaco: pausa | H: ajuda')
        self.renderer=Renderer([.075,.13,.17])
        self.scene=Scene()
        self.camera=Camera(angle_of_view=48, aspect_ratio=self.size[0]/self.size[1],far=100)
        self.sim=Simulation()
        self.models=Models()
        self.rover,self.wheels,self.sensor=self.models.rover(self.scene)
        self.dino,self.legs,self.tail=self.models.dinosaur(self.scene)
        self.scene.add(AmbientLight(color=[.35,.38,.40]))
        light=DirectionalLight(color=[.80,.76,.65],direction=[-6,-12,-7])
        light.set_position([6,12,7]); light.look_at([0,0,0]); self.scene.add(light)
        self.renderer.enable_shadows(light,strength=.58,resolution=(2048,2048))
        self.renderer.shadow_object.camera.set_orthographic(-14,14,-12,12,.1,40)
        self.renderer.shadow_object._bias=.0018
        self.environment()
        self.azimuth=-.65; self.elevation=.46; self.radius=17
        self.target=[-.6,1,0]
        self.show_help=True
        self.hud=HUD(self.size)
        self.clock=pygame.time.Clock()

    def environment(self):
        ground=RectangleGeometry(width=28,height=20)
        uv=ground.attribute_dict['vertexUV']
        uv.data=[[u*9,v*7] for u,v in uv.data]; uv.upload_data()
        material=PhongMaterial(texture=Texture(str(ROOT/'assets/terreno.png')),
            number_of_light_sources=2,use_shadow=True,
            property_dict={'specularStrength':.02,'baseColor':[.75,.83,.74]})
        floor=Mesh(ground,material); floor.rotate_x(-math.pi/2); self.scene.add(floor)
        # Pista de demonstração paralela ao eixo X e marcos de destino.
        self.models.part(self.scene,(-.8,.014,0),(18,.025,4.6),(.27,.35,.32))
        for z in (-2.18,2.18):
            self.models.part(self.scene,(-.8,.035,z),(18,.02,.065),(.86,.79,.44))
        for x in range(-9,9,2):
            self.models.part(self.scene,(x,.04,0),(.65,.02,.06),(.68,.75,.63))
        for x,z,s in ((-8,-5,1.1),(6,-5,.9),(9,4,1.4),(-10,4,.7),(2,-6,.6)):
            rock=self.models.part(self.scene,(x,s*.32,z),(s,s*.64,s*.8),(.40,.45,.39))
            rock.rotate_y(x*.3)
        for z in (-2.7,2.7):
            self.models.part(self.scene,(6,.55,z),(.15,1.1,.15),(.86,.79,.44))
            self.models.part(self.scene,(6,1.16,z),(.3,.12,.3),(.15,.65,.61))

    def apply_pose(self):
        p=self.sim.pose()
        transform(self.rover,(p.rover_x,0,-.75))
        transform(self.dino,(p.dino_x,0,.75),yaw=p.dino_yaw)
        transform(self.sensor,(.4,2.02,0),yaw=-p.sensor_yaw)
        for wheel in self.wheels:
            transform(wheel,wheel.local_position,roll=p.wheel_angle)
        for i,leg in enumerate(self.legs):
            transform(leg,leg.local_position,pitch=p.leg_angle*(1 if i else -1))
        transform(self.tail,(0,1.30,-.72),yaw=p.tail_angle)

    def controls(self,dt):
        keys=pygame.key.get_pressed()
        self.azimuth+=(keys[pygame.K_RIGHT]-keys[pygame.K_LEFT])*dt
        self.elevation=max(.12,min(1.35,self.elevation+(keys[pygame.K_UP]-keys[pygame.K_DOWN])*dt))
        self.radius=max(5,min(32,self.radius+(keys[pygame.K_s]-keys[pygame.K_w])*7*dt))
        self.target[0]+=(keys[pygame.K_d]-keys[pygame.K_a])*4*dt
        self.target[1]=max(.4,min(6,self.target[1]+(keys[pygame.K_e]-keys[pygame.K_q])*3*dt))
        r=self.radius; a=self.azimuth; e=self.elevation
        self.camera.set_position([self.target[0]+r*math.cos(e)*math.sin(a),
            self.target[1]+r*math.sin(e), self.target[2]+r*math.cos(e)*math.cos(a)])
        self.camera.look_at(self.target)

    def run(self):
        running=True; frame=0
        captures={0:'01_aproximacao',360:'02_sensor',480:'03_resposta',720:'04_acompanhamento',990:'05_final'}
        out=ROOT/'evidencias'; out.mkdir(exist_ok=True)
        while running:
            real_dt=self.clock.tick(60)/1000
            dt=1/60 if self.args.validate else real_dt
            for event in pygame.event.get():
                if event.type==pygame.QUIT: running=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE: running=False
                    elif event.key==pygame.K_SPACE: self.sim.paused=not self.sim.paused
                    elif event.key==pygame.K_r: self.sim.reset()
                    elif event.key==pygame.K_h: self.show_help=not self.show_help
                    elif event.key==pygame.K_HOME:
                        self.azimuth=-.65; self.elevation=.46; self.radius=17; self.target=[-.6,1,0]
                    elif event.key==pygame.K_F12: self.capture(out/'captura.png')
            self.sim.update(dt)
            self.controls(real_dt)
            self.apply_pose()
            self.renderer.render(self.scene,self.camera)
            self.hud.draw(self.sim,self.show_help)
            if self.args.validate and frame in captures:
                self.capture(out/(captures[frame]+'.png'))
            error=GL.glGetError()
            if error!=GL.GL_NO_ERROR: raise RuntimeError(f'Erro OpenGL: {error}')
            pygame.display.flip()
            frame+=1
            if self.args.validate and frame>=1000:
                report={'frames':frame,'estado_final':self.sim.name,
                    'opengl':GL.glGetString(GL.GL_VERSION).decode(),
                    'gpu':GL.glGetString(GL.GL_RENDERER).decode(),
                    'gl_error':int(error),'shadow_resolution':2048}
                (out/'validacao_gpu.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
                print(json.dumps(report)); running=False
        pygame.quit()

    def capture(self,path):
        pixels=GL.glReadPixels(0,0,*self.size,GL.GL_RGB,GL.GL_UNSIGNED_BYTE)
        image=pygame.image.fromstring(pixels,self.size,'RGB',True)
        pygame.image.save(image,str(path))

class HUD:
    """Painel 2D em textura; não participa da passagem de sombras."""
    def __init__(self,size):
        from py3d.material.texture import TextureMaterial
        self.size=size
        self.renderer=Renderer()
        self.scene=Scene(); self.camera=Camera()
        self.camera.set_orthographic(0,size[0],0,size[1],-1,1)
        self.texture=Texture()
        self.texture.surface=pygame.Surface(size,pygame.SRCALPHA); self.texture.upload_data()
        self.mesh=Mesh(RectangleGeometry(width=size[0],height=size[1]),TextureMaterial(self.texture))
        self.mesh.set_position([size[0]/2,size[1]/2,0]); self.scene.add(self.mesh)
        self.title=pygame.font.SysFont('segoeui',25,bold=True)
        self.font=pygame.font.SysFont('segoeui',17)
        self.last=None

    def draw(self,sim,help_on):
        key=(sim.stage,sim.paused,help_on)
        if key!=self.last:
            surface=self.texture.surface; surface.fill((0,0,0,0))
            pygame.draw.rect(surface,(12,26,32,240),(22,22,590,113),border_radius=12)
            pygame.draw.rect(surface,(67,206,179,255),(22,22,5,113))
            surface.blit(self.font.render('PARQUE DE RECONHECIMENTO / ROVER + DINOSSAURO',True,(107,215,189)),(40,34))
            surface.blit(self.title.render(LABELS[sim.stage]+(' / PAUSADO' if sim.paused else ''),True,(240,242,228)),(40,60))
            surface.blit(self.font.render(DESCRIPTIONS[sim.stage],True,(195,209,206)),(40,100))
            if help_on:
                pygame.draw.rect(surface,(12,26,32,235),(22,self.size[1]-88,850,65),border_radius=10)
                for i,line in enumerate(('ESPACO pausa/retoma  |  R reinicia  |  H ajuda  |  ESC sai',
                    'SETAS orbita  |  W/S aproxima  |  A/D desloca  |  Q/E altura  |  HOME restaura  |  F12 captura')):
                    surface.blit(self.font.render(line,True,(220,231,223)),(39,self.size[1]-78+i*25))
            self.texture.upload_data(); self.last=key
        GL.glDisable(GL.GL_DEPTH_TEST)
        self.renderer.render(self.scene,self.camera,clear_color=False,clear_depth=False)
        GL.glEnable(GL.GL_DEPTH_TEST)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validate',action='store_true',help='Executa 1000 quadros com passo fixo e salva evidencias')
    Application(parser.parse_args()).run()
