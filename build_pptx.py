# -*- coding: utf-8 -*-
"""Готовая презентация проекта скейт-парка в Цхинвале (с иллюстрациями)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BG     = RGBColor(0x0A, 0x0E, 0x1A)
BG2    = RGBColor(0x0F, 0x16, 0x28)
CARD   = RGBColor(0x14, 0x1D, 0x33)
LINE   = RGBColor(0x24, 0x31, 0x50)
ACCENT = RGBColor(0xFF, 0x57, 0x22)
GOLD   = RGBColor(0xFF, 0xC1, 0x07)
TXT    = RGBColor(0xEA, 0xF0, 0xFA)
DIM    = RGBColor(0x8B, 0x9A, 0xB8)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GREEN  = RGBColor(0x34, 0xD3, 0x99)
DARK   = RGBColor(0x0A, 0x0E, 0x1A)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
blank = prs.slide_layouts[6]
FONT = "Arial"
IMG = "img/%s.png"

def slide(bg=BG):
    s = prs.slides.add_slide(blank)
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    r.fill.solid(); r.fill.fore_color.rgb = bg; r.line.fill.background(); r.shadow.inherit=False
    return s

def setrun(r, text, size, color, bold=False, italic=False):
    r.text=text; r.font.size=Pt(size); r.font.name=FONT
    r.font.color.rgb=color; r.font.bold=bold; r.font.italic=italic

def tbox(s,l,t,w,h,anchor=MSO_ANCHOR.TOP):
    tb=s.shapes.add_textbox(l,t,w,h); tf=tb.text_frame
    tf.word_wrap=True; tf.vertical_anchor=anchor; return tf

def para(tf,text,size,color,bold=False,italic=False,sa=6,align=PP_ALIGN.LEFT,first=False,sb=0):
    p=tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment=align; p.space_after=Pt(sa); p.space_before=Pt(sb)
    setrun(p.add_run(),text,size,color,bold,italic); return p

def kicker(s,text,l=Inches(0.85),t=Inches(0.62)):
    bar=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,l,t+Inches(0.09),Inches(0.34),Pt(3))
    bar.fill.solid(); bar.fill.fore_color.rgb=ACCENT; bar.line.fill.background(); bar.shadow.inherit=False
    tf=tbox(s,l+Inches(0.45),t,Inches(8),Inches(0.45))
    para(tf,text.upper(),14,GOLD,bold=True,first=True)

def picture(s,name,l,t,w,h,border=True):
    pic=s.shapes.add_picture(IMG%name,l,t,w,h)
    if border:
        pic.line.color.rgb=LINE; pic.line.width=Pt(1.25)
    return pic

def title_block(s,top,lines,size=40):
    tf=tbox(s,Inches(0.85),top,Inches(6.1),Inches(2))
    for i,(t,c) in enumerate(lines):
        para(tf,t,size,c,bold=True,first=(i==0),sa=0)

def bullets(s,top,items,w=Inches(5.7)):
    tf=tbox(s,Inches(0.95),top,w,Inches(3.8))
    for i,(b,d) in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.space_after=Pt(11); p.space_before=Pt(0)
        setrun(p.add_run(),"●  ",13,ACCENT,bold=True)
        setrun(p.add_run(),b+"  ",16,WHITE,bold=True)
        if d: setrun(p.add_run(),d,15,DIM)

# панель справа под иллюстрацию (16:9 от 1400x900 → ratio 1.5556)
RX, RW = Inches(6.95), Inches(5.7)
RH = Inches(5.7/ (1400/900))   # ~3.66"
RY = Inches(2.05)

# ---------- 1. ТИТУЛ ----------
s=slide()
iw=Inches(7.5*(1400/900)); ix=Emu(int((SW-iw)/1));
iw_emu=int(7.5*(1400/900)*914400); ix_emu=int((int(SW)-iw_emu)/2)
s.shapes.add_picture(IMG%"hero",ix_emu,0,height=SH)
band=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,Inches(0.22),SH)
band.fill.solid(); band.fill.fore_color.rgb=ACCENT; band.line.fill.background(); band.shadow.inherit=False
kicker(s,"Социальный проект · Южная Осетия")
tf=tbox(s,Inches(0.85),Inches(1.45),Inches(11),Inches(2.6))
para(tf,"Скейт-парк",70,TXT,bold=True,first=True,sa=0)
p=tf.add_paragraph(); p.space_after=Pt(0)
setrun(p.add_run(),"в ",70,TXT,bold=True); setrun(p.add_run(),"Цхинвале",70,GOLD,bold=True)
tf2=tbox(s,Inches(0.9),Inches(5.55),Inches(8),Inches(1.2))
para(tf2,"Современное и безопасное пространство для досуга\nи спорта детей и подростков города.",19,DIM,first=True)
pill=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(0.9),Inches(6.55),Inches(4.5),Inches(0.6))
pill.fill.solid(); pill.fill.fore_color.rgb=ACCENT; pill.line.fill.background(); pill.shadow.inherit=False
ptf=pill.text_frame; ptf.vertical_anchor=MSO_ANCHOR.MIDDLE
pp=ptf.paragraphs[0]; pp.alignment=PP_ALIGN.CENTER
setrun(pp.add_run(),"BMX · Самокат · Скейтборд",18,RGBColor(0x1A,0x12,0x05),bold=True)

# ---------- 2. ПРОБЛЕМА ----------
s=slide()
kicker(s,"Проблема")
title_block(s,Inches(1.4),[("Детям и подросткам",TXT),("негде проводить время",TXT)],size=34)
bullets(s,Inches(3.4),[
 ("Нет инфраструктуры.","В Цхинвале почти нет современных площадок для активного отдыха молодёжи."),
 ("Опасно.","Дети катаются на улицах, парковках и тротуарах — риск для них и прохожих."),
 ("Энергия без выхода.","У подростков нет места для здорового и полезного досуга."),
])
picture(s,"problem",RX,RY,RW,RH)

# ---------- 3. РЕШЕНИЕ ----------
s=slide()
kicker(s,"Решение")
title_block(s,Inches(1.4),[("Построить современный",TXT),("скейт-парк",GOLD)],size=34)
bullets(s,Inches(3.4),[
 ("Качественное покрытие.","Рампы, фигуры и гладкое профессиональное основание."),
 ("Зона отдыха.","Скамейки, освещение и озеленение — место притяжения города."),
 ("Для всех уровней.","От первых шагов новичка до тренировки сложных трюков."),
])
picture(s,"solution",RX,RY,RW,RH)

# ---------- 4. СНАРЯДЫ (3 карточки) ----------
s=slide()
kicker(s,"Спортивные направления")
title_block(s,Inches(1.25),[("Три вида спорта на одной площадке",TXT)],size=34)
cw=Inches(3.95); gap=Inches(0.22); x0=Inches(0.85); cy=Inches(2.7); ch=Inches(4.1)
data=[("c_bmx","BMX","Сила, координация и зрелищность."),
      ("c_scooter","Трюковой самокат","Доступный старт для детей."),
      ("c_skate","Скейтборд","Баланс и чувство тела.")]
for i,(img,t,d) in enumerate(data):
    x=x0+i*(cw+gap)
    box=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,x,cy,cw,ch)
    box.fill.solid(); box.fill.fore_color.rgb=CARD; box.line.color.rgb=LINE; box.shadow.inherit=False
    imh=Inches(float(cw.inches)/(600/470))
    s.shapes.add_picture(IMG%img,x+Inches(0.12),cy+Inches(0.12),cw-Inches(0.24),imh)
    tf=tbox(s,x+Inches(0.25),cy+imh+Inches(0.2),cw-Inches(0.5),Inches(1.2))
    para(tf,t,19,WHITE,bold=True,first=True,sa=4)
    para(tf,d,14,DIM)
tf=tbox(s,Inches(0.85),Inches(6.95),Inches(11.6),Inches(0.5))
para(tf,"Дети осваивают новые спортивные снаряды и находят дело по душе.",16,GOLD,first=True)

# ---------- 5. БЕЗОПАСНОСТЬ ----------
s=slide()
kicker(s,"Главный приоритет")
title_block(s,Inches(1.3),[("Безопасность прежде всего",ACCENT)],size=36)
items=[("Защитная экипировка.","Шлемы, наколенники, налокотники, перчатки — для всех."),
       ("Безопасное покрытие.","Сертифицированные материалы, без острых углов."),
       ("Зонирование.","Раздельные зоны для новичков и опытных."),
       ("Освещение и аптечка.","Свет вечером и медпункт первой помощи на месте.")]
yy=Inches(2.55)
for i,(t,d) in enumerate(items):
    chip=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(0.9),yy,Inches(0.5),Inches(0.5))
    chip.fill.solid(); chip.fill.fore_color.rgb=ACCENT; chip.line.fill.background(); chip.shadow.inherit=False
    ctf=chip.text_frame; ctf.vertical_anchor=MSO_ANCHOR.MIDDLE
    cp=ctf.paragraphs[0]; cp.alignment=PP_ALIGN.CENTER
    setrun(cp.add_run(),str(i+1),18,DARK,bold=True)
    tf=tbox(s,Inches(1.55),yy-Inches(0.05),Inches(5.3),Inches(0.7),MSO_ANCHOR.MIDDLE)
    p=tf.paragraphs[0]; p.space_after=Pt(0)
    setrun(p.add_run(),t+" ",15,WHITE,bold=True); setrun(p.add_run(),d,13.5,DIM)
    yy+=Inches(1.02)
picture(s,"safety",RX,Inches(2.4),RW,RH)

# ---------- 6. ТРЕНЕР ----------
s=slide()
kicker(s,"Ключевая роль")
tf=tbox(s,Inches(0.85),Inches(1.3),Inches(6),Inches(1))
p=tf.paragraphs[0]
setrun(p.add_run(),"Нужен ",40,TXT,bold=True); setrun(p.add_run(),"тренер",40,GOLD,bold=True)
tf2=tbox(s,Inches(0.9),Inches(2.25),Inches(5.7),Inches(1))
para(tf2,"Без наставника спорт превращается в риск. Тренер — основа безопасного и результативного парка.",15,DIM,first=True)
bullets(s,Inches(3.5),[
 ("Правильная техника.","Учит трюкам и падениям так, чтобы избежать травм."),
 ("Контроль и порядок.","Следит за дисциплиной и экипировкой на площадке."),
 ("Спортивные секции.","Группы, прогресс, соревнования и мотивация."),
 ("Наставничество.","Авторитетный взрослый, который направляет ребят."),
])
picture(s,"coach",RX,RY,RW,RH)

# ---------- 7. СОЦИАЛЬНАЯ ПОЛЬЗА ----------
s=slide()
kicker(s,"Социальная сфера")
title_block(s,Inches(1.3),[("Польза для города",TXT),("и его молодёжи",TXT)],size=36)
pills=["Здоровье и спорт вместо улицы","Меньше детской преступности","Активный полезный досуг",
       "Новые знакомства и команда","Точка притяжения города","Будущие чемпионы Осетии",
       "Гордость и развитие региона"]
px,py=Inches(0.9),Inches(2.6); xx=px; maxx=Inches(6.55)
for txt in pills:
    w=Inches(0.5+len(txt)*0.108)
    if xx+w>maxx: xx=px; py=Inches(py.inches+0.62)
    pl=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,xx,py,w,Inches(0.55))
    pl.fill.solid(); pl.fill.fore_color.rgb=BG2; pl.line.color.rgb=LINE; pl.shadow.inherit=False
    ptf=pl.text_frame; ptf.vertical_anchor=MSO_ANCHOR.MIDDLE
    ptf.margin_left=Inches(0.1); ptf.margin_right=Inches(0.1)
    pp=ptf.paragraphs[0]; pp.alignment=PP_ALIGN.CENTER
    setrun(pp.add_run(),txt,12.5,TXT,bold=True)
    xx=Inches(xx.inches+w.inches+0.16)
picture(s,"social",RX,RY,RW,RH)

# ---------- 8. ЭКОНОМИКА / БЮДЖЕТ ----------
s=slide()
kicker(s,"Экономика и бюджет")
title_block(s,Inches(1.3),[("Выгода для бизнеса и казны",TXT)],size=33)
bullets(s,Inches(3.0),[
 ("Рост продаж.","Местные торговцы продают самокаты, скейты, BMX, запчасти и защиту."),
 ("Новые рабочие места.","Магазины, прокат, сервис и тренеры."),
 ("Средства в бюджет.","Налоги и сборы с торговли пополняют казну города."),
])
picture(s,"budget",RX,RY,RW,RH)

# ---------- 9. ВСЕ ПЛЮСЫ ----------
s=slide()
kicker(s,"Итог")
title_block(s,Inches(1.4),[("Все плюсы проекта",TXT)],size=36)
bullets(s,Inches(2.7),[
 ("Спорт и развитие.","BMX, самокат, скейтборд — новые навыки для детей."),
 ("Безопасность.","Экипировка, зонирование, тренер и медпункт."),
 ("Социальная польза.","Здоровый досуг и меньше уличных рисков."),
 ("Доход в бюджет.","Торговля инвентарём и налоги в казну города."),
])
picture(s,"plus",RX,RY,RW,RH)

# ---------- 10. ПРИЗЫВ ----------
s=slide()
s.shapes.add_picture(IMG%"final",ix_emu,0,height=SH)
band=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,Inches(0.22),SH)
band.fill.solid(); band.fill.fore_color.rgb=ACCENT; band.line.fill.background(); band.shadow.inherit=False
kicker(s,"Призыв к действию")
tf=tbox(s,Inches(0.85),Inches(1.5),Inches(11),Inches(2))
para(tf,"Дадим детям",54,TXT,bold=True,first=True,sa=0)
para(tf,"место для роста",54,GOLD,bold=True,sa=0)
barq=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(0.9),Inches(3.95),Inches(0.07),Inches(1.2))
barq.fill.solid(); barq.fill.fore_color.rgb=ACCENT; barq.line.fill.background(); barq.shadow.inherit=False
tf2=tbox(s,Inches(1.15),Inches(3.9),Inches(4.0),Inches(1.4),MSO_ANCHOR.MIDDLE)
para(tf2,"«Скейт-парк — это инвестиция в активное будущее Южной Осетии».",21,TXT,bold=True,italic=True,first=True)
pill=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(0.9),Inches(5.7),Inches(3.4),Inches(0.62))
pill.fill.solid(); pill.fill.fore_color.rgb=ACCENT; pill.line.fill.background(); pill.shadow.inherit=False
ptf=pill.text_frame; ptf.vertical_anchor=MSO_ANCHOR.MIDDLE
pp=ptf.paragraphs[0]; pp.alignment=PP_ALIGN.CENTER
setrun(pp.add_run(),"Поддержать проект",18,DARK,bold=True)
tf3=tbox(s,Inches(4.55),Inches(5.7),Inches(4),Inches(0.62),MSO_ANCHOR.MIDDLE)
para(tf3,"Цхинвал · 2026",18,DIM,bold=True,first=True)

prs.save("/home/user/napitki-fartuny/skatepark.pptx")
print("OK slides:", len(prs.slides._sldIdLst))
