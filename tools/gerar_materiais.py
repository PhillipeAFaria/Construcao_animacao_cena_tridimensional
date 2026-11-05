"""Gera texturas originais; não reutiliza figuras dos PDFs nem imagens externas."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

OUT=Path(__file__).resolve().parents[1]/'assets'
OUT.mkdir(exist_ok=True)
rng=random.Random(20261104)

def noise(name,base,size=256,spread=10):
    image=Image.new('RGB',(size,size))
    image.putdata([tuple(max(0,min(255,c+(delta:=rng.randrange(-spread,spread+1)))) for c in base)
                   for _ in range(size*size)])
    image.save(OUT/name)
    return image

noise('terreno.png',(132,143,113))
noise('asfalto.png',(79,94,99),spread=9)
image=noise('escamas.png',(229,239,230),128,5)
d=ImageDraw.Draw(image)
for row in range(-1,10):
    for col in range(-1,10):
        x=col*16+(row%2)*8; y=row*16
        d.arc((x-8,y-8,x+8,y+8),0,180,fill=(187,207,193),width=1)
image.save(OUT/'escamas.png')
image=Image.new('RGB',(256,256),(28,44,57));d=ImageDraw.Draw(image)
for y in range(8,248,40):
    for x in range(8,248,60):
        d.rounded_rectangle((x,y,x+54,y+34),radius=4,fill=(29,76+(y//40)*2,108),outline=(83,135,155),width=1)
        for offset in (12,25,38):d.line((x+offset,y+3,x+offset,y+31),fill=(121,163,179))
d.rectangle((1,1,254,254),outline=(173,183,177),width=3)
image.save(OUT/'solar.png')
try: font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',18)
except OSError: font=ImageFont.load_default(size=18)
image=Image.new('RGB',(256,256));d=ImageDraw.Draw(image)
palette=((203,113,70),(57,134,150),(204,181,86),(101,153,117))
for j in range(4):
    for i in range(4):
        x=i*64;y=(3-j)*64
        d.rectangle((x,y,x+63,y+63),fill=palette[(i+j)%4],outline=(240,240,215),width=2)
        d.text((x+13,y+22),f'{chr(65+i)}{j+1}',font=font,fill=(15,27,34))
d.line((5,250,248,250),fill='white',width=3); d.line((5,250,5,7),fill='white',width=3)
d.polygon(((248,250),(237,244),(237,255)),fill='white')
d.polygon(((5,7),(0,18),(10,18)),fill='white')
d.text((220,226),'U',font=font,fill='white');d.text((12,8),'V',font=font,fill='white')
image.save(OUT/'grade_uv.png')
print('Materiais PNG gerados em',OUT)
