from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parents[1]
image=Image.new('RGB',(1024,352),(20,44,47)); d=ImageDraw.Draw(image)
try:
    title=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',80)
    small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',32)
except OSError:
    title=ImageFont.load_default(size=80); small=ImageFont.load_default(size=32)
d.rounded_rectangle((8,8,1015,343),radius=24,outline=(99,203,168),width=4)
d.text((54,33),'ORBITA / CAMPO 28',font=small,fill=(111,214,178))
d.text((47,94),'PARQUE JURASSICO',font=title,fill=(237,239,213))
d.line((54,222,968,222),fill=(99,203,168),width=3)
d.text((54,258),'RECONHECER  >  RESPONDER  >  ACOMPANHAR',font=small,fill=(174,201,188))
image.save(root/'assets/placa.png')
