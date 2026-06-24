# -*- coding: utf-8 -*-
"""Флэт-иллюстрации для презентации скейт-парка. Рендер SVG -> PNG (cairosvg).
ВАЖНО: градиент на тонких вертикальных/горизонтальных штрихах не рисуется
(нулевой bbox), поэтому все обводки — солидным цветом."""
import cairosvg, os, math
os.makedirs("img", exist_ok=True)

BG1="#0A0E1A"; BG2="#16213E"; CARD="#1B2745"; CARD2="#141D33"
ACC="#FF5722"; ACC2="#FF7A45"; GOLD="#FFC107"; GOLD2="#FFD54F"
CY="#22D3EE"; GR="#34D399"; WHITE="#EAF0FA"; DIM="#5B6B8A"; DARK="#0A0E1A"

def render(name, w, h, body, defs=""):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
<linearGradient id="orange" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="{ACC2}"/><stop offset="1" stop-color="{ACC}"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="{GOLD2}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
 <stop offset="0" stop-color="{ACC}" stop-opacity="0.20"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></radialGradient>
{defs}
</defs>
<rect width="{w}" height="{h}" fill="url(#sky)"/>
{body}
</svg>'''
    cairosvg.svg2png(bytestring=svg.encode(), write_to=f"img/{name}.png",
                     output_width=w*2, output_height=h*2)
    print("ok", name)

def stars(w, y0=40, n=18):
    out=[]
    for i in range(n):
        x=(i*97+40)%(w-40)+20; yy=(i*53+25)%(y0+140)
        r=1.2+(i%3)*0.7
        out.append(f'<circle cx="{x}" cy="{yy}" r="{r}" fill="{WHITE}" opacity="0.3"/>')
    return "".join(out)

def glow(cx,cy,rx,ry):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#glow)"/>'

def ground(w,h,y,col=CARD2):
    return (f'<rect x="0" y="{y}" width="{w}" height="{h-y}" fill="{col}"/>'
            f'<rect x="0" y="{y}" width="{w}" height="5" fill="{ACC}" opacity="0.55"/>')

def shadow(cx,cy,rx):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.18}" fill="{DARK}" opacity="0.45"/>'

# ---------- снаряды ----------
def skateboard(cx, cy, s=1.0, rot=-10, col="url(#orange)"):
    return f'''<g transform="translate({cx},{cy}) scale({s}) rotate({rot})">
 <rect x="-100" y="-9" width="200" height="20" rx="10" fill="{col}"/>
 <path d="M-100 1 q-22 0 -22 -16 M100 1 q22 0 22 -16" fill="none" stroke="{ACC}" stroke-width="6"/>
 <rect x="-72" y="11" width="10" height="14" rx="2" fill="{DIM}"/>
 <rect x="62" y="11" width="10" height="14" rx="2" fill="{DIM}"/>
 <circle cx="-67" cy="28" r="13" fill="{GOLD}"/><circle cx="67" cy="28" r="13" fill="{GOLD}"/>
 <circle cx="-67" cy="28" r="5" fill="{DARK}"/><circle cx="67" cy="28" r="5" fill="{DARK}"/>
</g>'''

def scooter(cx, cy, s=1.0):
    # cy — уровень земли (колёса). Высота композиции вверх ~ 200*s.
    return f'''<g transform="translate({cx},{cy}) scale({s})">
 <rect x="-15" y="-14" width="150" height="16" rx="8" fill="{ACC}"/>
 <rect x="115" y="-150" width="16" height="150" rx="8" fill="{ACC}"/>
 <rect x="80" y="-160" width="90" height="16" rx="8" fill="{GOLD}"/>
 <circle cx="-15" cy="14" r="26" fill="{CARD}" stroke="{WHITE}" stroke-width="8"/>
 <circle cx="135" cy="14" r="26" fill="{CARD}" stroke="{WHITE}" stroke-width="8"/>
 <circle cx="-15" cy="14" r="7" fill="{GOLD}"/><circle cx="135" cy="14" r="7" fill="{GOLD}"/>
</g>'''

def bmx(cx, cy, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
 <circle cx="-78" cy="0" r="58" fill="none" stroke="{WHITE}" stroke-width="11"/>
 <circle cx="78" cy="0" r="58" fill="none" stroke="{WHITE}" stroke-width="11"/>
 <circle cx="-78" cy="0" r="10" fill="{GOLD}"/><circle cx="78" cy="0" r="10" fill="{GOLD}"/>
 <path d="M-78 0 L8 0 M-78 0 L-6 -54 M8 0 L-6 -54 M8 0 L44 -56" fill="none" stroke="{ACC}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
 <path d="M44 -56 L78 -56" stroke="{GOLD}" stroke-width="11" stroke-linecap="round"/>
 <path d="M78 0 L44 -56" stroke="{ACC}" stroke-width="11" stroke-linecap="round"/>
 <rect x="-26" y="-64" width="40" height="11" rx="5" fill="{GOLD}"/>
 <path d="M-6 -54 L-6 -38" stroke="{DARK}" stroke-width="9"/>
</g>'''

def rider(cx, cy, s=1.0, col=WHITE):
    """Силуэт на доске: ноги расставлены, корпус наклонён, руки для баланса."""
    return f'''<g transform="translate({cx},{cy}) scale({s})" fill="{col}">
 <circle cx="6" cy="-96" r="19"/>
 <path d="M-8 -78 Q8 -70 22 -80 L26 -34 Q4 -26 -16 -34 Z"/>
 <path d="M-6 -72 L-44 -58 L-40 -46 L-2 -56 Z"/>
 <path d="M20 -72 L52 -86 L58 -74 L26 -58 Z"/>
 <path d="M-12 -36 L-40 -4 L-28 4 L-2 -24 Z"/>
 <path d="M16 -36 L44 -6 L34 4 L4 -24 Z"/>
 <ellipse cx="-40" cy="2" rx="13" ry="7"/><ellipse cx="40" cy="2" rx="13" ry="7"/>
</g>'''

def standfig(cx, cy, s=1.0, col=WHITE):
    """Спокойный стоящий силуэт."""
    return f'''<g transform="translate({cx},{cy}) scale({s})" fill="{col}">
 <circle cx="0" cy="-118" r="19"/>
 <path d="M-16 -98 Q0 -90 16 -98 L20 -34 L-20 -34 Z"/>
 <path d="M-16 -92 L-34 -52 L-24 -48 L-6 -84 Z"/>
 <path d="M16 -92 L34 -52 L24 -48 L6 -84 Z"/>
 <rect x="-18" y="-36" width="14" height="40" rx="6"/>
 <rect x="4" y="-36" width="14" height="40" rx="6"/>
</g>'''

def helmet(cx, cy, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
 <path d="M-72 12 A72 70 0 0 1 72 12 L72 26 L-72 26 Z" fill="url(#orange)"/>
 <path d="M-72 12 A72 70 0 0 1 72 12" fill="none" stroke="{GOLD}" stroke-width="5" opacity="0.7"/>
 <rect x="-74" y="22" width="42" height="13" rx="6" fill="{GOLD}"/>
 <circle cx="-30" cy="-12" r="5" fill="{WHITE}" opacity="0.5"/>
</g>'''

def pad(cx, cy, s=1.0, col=GR):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
 <rect x="-32" y="-38" width="64" height="76" rx="22" fill="{col}"/>
 <rect x="-32" y="-12" width="64" height="8" fill="{DARK}" opacity="0.2"/>
 <rect x="-32" y="6" width="64" height="8" fill="{DARK}" opacity="0.2"/>
 <ellipse cx="0" cy="0" rx="15" ry="20" fill="{DARK}" opacity="0.18"/>
</g>'''

def coachfig(cx, cy, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
 <circle cx="0" cy="-152" r="32" fill="{WHITE}"/>
 <path d="M-28 -134 Q0 -124 28 -134 L46 -8 L-46 -8 Z" fill="url(#orange)"/>
 <rect x="-46" y="-44" width="92" height="13" fill="{GOLD}"/>
 <rect x="-18" y="-8" width="14" height="8" fill="{DARK}" opacity="0.3"/>
 <path d="M28 -126 L84 -92" stroke="{WHITE}" stroke-width="14" stroke-linecap="round"/>
 <circle cx="92" cy="-86" r="15" fill="{GOLD}"/><circle cx="92" cy="-86" r="6" fill="{DARK}"/>
 <path d="M-28 -126 L-72 -78" stroke="{WHITE}" stroke-width="14" stroke-linecap="round"/>
 <rect x="-94" y="-80" width="34" height="44" rx="4" fill="{CY}"/>
 <rect x="-88" y="-72" width="22" height="4" fill="{DARK}"/><rect x="-88" y="-62" width="22" height="4" fill="{DARK}"/><rect x="-88" y="-52" width="14" height="4" fill="{DARK}"/>
</g>'''

def shop(cx, cy, s=1.0):
    awn="".join(f'<rect x="{-96+i*38}" y="-34" width="20" height="42" fill="{GOLD if i%2 else WHITE}"/>' for i in range(5))
    return f'''<g transform="translate({cx},{cy}) scale({s})">
 <rect x="-104" y="8" width="208" height="128" rx="6" fill="{CARD}"/>
 <rect x="-104" y="-34" width="208" height="44" fill="{ACC}"/>
 {awn}
 <rect x="-78" y="44" width="62" height="92" fill="{BG1}"/>
 <rect x="18" y="44" width="64" height="56" rx="4" fill="{CY}" opacity="0.45"/>
 <rect x="-50" y="-72" width="100" height="30" rx="6" fill="{CARD}"/>
 <text x="0" y="-50" font-family="Arial" font-size="22" font-weight="bold" fill="{GOLD}" text-anchor="middle">SHOP</text>
</g>'''

def rubsign(col=DARK):
    # символ ₽ штрихами (стем + дуга + перекладина)
    return f'''<g fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round">
 <path d="M-7 -22 L-7 22"/>
 <path d="M-7 -22 L4 -22 a13 12 0 0 1 0 24 L-7 2"/>
 <path d="M-20 10 L12 10"/>
</g>'''

def coin(cx, cy, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
 <ellipse cx="0" cy="6" rx="42" ry="12" fill="{DARK}" opacity="0.3"/>
 <circle cx="0" cy="0" r="42" fill="url(#gold)" stroke="{ACC}" stroke-width="5"/>
 <circle cx="0" cy="0" r="32" fill="none" stroke="{ACC}" stroke-width="2" opacity="0.5"/>
 {rubsign()}
</g>'''

def bars(cx, cy, s=1.0):
    hs=[46,78,112,150]
    out=[f'<rect x="{i*50}" y="{-bh}" width="36" height="{bh}" rx="5" fill="url(#gold)"/>' for i,bh in enumerate(hs)]
    out.append(f'<path d="M6 -28 L168 -160" stroke="{GR}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="M140 -160 L172 -160 L172 -128" fill="none" stroke="{GR}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    return f'<g transform="translate({cx},{cy}) scale({s})">{"".join(out)}</g>'

def ramp(x, baseY, w, hgt, col=CARD):
    s = 1 if w>0 else -1
    return (f'<path d="M{x} {baseY} L{x} {baseY-hgt} Q{x} {baseY} {x+w} {baseY} Z" fill="{col}"/>'
            f'<path d="M{x} {baseY-hgt} Q{x} {baseY} {x+w} {baseY}" fill="none" stroke="{ACC}" stroke-width="6"/>'
            f'<line x1="{x+ (8*s)}" y1="{baseY-hgt+40}" x2="{x+(8*s)}" y2="{baseY-30}" stroke="{WHITE}" stroke-width="3" opacity="0.15"/>')

# ============== СЦЕНЫ ==============
W,H=1400,900

hero=f'''{stars(W)}{glow(700,470,440,200)}
{ground(W,H,700)}
{ramp(110,700,300,220)}{ramp(1290,700,-300,190)}
{shadow(720,690,70)}
{skateboard(722,430,1.25)}
{rider(720,360,1.5)}'''
render("hero",W,H,hero)

problem=f'''{stars(W)}{ground(W,H,700,col="#11192C")}
<g opacity="0.45">
 <rect x="120" y="380" width="120" height="320" rx="4" fill="{CARD}"/>
 <rect x="280" y="300" width="140" height="400" rx="4" fill="{BG2}"/>
 <rect x="980" y="340" width="130" height="360" rx="4" fill="{CARD}"/>
 <rect x="1150" y="420" width="120" height="280" rx="4" fill="{BG2}"/>
 <rect x="150" y="430" width="24" height="30" fill="{GOLD}" opacity="0.5"/>
 <rect x="200" y="430" width="24" height="30" fill="{GOLD}" opacity="0.5"/>
 <rect x="1180" y="470" width="24" height="30" fill="{GOLD}" opacity="0.5"/>
</g>
<rect x="500" y="694" width="400" height="12" fill="{GOLD}" opacity="0.5"/>
<rect x="560" y="697" width="34" height="6" fill="{DARK}"/><rect x="660" y="697" width="34" height="6" fill="{DARK}"/><rect x="760" y="697" width="34" height="6" fill="{DARK}"/>
{shadow(700,700,46)}{standfig(700,700,1.15,col=DIM)}
<g transform="translate(700,300)">
 <circle r="58" fill="{BG1}" stroke="{ACC}" stroke-width="11"/>
 <line x1="0" y1="-26" x2="0" y2="14" stroke="{ACC}" stroke-width="13" stroke-linecap="round"/>
 <circle cx="0" cy="34" r="8" fill="{ACC}"/></g>'''
render("problem",W,H,problem)

solution=f'''{stars(W)}{glow(700,500,500,210)}
{ground(W,H,700)}
{ramp(90,700,340,230)}{ramp(1310,700,-340,230)}
<rect x="560" y="612" width="280" height="88" rx="10" fill="{CARD}"/>
<rect x="560" y="604" width="280" height="12" rx="6" fill="{ACC}"/>
{shadow(700,604,90)}
{skateboard(700,566,1.0,rot=0)}'''
render("solution",W,H,solution)

CW,CH=600,470
render("c_bmx",CW,CH,f'{stars(CW,30,7)}{glow(300,260,210,140)}{shadow(300,330,150)}{bmx(300,250,1.4)}')
render("c_scooter",CW,CH,f'{stars(CW,30,7)}{glow(300,260,210,140)}{shadow(300,332,150)}{scooter(230,300,1.35)}')
render("c_skate",CW,CH,f'{stars(CW,30,7)}{glow(300,260,210,140)}{shadow(300,300,170)}{skateboard(300,250,1.7,rot=-8)}')

safety=f'''{stars(W)}{glow(700,400,430,210)}
{helmet(700,350,2.4)}
{shadow(700,470,140)}
{pad(430,560,1.45,col=GR)}{pad(970,560,1.45,col=CY)}
<text x="430" y="660" font-family="Arial" font-size="30" fill="{DIM}" text-anchor="middle">наколенник</text>
<text x="700" y="540" font-family="Arial" font-size="32" fill="{DIM}" text-anchor="middle">шлем</text>
<text x="970" y="660" font-family="Arial" font-size="30" fill="{DIM}" text-anchor="middle">налокотник</text>'''
render("safety",W,H,safety)

coach=f'''{stars(W)}{glow(640,470,440,220)}
{ground(W,H,720)}
{shadow(560,720,80)}{coachfig(560,720,1.6)}
{shadow(1010,710,70)}{skateboard(1010,700,0.85,rot=0)}{rider(1008,632,1.05)}
<path d="M720 470 Q880 470 970 560" stroke="{GOLD}" stroke-width="5" stroke-dasharray="9 10" fill="none"/>'''
render("coach",W,H,coach)

cols=[WHITE,GOLD,CY,GR,ACC2]
people="".join(shadow(360+i*170,662,46)+standfig(360+i*170,662,1.05+(i%3)*0.08,col=cols[i%5]) for i in range(5))
social=f'''{stars(W)}{glow(700,500,540,210)}
{ground(W,H,662)}
{people}'''
render("social",W,H,social)

budget=f'''{stars(W)}{glow(640,470,500,220)}
{ground(W,H,720)}
{shadow(380,724,110)}{shop(380,580,1.45)}
{bars(810,704,1.25)}
{coin(1190,360,1.5)}{coin(1268,506,1.0)}{coin(1112,520,0.78)}'''
render("budget",W,H,budget)

plus=f'''{stars(W)}{glow(700,420,460,230)}
<g transform="translate(700,360)">
 <circle r="150" fill="none" stroke="{GR}" stroke-width="20"/>
 <circle r="150" fill="{GR}" opacity="0.08"/>
 <path d="M-72 8 L-22 66 L78 -58" fill="none" stroke="{GR}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/></g>
{shadow(360,650,90)}{skateboard(360,640,0.8,rot=-8)}
{shadow(900,650,70)}{scooter(852,640,0.8)}
{shadow(1090,690,80)}{helmet(1090,660,1.25)}'''
render("plus",W,H,plus)

rays="".join(f'<line x1="700" y1="650" x2="{700+580*math.cos(math.radians(a))}" y2="{650+580*math.sin(math.radians(a))}" stroke="{GOLD}" stroke-width="6" opacity="0.22"/>' for a in range(188,357,13))
final=f'''{stars(W)}{rays}
<circle cx="700" cy="650" r="170" fill="url(#gold)"/>
<circle cx="700" cy="650" r="170" fill="{GOLD}" opacity="0.15"/>
{ground(W,H,650,col="#11192C")}
{shadow(700,648,80)}
{skateboard(700,566,1.1,rot=-6,col=DARK)}
{rider(700,496,1.35,col=DARK)}'''
render("final",W,H,final)

print("DONE")
