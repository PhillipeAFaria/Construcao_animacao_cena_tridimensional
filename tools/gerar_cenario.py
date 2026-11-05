"""Gera a placa original da estação de pesquisa, sem imagem externa."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]
image=Image.new('RGB',(1024,160),(21,48,50));draw=ImageDraw.Draw(image)
try:font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',49)
except OSError:font=ImageFont.load_default(size=49)
draw.rounded_rectangle((7,7,1016,152),radius=12,outline=(130,189,162),width=4)
draw.text((43,42),'ESTACAO  /  PESQUISA  28',font=font,fill=(229,233,201))
image.save(root/'assets/estacao.png')
