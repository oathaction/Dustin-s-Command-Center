"""Construction view for option B: outline, centreline, nodes, and the Lora master behind it."""
import sys, json, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p1 as o, p1_amp_b as B
B.export()
s=(B.DIR/"20261021_Amp-B-Drawn-Master.svg").read_text()
d=re.search(r' d="([^"]+)"',s).group(1)
vb=o.viewbox(s)
cons=json.loads((B.DIR/"construction.json").read_text())
lora=o.d_from_path(o.amp_glyph(0,100,0.14))
sc=7
W,H=int((vb[2]+20)*sc),int((vb[3]+20)*sc)
off=cons["offset_x_units"]
nodes=re.findall(r'[MLCZ]([^MLCZ]*)', d)
pts=[]
for verb,ps in o.path_from_d(d).segments:
    if ps: pts.append(ps[-1])
dots="".join(f'<circle cx="{x}" cy="{y}" r="0.5" fill="#121212"/>' for x,y in pts)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-10} {vb[1]-10} {vb[2]+20} {vb[3]+20}" width="{W}" height="{H}" style="left:0;top:0">
<line x1="-10" y1="0" x2="{vb[2]+10}" y2="0" stroke="#4A7C74" stroke-width="0.2"/><line x1="-10" y1="100" x2="{vb[2]+10}" y2="100" stroke="#4A7C74" stroke-width="0.2"/>
<path d="{lora}" fill="none" stroke="#1F2D5A" stroke-width="0.35" stroke-dasharray="1 1" transform="translate({-off*0+0} 0)"/>
<path d="{d}" fill="#E63946" fill-opacity="0.55" stroke="#121212" stroke-width="0.25"/>
<path d="{cons['centreline_font_units_y_up']}" fill="none" stroke="#121212" stroke-width="0.3" transform="matrix({1/7} 0 0 {-1/7} {-off} 100)"/>
{dots}</svg>'''
o.render([{"id":"bdebug","w":W,"h":H,"bg":"#FFFFFF","html":svg}], o.SCRATCH/"peek", "bdebug")
print(o.SCRATCH/"peek/bdebug.png")
