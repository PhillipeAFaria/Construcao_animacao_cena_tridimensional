"""Gera o PNG original usado no terreno. Executar a partir de qualquer pasta."""
from pathlib import Path
import random
from PIL import Image, ImageDraw

target=Path(__file__).resolve().parents[1]/'assets/terreno.png'
image=Image.new('RGB',(256,256),(127,143,104))
draw=ImageDraw.Draw(image); rng=random.Random(28)
for _ in range(12000):
    x,y=rng.randrange(256),rng.randrange(256); v=rng.randrange(-13,14)
    draw.point((x,y),fill=(127+v,143+v,104+v))
for x in range(0,256,64):
    draw.line((x,0,x,255),fill=(105,123,87),width=2)
    draw.line((0,x,255,x),fill=(105,123,87),width=2)
image.save(target)
print(target)
