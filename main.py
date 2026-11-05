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
        pygame.display.set_caption('ORBITA / Parque Jurassico 1.1 | Espaco: pausa | H: ajuda')
        self.renderer=Renderer([.11,.18,.22])
        self.scene=Scene()
        self.camera=Camera(angle_of_view=48, aspect_ratio=self.size[0]/self.size[1],far=100)
        self.sim=Simulation()
        self.models=Models()
        self.rover,self.wheels,self.sensor=self.models.rover(self.scene)
        self.dino,self.legs,self.tail=self.models.dinosaur(self.scene)
        self.scene.add(AmbientLight(color=[.40,.43,.44]))
        light=DirectionalLight(color=[.85,.80,.68],direction=[-6,-12,-7])
        light.set_position([6,12,7]); light.look_at([0,0,0]); self.scene.add(light)
        self.renderer.enable_shadows(light,strength=.58,resolution=(2048,2048))
        self.renderer.shadow_object.camera.set_orthographic(-14,14,-12,12,.1,40)
        self.renderer.shadow_object._bias=.0018
        self.environment()
        self.azimuth=-.65; self.elevation=.46; self.radius=17
        self.target=[-.6,1,0]
        self.camera_mode='LIVRE'
        self.speed=1.0
        self.loop=False
        self.shadows=True
        self.pending_capture=False
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
        self.models.part(self.scene,(0,-.32,0),(28,.60,20),(.20,.29,.28))
        self.models.part(self.scene,(0,-.065,0),(28,.12,20),(.38,.48,.33))
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
        # Vegetação feita com a mesma geometria de caixas/cilindros dos modelos.
        for x,z,s in ((-10,-6,1.1),(-5,-7,1.3),(1,-7,1.1),(8,-6,1.2),
                      (-11,5,.85),(10,6,1.05),(5,7,.9)):
            self.models.part(self.scene,(x,.65*s,z),(.25*s,1.3*s,.25*s),(.37,.29,.19))
            for y,w,color in ((1.5,1.3,(.24,.43,.31)),(2.05,1.05,(.32,.53,.36)),(2.5,.65,(.43,.62,.38))):
                foliage=self.models.part(self.scene,(x,y*s,z),(w*s,.65*s,w*s),color)
                foliage.rotate_y(.25*x)
        for x in range(-10,11,2):
            self.models.part(self.scene,(x,.45,-4.2),(.10,.90,.10),(.54,.63,.52))
        for y in (.32,.72):
            self.models.part(self.scene,(0,y,-4.2),(20,.065,.065),(.64,.72,.60))
        for x in (-5.8,-3.2):
            self.models.part(self.scene,(x,1.0,-4.8),(.13,2.0,.13),(.20,.31,.31))
        self.models.part(self.scene,(-4.5,2.05,-4.82),(3.5,1.30,.15),(.12,.22,.24))
        sign_material=PhongMaterial(texture=Texture(str(ROOT/'assets/placa.png')),
            number_of_light_sources=2,use_shadow=True,property_dict={'specularStrength':.02})
        sign=Mesh(RectangleGeometry(width=3.3,height=1.12),sign_material)
        sign.set_position([-4.5,2.05,-4.73]); self.scene.add(sign)
        for x in (-7,5.6):
            for i in range(20):
                a=i*2*math.pi/20
                mark=self.models.part(self.scene,(x+.85*math.cos(a),.045,.85*math.sin(a)),(.18,.025,.055),(.74,.79,.48))
                mark.rotate_y(-a-math.pi/2)
        self.scan_ring=[]
        for i in range(24):
            a=i*2*math.pi/24
            mark=self.models.part(self.scene,(0,.07,0),(.18,.035,.055),(.24,.92,.82))
            mark.cast_shadow=False
            self.scan_ring.append((mark,a))

    def apply_pose(self):
        p=self.sim.pose()
        transform(self.rover,(p.rover_x,0,-.75))
        transform(self.dino,(p.dino_x,p.body_bob,.75),yaw=p.dino_yaw)
        transform(self.sensor,(.4,2.02,0),yaw=-p.sensor_yaw)
        for wheel in self.wheels:
            transform(wheel,wheel.local_position,roll=p.wheel_angle)
        for i,leg in enumerate(self.legs):
            transform(leg,leg.local_position,pitch=p.leg_angle*(1 if i else -1))
        transform(self.tail,(0,1.30,-.72),yaw=p.tail_angle)
        transform(self.models.head,(0,2.15,.51),yaw=p.head_yaw)
        transform(self.models.jaw,(0,.09,.40),pitch=p.jaw_angle)
        for mesh,angle in self.scan_ring:
            mesh.visible=self.sim.stage in (1,2)
            a=angle+self.sim.time*.7
            radius=1.45+.08*math.sin(self.sim.time*5)
            transform(mesh,(p.dino_x+radius*math.cos(a),.065,.75+radius*math.sin(a)),yaw=-a,scale=(.18,.035,.055))

    def controls(self,dt):
        keys=pygame.key.get_pressed()
        if any(keys[k] for k in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN,
                                 pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d,pygame.K_q,pygame.K_e)):
            self.camera_mode='LIVRE'
        self.azimuth+=(keys[pygame.K_RIGHT]-keys[pygame.K_LEFT])*dt
        self.elevation=max(.12,min(1.35,self.elevation+(keys[pygame.K_UP]-keys[pygame.K_DOWN])*dt))
        self.radius=max(5,min(32,self.radius+(keys[pygame.K_s]-keys[pygame.K_w])*7*dt))
        self.target[0]+=(keys[pygame.K_d]-keys[pygame.K_a])*4*dt
        self.target[1]=max(.4,min(6,self.target[1]+(keys[pygame.K_e]-keys[pygame.K_q])*3*dt))
        if self.camera_mode=='ACOMPANHAR':
            # Alvo diretamente definido pela pose: sem atraso dependente de FPS.
            self.target=[(self.sim.rover_x+self.sim.dino_x)/2,1.15,0]
        r=self.radius; a=self.azimuth; e=self.elevation
        self.camera.set_position([self.target[0]+r*math.cos(e)*math.sin(a),
            self.target[1]+r*math.sin(e), self.target[2]+r*math.cos(e)*math.cos(a)])
        self.camera.look_at(self.target)

    def handle_event(self,event):
        """Processa comandos da interface; retorna False ao solicitar fechamento."""
        if event.type==pygame.QUIT: return False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE: return False
            elif event.key==pygame.K_SPACE: self.sim.paused=not self.sim.paused
            elif event.key==pygame.K_r: self.sim.reset()
            elif event.key==pygame.K_h: self.show_help=not self.show_help
            elif event.key==pygame.K_c:
                self.camera_mode='LIVRE' if self.camera_mode=='ACOMPANHAR' else 'ACOMPANHAR'
            elif event.key==pygame.K_l: self.loop=not self.loop
            elif event.key==pygame.K_LEFTBRACKET: self.speed=max(.25,self.speed/2)
            elif event.key==pygame.K_RIGHTBRACKET: self.speed=min(2.0,self.speed*2)
            elif event.key==pygame.K_F2:
                self.shadows=not self.shadows
                for mesh in self.scene.descendant_list:
                    if isinstance(mesh,Mesh) and 'useShadow' in mesh.material.uniform_dict:
                        mesh.material.uniform_dict['useShadow'].data=self.shadows
            elif event.key in (pygame.K_1,pygame.K_2,pygame.K_3):
                presets={pygame.K_1:(-.65,.46,17),pygame.K_2:(-1.3,.27,11),pygame.K_3:(-.4,1.1,18)}
                self.azimuth,self.elevation,self.radius=presets[event.key]
                self.camera_mode='ACOMPANHAR'
            elif event.key==pygame.K_HOME:
                self.azimuth=-.65; self.elevation=.46; self.radius=17; self.target=[-.6,1,0]; self.camera_mode='LIVRE'
            elif event.key==pygame.K_F12: self.pending_capture=True
        if event.type==pygame.MOUSEWHEEL:
            self.radius=max(5,min(32,self.radius-event.y))
        return True

    def run(self):
        running=True; frame=0
        captures={0:'01_aproximacao',360:'02_sensor',480:'03_resposta',720:'04_acompanhamento',990:'05_final'}
        out=ROOT/'evidencias'; out.mkdir(exist_ok=True)
        while running:
            real_dt=self.clock.tick(60)/1000
            dt=1/60 if self.args.validate else real_dt
            for event in pygame.event.get():
                if not self.handle_event(event): running=False
            if self.loop and self.sim.stage==4 and not self.sim.paused:
                self.sim.reset()
            self.sim.update(dt*self.speed)
            self.controls(real_dt)
            self.apply_pose()
            self.renderer.render(self.scene,self.camera)
            self.hud.draw(self.sim,self.show_help,self.speed,self.camera_mode,self.loop,self.shadows)
            if self.pending_capture:
                self.capture(out/'captura.png'); self.pending_capture=False
            if self.args.validate and frame in captures:
                self.capture(out/(captures[frame]+'.png'))
            error=GL.glGetError()
            if error!=GL.GL_NO_ERROR: raise RuntimeError(f'Erro OpenGL: {error}')
            pygame.display.flip()
            frame+=1
            if self.args.validate and frame>=1000:
                report={'versao':'1.1','frames':frame,'estado_final':self.sim.name,
                    'opengl':GL.glGetString(GL.GL_VERSION).decode(),
                    'gpu':GL.glGetString(GL.GL_RENDERER).decode(),
                    'gl_error':int(error),'shadow_resolution':2048}
                (out/'validacao_gpu.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
                print(json.dumps(report)); running=False
        pygame.quit()

    def capture(self,path):
        path=Path(path)
        path.parent.mkdir(parents=True,exist_ok=True)
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

    def draw(self,sim,help_on,speed=1.0,camera='LIVRE',loop=False,shadows=True):
        key=(sim.stage,sim.paused,help_on,int(sim.time*10),speed,camera,loop,shadows)
        if key!=self.last:
            surface=self.texture.surface; surface.fill((0,0,0,0))
            ink=(229,238,223); muted=(170,196,188); mint=(90,218,182)
            pygame.draw.rect(surface,(12,29,34,238),(22,22,565,140),border_radius=14)
            pygame.draw.rect(surface,(*mint,255),(22,42,4,96),border_radius=2)
            surface.blit(self.font.render('ORBITA  /  PARQUE JURASSICO',True,mint),(42,34))
            surface.blit(self.title.render('Encontro no parque',True,ink),(42,58))
            surface.blit(self.font.render(LABELS[sim.stage],True,mint),(42,95))
            surface.blit(self.font.render(DESCRIPTIONS[sim.stage],True,muted),(42,125))
            pygame.draw.rect(surface,(12,29,34,238),(936,22,242,140),border_radius=14)
            status='PAUSADO' if sim.paused else ('CONCLUIDO' if sim.stage==4 else 'EM ANDAMENTO')
            surface.blit(self.font.render(status,True,(244,202,112) if sim.paused else mint),(954,36))
            for i,line in enumerate((f'Tempo {sim.time:04.1f}s / 16s   |   {speed:g}x',
                                     'Camera: '+camera.lower(),
                                     'Repetir: '+('sim' if loop else 'nao')+'  |  Sombras: '+('sim' if shadows else 'nao'))):
                surface.blit(self.font.render(line,True,muted),(954,66+i*26))
            # Linha do tempo reflete o tempo da simulação e fica imóvel na pausa.
            panel_y=603 if help_on else 656
            pygame.draw.rect(surface,(12,29,34,238),(22,panel_y,1156,79),border_radius=12)
            pygame.draw.line(surface,(65,85,80),(65,panel_y+24),(1090,panel_y+24),3)
            progress=min(1,sim.time/16)
            pygame.draw.line(surface,mint,(65,panel_y+24),(65+int(1025*progress),panel_y+24),3)
            stages=('Aproximar','Reconhecer','Responder','Acompanhar','Concluir')
            for i,text in enumerate(stages):
                x=65+int((0,5,7,9,16)[i]*1025/16)
                color=mint if i<=sim.stage else (89,115,106)
                pygame.draw.circle(surface,color,(x,panel_y+24),7)
                label=self.font.render(text,True,ink if i==sim.stage else muted)
                surface.blit(label,(x-label.get_width()/2,panel_y+43))
            if help_on:
                for i,line in enumerate(('ESPACO pausa  /  R reinicia  /  1-2-3 cameras  /  C acompanha  /  [ ] velocidade  /  L repete',
                    'SETAS orbita  /  W-S zoom  /  A-D desloca  /  Q-E altura  /  F2 sombras  /  F12 captura  /  H ajuda  /  ESC sai')):
                    surface.blit(self.font.render(line,True,ink),(38,695+i*26))
            self.texture.upload_data(); self.last=key
        GL.glDisable(GL.GL_DEPTH_TEST)
        self.renderer.render(self.scene,self.camera,clear_color=False,clear_depth=False)
        GL.glEnable(GL.GL_DEPTH_TEST)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validate',action='store_true',help='Executa 1000 quadros com passo fixo e salva evidencias')
    Application(parser.parse_args()).run()
