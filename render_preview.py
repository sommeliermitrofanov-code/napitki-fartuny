# -*- coding: utf-8 -*-
"""Превью слайдов через Pillow по тем же координатам, что и в build_pptx.py.
Служит для проверки вёрстки и как картинки для показа."""
from PIL import Image, ImageDraw, ImageFont
import os
os.makedirs("preview", exist_ok=True)
S=100  # px per inch
W,H=int(13.333*S),int(7.5*S)
def I(v): return int(v*S)
def PT(pt): return max(8,int(pt*S/72))

FB="/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR="/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FI="/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
FBI="/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"
def font(pt,b=False,it=False):
    f=FBI if (b and it) else FB if b else FI if it else FR
    return ImageFont.truetype(f,PT(pt))

BG=(0x0A,0x0E,0x1A); BG2=(0x0F,0x16,0x28); CARD=(0x14,0x1D,0x33); LINE=(0x24,0x31,0x50)
ACC=(0xFF,0x57,0x22); GOLD=(0xFF,0xC1,0x07); TXT=(0xEA,0xF0,0xFA); DIM=(0x8B,0x9A,0xB8)
WHITE=(0xFF,0xFF,0xFF); DARK=(0x0A,0x0E,0x1A)

def canvas(bg=BG):
    im=Image.new("RGB",(W,H),bg); return im,ImageDraw.Draw(im)

def rrect(d,x,y,w,h,r,fill=None,outline=None,ow=1):
    d.rounded_rectangle([I(x),I(y),I(x+w),I(y+h)],radius=I(r),fill=fill,outline=outline,width=ow)

def rect(d,x,y,w,h,fill):
    d.rectangle([I(x),I(y),I(x+w),I(y+h)],fill=fill)

def text(d,x,y,s,pt,col,b=False,it=False):
    d.text((I(x),I(y)),s,font=font(pt,b,it),fill=col)

def textc(d,cx,cy,s,pt,col,b=False):
    f=font(pt,b); bb=d.textbbox((0,0),s,font=f)
    d.text((I(cx)-(bb[2]-bb[0])//2,I(cy)-(bb[3]-bb[1])//2-bb[1]),s,font=f,fill=col)

def runs(d,x,y,parts,pt):
    """parts: list of (text,color,bold). Рисует в строку."""
    cx=I(x)
    for s,c,b in parts:
        f=font(pt,b); d.text((cx,I(y)),s,font=f,fill=c)
        cx+=d.textbbox((0,0),s,font=f)[2]

def wrap(d,s,pt,maxw,b=False):
    f=font(pt,b); words=s.split(); lines=[]; cur=""
    for w_ in words:
        t=(cur+" "+w_).strip()
        if d.textbbox((0,0),t,font=f)[2]<=I(maxw): cur=t
        else: lines.append(cur); cur=w_
    if cur: lines.append(cur)
    return lines

def paste(im,name,x,y,w,h,border=True):
    p=Image.open("img/%s.png"%name).convert("RGB").resize((I(w),I(h)))
    im.paste(p,(I(x),I(y)))
    if border:
        ImageDraw.Draw(im).rectangle([I(x),I(y),I(x+w)-1,I(y+h)-1],outline=LINE,width=2)

def paste_h(im,name,x,h_in,centered=True):
    src=Image.open("img/%s.png"%name).convert("RGB")
    ratio=src.width/src.height; w_in=h_in*ratio
    p=src.resize((I(w_in),I(h_in)))
    px=I((13.333-w_in)/2) if centered else I(x)
    im.paste(p,(px,0))

def kicker(d,t,x=0.85,y=0.62):
    rect(d,x,y+0.13,0.34,0.04,ACC)
    text(d,x+0.45,y-0.02,t.upper(),14,GOLD,b=True)

RX,RW=6.95,5.7; RH=5.7/(1400/900); RY=2.05

_md=ImageDraw.Draw(Image.new("RGB",(4,4)))
def tw_in(s,pt,b=False,it=False):  # ширина текста в дюймах
    return _md.textbbox((0,0),s,font=font(pt,b,it))[2]/S

def flow(d,x,top,tokens,pt,maxw,lh=0.3):
    """Поток токенов (text,color,bold) с переносом по словам в ширину maxw от x."""
    cx,cy=x,top
    for s,c,b in tokens:
        for word in s.split(" "):
            if word=="":
                cx+=tw_in(" ",pt,b); continue
            ww=tw_in(word+" ",pt,b)
            if cx+ww>x+maxw and cx>x:
                cx=x; cy+=lh
            text(d,cx,cy,word,pt,c,b=b); cx+=ww
    return cy

def bullets(d,top,items,x=0.95,w=5.7):
    y=top
    for b,desc in items:
        toks=[("●  ",ACC,True),(b+" ",WHITE,True),(desc,DIM,False)]
        endy=flow(d,x,y,toks,16,w,lh=0.31)
        y=endy+0.52

def title(d,top,lines,size=40):
    y=top
    for t,c in lines:
        for ln in wrap(d,t,size,6.0,b=True):
            text(d,0.85,y,ln,size,c,b=True); y+=size/72*1.18

slides=[]

# 1 ТИТУЛ
im,d=canvas()
paste_h(im,"hero",0,7.5); d=ImageDraw.Draw(im)
rect(d,0,0,0.22,7.5,ACC)
kicker(d,"Социальный проект · Южная Осетия")
text(d,0.85,1.35,"Скейт-парк",70,TXT,b=True)
runs(d,0.85,2.45,[("в ",TXT,True),("Цхинвале",GOLD,True)],70)
text(d,0.9,5.5,"Современное и безопасное пространство для досуга",19,DIM)
text(d,0.9,5.82,"и спорта детей и подростков города.",19,DIM)
rrect(d,0.9,6.55,4.5,0.6,0.14,fill=ACC)
textc(d,0.9+2.25,6.85,"BMX · Самокат · Скейтборд",18,DARK,b=True)
slides.append(im)

# 2 ПРОБЛЕМА
im,d=canvas()
kicker(d,"Проблема")
title(d,1.35,[("Детям и подросткам",TXT),("негде проводить время",TXT)])
bullets(d,3.4,[("Нет инфраструктуры.","В Цхинвале почти нет современных площадок для активного отдыха."),
 ("Опасно.","Дети катаются на улицах и парковках — риск для них и прохожих."),
 ("Энергия без выхода.","У подростков нет места для здорового досуга.")])
paste(im,"problem",RX,RY,RW,RH)
slides.append(im)

# 3 РЕШЕНИЕ
im,d=canvas()
kicker(d,"Решение")
title(d,1.35,[("Построить современный",TXT),("скейт-парк",GOLD)])
bullets(d,3.4,[("Качественное покрытие.","Рампы, фигуры и гладкое основание."),
 ("Зона отдыха.","Скамейки, освещение и озеленение."),
 ("Для всех уровней.","От первых шагов до сложных трюков.")])
paste(im,"solution",RX,RY,RW,RH)
slides.append(im)

# 4 СНАРЯДЫ
im,d=canvas()
kicker(d,"Спортивные направления")
title(d,1.25,[("Три вида спорта на одной площадке",TXT)],size=34)
cw=3.95;gap=0.22;x0=0.85;cy=2.7;ch=4.1
data=[("c_bmx","BMX","Сила, координация и зрелищность."),
 ("c_scooter","Трюковой самокат","Доступный старт для детей."),
 ("c_skate","Скейтборд","Баланс и чувство тела.")]
for i,(img,t,desc) in enumerate(data):
    x=x0+i*(cw+gap)
    rrect(d,x,cy,cw,ch,0.16,fill=CARD,outline=LINE,ow=2)
    imh=cw/(600/470)
    paste(im,img,x+0.12,cy+0.12,cw-0.24,imh,border=False); d=ImageDraw.Draw(im)
    text(d,x+0.25,cy+imh+0.2,t,19,WHITE,b=True)
    for j,ln in enumerate(wrap(d,desc,14,cw-0.5)):
        text(d,x+0.25,cy+imh+0.6+j*0.26,ln,14,DIM)
text(d,0.85,6.95,"Дети осваивают новые снаряды и находят дело по душе.",16,GOLD)
slides.append(im)

# 5 БЕЗОПАСНОСТЬ
im,d=canvas()
kicker(d,"Главный приоритет")
title(d,1.3,[("Безопасность прежде всего",ACC)],size=36)
items=[("Защитная экипировка.","Шлемы, наколенники, налокотники."),
 ("Безопасное покрытие.","Сертифицированные материалы."),
 ("Зонирование.","Зоны для новичков и опытных."),
 ("Освещение и аптечка.","Свет вечером и медпункт.")]
yy=2.55
for i,(t,desc) in enumerate(items):
    rrect(d,0.9,yy,0.5,0.5,0.12,fill=ACC)
    textc(d,1.15,yy+0.25,str(i+1),18,DARK,b=True)
    runs(d,1.55,yy+0.1,[(t+" ",WHITE,True),(desc,DIM,False)],14)
    yy+=1.02
paste(im,"safety",RX,2.4,RW,RH)
slides.append(im)

# 6 ТРЕНЕР
im,d=canvas()
kicker(d,"Ключевая роль")
runs(d,0.85,1.3,[("Нужен ",TXT,True),("тренер",GOLD,True)],40)
for j,ln in enumerate(wrap(d,"Без наставника спорт превращается в риск. Тренер — основа безопасного парка.",15,5.7)):
    text(d,0.9,2.3+j*0.28,ln,15,DIM)
bullets(d,3.5,[("Правильная техника.","Учит трюкам и падениям без травм."),
 ("Контроль и порядок.","Следит за дисциплиной и экипировкой."),
 ("Спортивные секции.","Группы, прогресс, соревнования."),
 ("Наставничество.","Авторитетный взрослый рядом.")])
paste(im,"coach",RX,RY,RW,RH)
slides.append(im)

# 7 СОЦИАЛЬНАЯ ПОЛЬЗА
im,d=canvas()
kicker(d,"Социальная сфера")
title(d,1.3,[("Польза для города",TXT),("и его молодёжи",TXT)],size=36)
pills=["Здоровье и спорт вместо улицы","Меньше детской преступности","Активный полезный досуг",
 "Новые знакомства и команда","Точка притяжения города","Будущие чемпионы Осетии","Гордость и развитие региона"]
px,py=0.9,2.6;xx=px;maxx=6.55
for t in pills:
    w=0.5+len(t)*0.108
    if xx+w>maxx: xx=px;py+=0.62
    rrect(d,xx,py,w,0.55,0.12,fill=BG2,outline=LINE,ow=2)
    textc(d,xx+w/2,py+0.275,t,12.5,TXT,b=True)
    xx+=w+0.16
paste(im,"social",RX,RY,RW,RH)
slides.append(im)

# 8 БЮДЖЕТ
im,d=canvas()
kicker(d,"Экономика и бюджет")
title(d,1.3,[("Выгода для бизнеса и казны",TXT)],size=33)
bullets(d,3.0,[("Рост продаж.","Местные торговцы продают самокаты, скейты, BMX и защиту."),
 ("Новые рабочие места.","Магазины, прокат, сервис и тренеры."),
 ("Средства в бюджет.","Налоги и сборы пополняют казну города.")])
paste(im,"budget",RX,RY,RW,RH)
slides.append(im)

# 9 ВСЕ ПЛЮСЫ
im,d=canvas()
kicker(d,"Итог")
title(d,1.3,[("Все плюсы проекта",TXT)],size=38)
bullets(d,2.7,[("Спорт и развитие.","BMX, самокат, скейтборд — новые навыки."),
 ("Безопасность.","Экипировка, зонирование, тренер, медпункт."),
 ("Социальная польза.","Здоровый досуг и меньше рисков."),
 ("Доход в бюджет.","Торговля инвентарём и налоги в казну.")])
paste(im,"plus",RX,RY,RW,RH)
slides.append(im)

# 10 ПРИЗЫВ
im,d=canvas()
paste_h(im,"final",0,7.5); d=ImageDraw.Draw(im)
rect(d,0,0,0.22,7.5,ACC)
kicker(d,"Призыв к действию")
text(d,0.85,1.5,"Дадим детям",54,TXT,b=True)
text(d,0.85,2.4,"место для роста",54,GOLD,b=True)
rect(d,0.9,3.9,0.07,1.4,ACC)
qy=4.05
for ln in wrap(d,"«Скейт-парк — это инвестиция в активное будущее Южной Осетии».",21,4.0,b=True):
    text(d,1.15,qy,ln,21,TXT,b=True,it=True); qy+=0.34
rrect(d,0.9,5.7,3.4,0.62,0.14,fill=ACC)
textc(d,0.9+1.7,6.01,"Поддержать проект",18,DARK,b=True)
text(d,4.55,5.85,"Цхинвал · 2026",18,DIM,b=True)
slides.append(im)

for i,im in enumerate(slides,1):
    im.save("preview/slide_%02d.png"%i)

# контактный лист 2x5
cols,rows=2,5; pad=20; tw=W//2
th=int(tw*H/W)
sheet=Image.new("RGB",(cols*tw+pad*(cols+1),rows*th+pad*(rows+1)),(20,24,36))
for i,im in enumerate(slides):
    t=im.resize((tw,th)); r,c=divmod(i,cols)
    sheet.paste(t,(pad+c*(tw+pad),pad+r*(th+pad)))
sheet.save("preview/contact_sheet.png")
print("DONE preview")
