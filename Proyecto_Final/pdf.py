from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable, PageBreak, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Flowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import math

W, H = A4

# ── Paleta ─────────────────────────────────────────────
WINE      = colors.HexColor("#8B1A2B")
WINE_L    = colors.HexColor("#FAECE7")
BLUE      = colors.HexColor("#185FA5")
BLUE_L    = colors.HexColor("#E6F1FB")
GREEN     = colors.HexColor("#3B6D11")
GREEN_L   = colors.HexColor("#EAF3DE")
AMBER     = colors.HexColor("#854F0B")
AMBER_L   = colors.HexColor("#FAEEDA")
PURPLE    = colors.HexColor("#534AB7")
PURPLE_L  = colors.HexColor("#EEEDFE")
TEAL      = colors.HexColor("#0D6B6B")
TEAL_L    = colors.HexColor("#E0F5F5")
ROSE      = colors.HexColor("#9C2A6A")
ROSE_L    = colors.HexColor("#FAEAF4")
SLATE     = colors.HexColor("#3D4F6B")
SLATE_L   = colors.HexColor("#EEF1F7")
GRAY_BG   = colors.HexColor("#F5F5F2")
GRAY_LINE = colors.HexColor("#DDDDDD")
DARK      = colors.HexColor("#1A1A1A")
MID       = colors.HexColor("#666666")

THEME_COLORS = [BLUE, PURPLE, GREEN, AMBER, WINE, TEAL, ROSE, SLATE, colors.HexColor("#6B3A6B")]

# ── Estilos ────────────────────────────────────────────
def s(name, **kw):
    defaults = dict(fontName="Helvetica", fontSize=10, textColor=DARK, leading=16, spaceAfter=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

title_s  = s("T", fontName="Helvetica-Bold", fontSize=20, textColor=WINE, spaceAfter=3, alignment=TA_CENTER)
sub_s    = s("SB", fontSize=10, textColor=MID, spaceAfter=1, alignment=TA_CENTER)
body_s   = s("B", leading=17, spaceAfter=6, alignment=TA_JUSTIFY)
note_s   = s("N", fontName="Helvetica-Oblique", fontSize=8.5, textColor=MID, leading=13)
code_s   = s("C", fontName="Courier", fontSize=8.5, leading=13, textColor=DARK)
small_s  = s("SM", fontSize=8, textColor=MID, leading=12)
white_s  = s("W", fontName="Helvetica-Bold", fontSize=10, textColor=colors.white)

# ── Helpers ────────────────────────────────────────────
def arrow(c, x1, y1, x2, y2, col=MID, label="", lw=1):
    c.setStrokeColor(col); c.setLineWidth(lw)
    c.line(x1, y1, x2, y2)
    ang = math.atan2(y2-y1, x2-x1)
    sz = 6
    c.setFillColor(col)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - sz*math.cos(ang-0.4), y2 - sz*math.sin(ang-0.4))
    p.lineTo(x2 - sz*math.cos(ang+0.4), y2 - sz*math.sin(ang+0.4))
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    if label:
        c.setFillColor(DARK); c.setFont("Helvetica", 7)
        c.drawCentredString((x1+x2)/2, (y1+y2)/2+5, label)

def node(c, x, y, label, r=24, fg=BLUE, bg=BLUE_L, font_size=8):
    c.setFillColor(bg); c.setStrokeColor(fg); c.setLineWidth(1)
    c.circle(x, y, r, fill=1, stroke=1)
    c.setFillColor(fg); c.setFont("Helvetica-Bold", font_size)
    # wrap text
    words = label.split()
    if len(words) <= 2:
        c.drawCentredString(x, y-3, label)
    else:
        c.drawCentredString(x, y+3, " ".join(words[:2]))
        c.drawCentredString(x, y-7, " ".join(words[2:]))

def rect_node(c, x, y, w, h, label, fg=BLUE, bg=BLUE_L, font_size=8):
    c.setFillColor(bg); c.setStrokeColor(fg); c.setLineWidth(1)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
    c.setFillColor(fg); c.setFont("Helvetica-Bold", font_size)
    c.drawCentredString(x+w/2, y+h/2-3, label)

def code_block(c, x, y, lines, width, bg=GRAY_BG, col=GRAY_LINE):
    lh = 13; pad = 8
    h = lh*len(lines) + pad*2
    c.setFillColor(bg); c.setStrokeColor(col); c.setLineWidth(0.5)
    c.roundRect(x, y-h+pad, width, h, 4, fill=1, stroke=1)
    c.setFillColor(DARK); c.setFont("Courier", 8)
    for i, line in enumerate(lines):
        c.drawString(x+pad, y - i*lh, line)
    return h


# ══════════════════════════════════════════════════════
# SECTION HEADER FLOWABLE
# ══════════════════════════════════════════════════════
class SecHeader(Flowable):
    def __init__(self, num, title, color, subtitle="", width=461):
        super().__init__()
        self._w = width; self._h = 36 if subtitle else 30
        self._num = num; self._title = title
        self._color = color; self._sub = subtitle
    def wrap(self, aW, aH): return self._w, self._h
    def draw(self):
        c = self.canv
        c.setFillColor(self._color)
        c.roundRect(0, 0, self._w, self._h, 5, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(14, self._h - 20, f"{self._num}.  {self._title}")
        if self._sub:
            c.setFont("Helvetica", 8); c.setFillColor(colors.HexColor("#DDDDFF"))
            c.drawString(14, 6, self._sub)


# ══════════════════════════════════════════════════════
# 1. LÓGICA DE PROPOSICIONES
# ══════════════════════════════════════════════════════
class ProposicionesFlowable(Flowable):
    def __init__(self, width=461): super().__init__(); self._w=width; self._h=160
    def wrap(self,a,b): return self._w, self._h
    def draw(self):
        c = self.canv
        reglas = [
            (BLUE,   "Regla 1",  "maridaje(v,comida) ∧ precio(v) ≤ P",           "→  recomendar(v)",        "Condicional — match directo"),
            (PURPLE, "Regla 1b", "Regla1 ∧ tipo(v) = pref",                       "→  recomendar(v)",        "Conjuncion + filtro tipo"),
            (GREEN,  "Regla 2",  "¬Regla1 ∧ precio(v) ≤ P",                      "→  sugerir_popular(v)",   "Fallback por popularidad"),
            (AMBER,  "Regla 3",  "¬Regla1 ∧ ¬Regla2",                            "→  sin_resultado",        "Contradiccion del dominio"),
        ]
        rh = 34; y0 = self._h - 10
        for i, (col, name, cond, cons, nota) in enumerate(reglas):
            y = y0 - i*rh
            c.setFillColor(col if i==0 else colors.HexColor("#F0F4FF") if i%2==0 else GRAY_BG)
            # colored left strip
            c.setFillColor(col); c.rect(0, y-rh+4, 5, rh-4, fill=1, stroke=0)
            c.setFillColor(GRAY_BG); c.setStrokeColor(GRAY_LINE); c.setLineWidth(0.4)
            c.roundRect(6, y-rh+4, self._w-6, rh-4, 3, fill=1, stroke=1)
            # texts
            c.setFillColor(col); c.setFont("Helvetica-Bold", 8.5)
            c.drawString(14, y-12, name)
            c.setFillColor(DARK); c.setFont("Courier", 8)
            c.drawString(80, y-12, cond)
            c.setFillColor(col); c.setFont("Courier-Bold", 8)
            c.drawString(80+230, y-12, cons)
            c.setFillColor(MID); c.setFont("Helvetica", 7)
            c.drawRightString(self._w-6, y-23, nota)

        # Clasificacion
        cls = [("Tautologia", "siempre V", GREEN, GREEN_L),
               ("Contradiccion","siempre F", WINE, WINE_L),
               ("Contingencia","V y F posibles", BLUE, BLUE_L)]
        cw = (self._w-20)/3
        bx = 0
        for name, desc, fg, bg in cls:
            c.setFillColor(bg); c.setStrokeColor(fg); c.setLineWidth(0.8)
            c.roundRect(bx, 2, cw, 20, 3, fill=1, stroke=1)
            c.setFillColor(fg); c.setFont("Helvetica-Bold", 7.5)
            c.drawCentredString(bx+cw/2, 10, name)
            c.setFillColor(MID); c.setFont("Helvetica", 7)
            c.drawCentredString(bx+cw/2, 3, desc)
            bx += cw+10


# ══════════════════════════════════════════════════════
# 2. LÓGICA DE PREDICADOS
# ══════════════════════════════════════════════════════
class PredicadosFlowable(Flowable):
    def __init__(self, width=461): super().__init__(); self._w=width; self._h=155
    def wrap(self,a,b): return self._w, self._h
    def draw(self):
        c = self.canv
        # Estructura visual
        c.setFillColor(PURPLE_L); c.setStrokeColor(PURPLE); c.setLineWidth(1)
        c.roundRect(0, self._h-44, self._w, 40, 6, fill=1, stroke=1)
        c.setFillColor(PURPLE); c.setFont("Courier-Bold", 13)
        c.drawCentredString(self._w/2, self._h-26, "maridaje(  carne_asada  ,  la_cetto_cabernet  )")
        # Etiquetas con flechas
        pts = [(72, "predicado"), (215, "argumento 1\n(comida)"), (370, "argumento 2\n(vino)")]
        for x, lbl in pts:
            c.setStrokeColor(MID); c.setLineWidth(0.7)
            c.line(x, self._h-44, x, self._h-56)
            c.setFillColor(MID); c.setFont("Helvetica", 7)
            for j, part in enumerate(lbl.split("\n")):
                c.drawCentredString(x, self._h-64-j*10, part)
        # Hechos
        hechos = [
            "% HECHOS (base de conocimiento)",
            "maridaje(la_cetto_cabernet, carne_asada).",
            "maridaje(la_cetto_cabernet, pasta).",
            "maridaje(monte_xanic_kristel, mariscos).",
            "es_tipo(la_cetto_cabernet, tinto).",
            "precio(la_cetto_cabernet, 200).",
            "",
            "% REGLA (motor de inferencia)",
            "recomendar(Vino, Comida, P) :-",
            "    maridaje(Vino, Comida),",
            "    precio(Vino, Precio),",
            "    Precio =< P.",
        ]
        lh=11; pad=6; bh = lh*len(hechos)+pad*2
        c.setFillColor(GRAY_BG); c.setStrokeColor(PURPLE); c.setLineWidth(0.4)
        c.roundRect(0, 0, self._w, bh, 4, fill=1, stroke=1)
        c.setFont("Courier", 7.5); c.setFillColor(DARK)
        for i, line in enumerate(hechos):
            col = PURPLE if line.startswith("%") else (GREEN if line.startswith("recomendar") else DARK)
            c.setFillColor(col)
            c.drawString(8, bh - pad - lh*(i+1) + 3, line)


# ══════════════════════════════════════════════════════
# 3. REDES SEMÁNTICAS
# ══════════════════════════════════════════════════════
class RedSemanticaFlowable(Flowable):
    def __init__(self, width=461): super().__init__(); self._w=width; self._h=200
    def wrap(self,a,b): return self._w, self._h
    def draw(self):
        c = self.canv
        # Nodos
        positions = {
            "Vino":          (230, 185),
            "Tinto":         (130, 130),
            "Blanco":        (230, 130),
            "Espumoso":      (330, 130),
            "L.A. Cetto":    (60,  70),
            "Casa Madero":   (140, 70),
            "Monte Xanic":   (230, 70),
            "Sala Vive":     (330, 70),
            "precio=200":    (40,  15),
            "maridaje=Carne":(140, 15),
            "tipo=Blanco":   (240, 15),
            "burbujas":      (360, 15),
        }
        node_styles = {
            "Vino":     (PURPLE, PURPLE_L, 26),
            "Tinto":    (WINE,   WINE_L,   22),
            "Blanco":   (BLUE,   BLUE_L,   22),
            "Espumoso": (TEAL,   TEAL_L,   22),
            "L.A. Cetto":(WINE,  WINE_L,   18),
            "Casa Madero":(WINE, WINE_L,   18),
            "Monte Xanic":(BLUE, BLUE_L,   18),
            "Sala Vive": (TEAL,  TEAL_L,   18),
            "precio=200":(GREEN,GREEN_L,   15),
            "maridaje=Carne":(GREEN,GREEN_L,15),
            "tipo=Blanco":(GREEN,GREEN_L,  15),
            "burbujas":  (GREEN, GREEN_L,  15),
        }
        for name,(x,y) in positions.items():
            fg,bg,r = node_styles[name]
            node(c, x, y, name, r=r, fg=fg, bg=bg, font_size=7 if r<20 else 8)

        # Arcos
        arcs = [
            ("L.A. Cetto","Tinto","IS-A", WINE),
            ("Casa Madero","Tinto","IS-A", WINE),
            ("Monte Xanic","Blanco","IS-A", BLUE),
            ("Sala Vive","Espumoso","IS-A", TEAL),
            ("Tinto","Vino","IS-A", PURPLE),
            ("Blanco","Vino","IS-A", PURPLE),
            ("Espumoso","Vino","IS-A", PURPLE),
            ("L.A. Cetto","precio=200","HAS", GREEN),
            ("L.A. Cetto","maridaje=Carne","HAS", GREEN),
            ("Monte Xanic","tipo=Blanco","HAS", GREEN),
            ("Sala Vive","burbujas","HAS", GREEN),
        ]
        for src, dst, lbl, col in arcs:
            x1,y1 = positions[src]; x2,y2 = positions[dst]
            r1 = node_styles[src][2]; r2 = node_styles[dst][2]
            dx,dy = x2-x1, y2-y1; dist=math.hypot(dx,dy)
            if dist>0:
                sx = x1+dx/dist*r1; sy = y1+dy/dist*r1
                ex = x2-dx/dist*r2; ey = y2-dy/dist*r2
                arrow(c, sx, sy, ex, ey, col=col, label=lbl)

        # Leyenda
        c.setFillColor(MID); c.setFont("Helvetica", 7.5); y_leg = 2
        c.drawString(0, y_leg, "IS-A = herencia (es un tipo de)")
        c.drawString(200, y_leg, "HAS = tiene propiedad/atributo")


# ══════════════════════════════════════════════════════
# 4. TRIPLETA OAV
# ══════════════════════════════════════════════════════
class OAVFlowable(Flowable):
    def __init__(self, width=461): super().__init__(); self._w=width; self._h=155
    def wrap(self,a,b): return self._w, self._h
    def draw(self):
        c = self.canv
        # Header
        headers = [("OBJETO", WINE, WINE_L), ("ATRIBUTO", BLUE, BLUE_L), ("VALOR", GREEN, GREEN_L)]
        cw = self._w/3 - 4
        for i,(h,fg,bg) in enumerate(headers):
            x = i*(cw+6)
            c.setFillColor(fg); c.roundRect(x,self._h-22,cw,18,3,fill=1,stroke=0)
            c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8)
            c.drawCentredString(x+cw/2, self._h-13, h)

        tripletas = [
            ("Casa Madero 3V",        "maridaje",   "Mole"),
            ("L.A. Cetto Cabernet",   "maridaje",   "Carne asada"),
            ("Monte Xanic Kristel",   "maridaje",   "Mariscos"),
            ("L.A. Cetto Cabernet",   "tipo",       "Tinto"),
            ("Monte Xanic Kristel",   "tipo",       "Blanco"),
            ("Sala Vive Brut",        "tipo",       "Espumoso"),
            ("Riunite Lambrusco",     "precio",     "$180 MXN"),
            ("Casa Madero 3V",        "precio",     "$520 MXN"),
            ("L.A. Cetto Petite",     "perfil",     "intenso y especiado"),
        ]
        rh = (self._h - 28) / len(tripletas)
        for i,(obj,attr,val) in enumerate(tripletas):
            y = self._h - 28 - (i+1)*rh
            bg = GRAY_BG if i%2==0 else colors.white
            c.setFillColor(bg); c.rect(0,y,self._w,rh,fill=1,stroke=0)
            # obj
            c.setFillColor(WINE); c.setFont("Helvetica",7.5)
            c.drawString(4, y+rh/2-3, obj)
            # attr
            c.setFillColor(BLUE); c.setFont("Helvetica-Bold",7.5)
            c.drawCentredString(self._w/2, y+rh/2-3, attr)
            # val
            c.setFillColor(GREEN); c.setFont("Helvetica",7.5)
            c.drawRightString(self._w-4, y+rh/2-3, val)
            # dividers
            c.setStrokeColor(GRAY_LINE); c.setLineWidth(0.3)
            c.line(0,y,self._w,y)
            c.line(self._w/3,y,self._w/3,y+rh)
            c.line(2*self._w/3,y,2*self._w/3,y+rh)

        # Busqueda del motor
        c.setFillColor(AMBER_L); c.setStrokeColor(AMBER); c.setLineWidth(0.6)
        c.roundRect(0,0,self._w,14,3,fill=1,stroke=1)
        c.setFillColor(AMBER); c.setFont("Helvetica-Bold",7.5)
        c.drawString(6,4,"Motor busca:  Atributo = 'maridaje'  AND  Valor CONTIENE comida_usuario  →  retorna Objeto (vino)")


# ══════════════════════════════════════════════════════
# 5. MARCOS / FRAMES
# ══════════════════════════════════════════════════════
class FramesFlowable(Flowable):
    def __init__(self, width=461): super().__init__(); self._w=width; self._h=200
    def wrap(self,a,b): return self._w, self._h
    def draw(self):
        c = self.canv
        frames = [
            ("L.A. Cetto Cabernet", WINE, WINE_L, [
                ("nombre","L.A. Cetto Cabernet"),("bodega","L.A. Cetto"),
                ("tipo","Tinto"),("uva","Cabernet Sauvignon"),
                ("popularidad","95%"),("precio","$200"),
                ("perfil","tanico y robusto"),("maridaje_target","Carne, Pasta, Mole"),
            ]),
            ("Monte Xanic Kristel", BLUE, BLUE_L, [
                ("nombre","Monte Xanic V.K."),("bodega","Monte Xanic"),
                ("tipo","Blanco"),("uva","Sauvignon Blanc"),
                ("popularidad","94%"),("precio","$450"),
                ("perfil","citrico y mineral"),("maridaje_target","Mariscos, Sushi"),
            ]),
        ]
        fw = self._w/2 - 8
        for fi,(fname,fg,bg,slots) in enumerate(frames):
            fx = fi*(fw+16)
            # header
            c.setFillColor(fg); c.roundRect(fx,self._h-24,fw,22,4,fill=1,stroke=0)
            c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8)
            c.drawCentredString(fx+fw/2, self._h-13, fname)
            # body
            c.setFillColor(colors.white); c.setStrokeColor(fg); c.setLineWidth(0.8)
            c.rect(fx, 0, fw, self._h-24, fill=1, stroke=1)
            rh = (self._h-28) / len(slots)
            for i,(slot,val) in enumerate(slots):
                y = self._h-24 - (i+1)*rh
                is_key = slot=="maridaje_target"
                c.setFillColor(bg if is_key else (GRAY_BG if i%2==0 else colors.white))
                c.rect(fx+1,y,fw-2,rh,fill=1,stroke=0)
                c.setStrokeColor(GRAY_LINE); c.setLineWidth(0.3)
                c.line(fx,y,fx+fw,y)
                c.line(fx+fw*0.46,y,fx+fw*0.46,y+rh)
                c.setFillColor(MID); c.setFont("Helvetica",7)
                c.drawString(fx+4,y+rh/2-3,slot)
                c.setFillColor(fg if is_key else DARK)
                c.setFont("Helvetica-Bold" if is_key else "Helvetica",7)
                c.drawString(fx+fw*0.47+3,y+rh/2-3,val)
        # etiqueta slots
        c.setFillColor(MID); c.setFont("Helvetica",7.5); c.drawString(0,0,"← Slots (atributos/propiedades)  |  maridaje_target = slot de conclusion/comportamiento →")


# ══════════════════════════════════════════════════════
# 6. GUIONES / SCRIPTS
# ══════════════════════════════════════════════════════
class GuionesFlowable(Flowable):
    def __init__(self, width=461): super().__init__(); self._w=width; self._h=200
    def wrap(self,a,b): return self._w, self._h
    def draw(self):
        c = self.canv
        # Guion: Compra de vino en CDMX
        pasos = [
            ("1. ENTRADA", TEAL, TEAL_L, [
                "Usuario ingresa: comida, presupuesto, tipo preferido",
                "Contexto: restaurante, celebracion, consumo casual",
            ]),
            ("2. BUSQUEDA", BLUE, BLUE_L, [
                "Motor consulta base de conocimiento (maridajes)",
                "Aplica filtro de presupuesto y tipo",
            ]),
            ("3. SELECCION", PURPLE, PURPLE_L, [
                "Ordena candidatos por popularidad CDMX",
                "Aplica regla de mayor coincidencia",
            ]),
            ("4. PRESENTACION", GREEN, GREEN_L, [
                "Muestra: nombre, bodega, precio, perfil",
                "Explica razon del maridaje",
            ]),
            ("5. CONFIRMACION", WINE, WINE_L, [
                "Usuario acepta o pide alternativa",
                "Sistema registra feedback (popularidad)",
            ]),
        ]
        pw = self._w / len(pasos)
        for i,(title,fg,bg,items) in enumerate(pasos):
            x = i*pw
            # box
            c.setFillColor(bg); c.setStrokeColor(fg); c.setLineWidth(0.8)
            c.roundRect(x+3, 30, pw-6, self._h-38, 5, fill=1, stroke=1)
            # header
            c.setFillColor(fg)
            c.roundRect(x+3, self._h-22, pw-6, 20, 5, fill=1, stroke=0)
            c.setFillColor(colors.white); c.setFont("Helvetica-Bold",7)
            c.drawCentredString(x+pw/2, self._h-12, title)
            # items
            c.setFillColor(DARK); c.setFont("Helvetica",6.5)
            for j,item in enumerate(items):
                # bullet
                c.setFillColor(fg); c.circle(x+9, self._h-40-j*22, 2, fill=1, stroke=0)
                c.setFillColor(DARK)
                # wrap 2 lines
                words = item.split()
                half = len(words)//2
                l1 = " ".join(words[:half]); l2 = " ".join(words[half:])
                c.drawString(x+14, self._h-37-j*22, l1)
                c.drawString(x+14, self._h-47-j*22, l2)
            # arrow to next
            if i < len(pasos)-1:
                arrow(c, x+pw-3, self._h/2, x+pw+3, self._h/2, col=fg)

        # Titulo del guion
        c.setFillColor(TEAL); c.setFont("Helvetica-Bold",9)
        c.drawString(0, self._h+2, "Guion: 'Compra/Recomendacion de Vino en CDMX'")


# ══════════════════════════════════════════════════════
# 7. REGLAS DE PRODUCCIÓN
# ══════════════════════════════════════════════════════
class ReglasFlowable(Flowable):
    def __init__(self, width=461): super().__init__(); self._w=width; self._h=190
    def wrap(self,a,b): return self._w, self._h
    def draw(self):
        c = self.canv
        reglas = [
            (BLUE,   "R1", "SI maridaje(V,comida) ∧ precio(V) ≤ presupuesto",
                           "ENTONCES recomendar(V)", "Maridaje directo dentro de presupuesto"),
            (PURPLE, "R2", "SI R1 ∧ tipo(V) = preferencia_usuario",
                           "ENTONCES recomendar_preferido(V)", "Refinamiento por tipo de uva/estilo"),
            (GREEN,  "R3", "SI ¬R1 ∧ precio(V) ≤ presupuesto",
                           "ENTONCES sugerir_popular(V)", "Fallback: mas popular en rango"),
            (AMBER,  "R4", "SI popularidad(V) > 90 ∧ precio(V) ≤ 250",
                           "ENTONCES marcar_popular_economico(V)", "Etiqueta especial precio-calidad"),
            (WINE,   "R5", "SI tipo(V) = 'Tinto' ∧ maridaje(V,'Tacos')",
                           "ENTONCES advertir('Maridaje atipico')", "Control de calidad del maridaje"),
            (TEAL,   "R6", "SI presupuesto < min_precio_KB",
                           "ENTONCES notificar('Presupuesto insuficiente')", "Regla de borde / sin datos"),
        ]
        rh = (self._h-10) / len(reglas)
        for i,(fg,rid,cond,cons,desc) in enumerate(reglas):
            y = self._h - 10 - (i+1)*rh
            bg = colors.white if i%2==0 else GRAY_BG
            c.setFillColor(fg); c.rect(0,y+2,5,rh-2,fill=1,stroke=0)
            c.setFillColor(bg); c.setStrokeColor(GRAY_LINE); c.setLineWidth(0.3)
            c.rect(6,y+2,self._w-6,rh-2,fill=1,stroke=1)
            # Etiqueta
            c.setFillColor(fg); c.setFont("Helvetica-Bold",8.5)
            c.drawString(12, y+rh-13, rid)
            # Condicion
            c.setFillColor(DARK); c.setFont("Courier",7.5)
            c.drawString(36, y+rh-13, cond)
            # Consecuente
            c.setFillColor(fg); c.setFont("Courier-Bold",7.5)
            c.drawString(36, y+rh-24, cons)
            # Descripcion
            c.setFillColor(MID); c.setFont("Helvetica",7)
            c.drawRightString(self._w-4, y+rh-24, desc)


# ══════════════════════════════════════════════════════
# 8. ÁRBOL DE DECISIÓN
# ══════════════════════════════════════════════════════
class ArbolFlowable(Flowable):
    def __init__(self, width=461): super().__init__(); self._w=width; self._h=220
    def wrap(self,a,b): return self._w, self._h
    def draw(self):
        c = self.canv
        # Nodo raiz
        def dnode(x,y,text,fg,bg,w=90,h=22):
            c.setFillColor(bg); c.setStrokeColor(fg); c.setLineWidth(0.8)
            c.roundRect(x-w/2,y-h/2,w,h,4,fill=1,stroke=1)
            c.setFillColor(fg); c.setFont("Helvetica-Bold",7.5)
            c.drawCentredString(x,y-3,text)

        def leaf(x,y,text,fg,bg):
            c.setFillColor(bg); c.setStrokeColor(fg); c.setLineWidth(1)
            c.roundRect(x-50,y-12,100,22,3,fill=1,stroke=1)
            c.setFillColor(fg); c.setFont("Helvetica-Bold",7)
            c.drawCentredString(x,y-3,text)

        def line(x1,y1,x2,y2,label="",col=GRAY_LINE):
            c.setStrokeColor(col); c.setLineWidth(0.7)
            c.line(x1,y1,x2,y2)
            if label:
                c.setFillColor(MID); c.setFont("Helvetica",6.5)
                c.drawCentredString((x1+x2)/2+8,(y1+y2)/2,label)

        # Nivel 0 - raiz
        cx = self._w/2
        dnode(cx, self._h-18, "¿Hay maridaje directo?", BLUE, BLUE_L, w=140)

        # Nivel 1
        line(cx, self._h-30, cx-130, self._h-68, "SI", BLUE)
        line(cx, self._h-30, cx+70,  self._h-68, "NO", WINE)

        dnode(cx-130, self._h-80, "¿Cabe en presupuesto?", GREEN, GREEN_L, w=130)
        dnode(cx+70,  self._h-80, "¿Hay vinos en rango?", AMBER, AMBER_L, w=130)

        # Nivel 2 izq
        line(cx-130, self._h-92, cx-175, self._h-130, "SI", GREEN)
        line(cx-130, self._h-92, cx-80,  self._h-130, "NO", WINE)

        dnode(cx-175, self._h-142, "¿Pref. de tipo?", PURPLE, PURPLE_L, w=100)
        leaf(cx-80,   self._h-142, "Ampliar presupuesto", WINE, WINE_L)

        # Nivel 2 der
        line(cx+70, self._h-92, cx+30,  self._h-130, "SI", AMBER)
        line(cx+70, self._h-92, cx+120, self._h-130, "NO", WINE)

        dnode(cx+30,  self._h-142, "Sugerir popular", GREEN, GREEN_L, w=100)
        leaf(cx+120,  self._h-142, "Sin resultado", WINE, WINE_L)

        # Nivel 3
        line(cx-175, self._h-154, cx-210, self._h-188, "SI", PURPLE)
        line(cx-175, self._h-154, cx-140, self._h-188, "NO", GREEN)

        leaf(cx-210, self._h-200, "Recomendar (filtrado)", PURPLE, PURPLE_L)
        leaf(cx-140, self._h-200, "Recomendar (general)", GREEN, GREEN_L)

        # leyenda
        c.setFillColor(MID); c.setFont("Helvetica",7)
        c.drawString(0,0,"Raiz: condicion inicial  |  Nodo interno: pregunta de decision  |  Hoja: accion final del sistema")


# ══════════════════════════════════════════════════════
# 9. AGENDA
# ══════════════════════════════════════════════════════
class AgendaFlowable(Flowable):
    def __init__(self, width=461): super().__init__(); self._w=width; self._h=195
    def wrap(self,a,b): return self._w, self._h
    def draw(self):
        c = self.canv
        # Columnas: Prioridad | Regla activada | Condicion satisfecha | Accion
        items = [
            (1, "R4 — popular_economico", "popularidad>90 ∧ precio≤250", "marcar(riunite, 'precio-calidad')",  GREEN),
            (2, "R1 — match directo",     "maridaje(v,comida) ∧ precio≤P", "recomendar(la_cetto, usuario)",   BLUE),
            (3, "R2 — filtro tipo",       "R1 ∧ tipo(v)=pref",            "recomendar_preferido(la_cetto)",   PURPLE),
            (4, "R5 — control calidad",   "tipo='Tinto' ∧ maridaje='Sushi'","advertir('Maridaje atipico')",   AMBER),
            (5, "R3 — fallback",          "¬R1 ∧ precio(v)≤P",            "sugerir_popular(riunite)",         WINE),
            (6, "R6 — presupuesto bajo",  "presupuesto < 180",            "notificar('Sin opciones')",        TEAL),
        ]
        headers = ["Prior.", "Regla activada", "Condicion satisfecha", "Accion"]
        widths  = [38, 130, 160, 133]
        hh = 20; rh = (self._h-hh-15)/len(items)

        # Header
        x=0
        for i,(h,w) in enumerate(zip(headers,widths)):
            c.setFillColor(SLATE); c.rect(x,self._h-hh,w,hh,fill=1,stroke=0)
            c.setFillColor(colors.white); c.setFont("Helvetica-Bold",7.5)
            c.drawCentredString(x+w/2, self._h-12, h)
            x+=w

        # Rows
        for ri,(pri,regla,cond,accion,fg) in enumerate(items):
            y = self._h-hh-(ri+1)*rh
            bg = GRAY_BG if ri%2==0 else colors.white
            c.setFillColor(bg); c.rect(0,y,self._w,rh,fill=1,stroke=0)
            # Prioridad badge
            c.setFillColor(fg); c.circle(widths[0]/2, y+rh/2, 9, fill=1, stroke=0)
            c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8)
            c.drawCentredString(widths[0]/2, y+rh/2-3, str(pri))
            # Regla
            c.setFillColor(fg); c.setFont("Helvetica-Bold",7)
            c.drawString(widths[0]+3, y+rh/2-3, regla)
            # Condicion
            c.setFillColor(DARK); c.setFont("Courier",6.5)
            c.drawString(widths[0]+widths[1]+3, y+rh/2-3, cond)
            # Accion
            c.setFillColor(fg); c.setFont("Courier",6.5)
            c.drawString(widths[0]+widths[1]+widths[2]+3, y+rh/2-3, accion)
            # separadores
            c.setStrokeColor(GRAY_LINE); c.setLineWidth(0.3); c.line(0,y,self._w,y)
            x=0
            for w in widths[:-1]:
                x+=w; c.line(x,y,x,y+rh)

        # Nota ciclo
        c.setFillColor(SLATE_L); c.setStrokeColor(SLATE); c.setLineWidth(0.5)
        c.roundRect(0,0,self._w,13,3,fill=1,stroke=1)
        c.setFillColor(SLATE); c.setFont("Helvetica",7.5)
        c.drawString(6,3,"Ciclo del motor: (1) Evaluar condiciones  →  (2) Insertar en agenda por prioridad  →  (3) Ejecutar accion de mayor prioridad  →  repetir")


# ══════════════════════════════════════════════════════
# CONSTRUIR PDF
# ══════════════════════════════════════════════════════
doc = SimpleDocTemplate(
    "/Users/javiercruzhernandez/Desktop/Inicio/Escuela/Octavo/Sistemas_expertos/Sistemas-Expertos/Proyecto_Final/representacion_conocimiento_vinos.pdf",
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=1.8*cm,
    title="Representacion del Conocimiento — Vinos CDMX",
)

story = []

# ─ Portada ─
story.append(Spacer(1,0.1*cm))
story.append(Paragraph("Representacion del Conocimiento", title_s))
story.append(Paragraph("Sistema Experto de Vinos CDMX 2026", sub_s))
story.append(Paragraph("Aplicacion de los 9 paradigmas al dominio de recomendacion de vinos", sub_s))
story.append(HRFlowable(width="100%", thickness=1.5, color=WINE, spaceAfter=12))

def section(num, title, color, subtitle, flowable, body_text, note_text=None):
    blocks = []
    blocks.append(KeepTogether([
        SecHeader(num, title, color, subtitle),
        Spacer(1,5),
        Paragraph(body_text, body_s),
        Spacer(1,5),
        flowable,
        Spacer(1,4),
    ]))
    if note_text:
        blocks.append(Paragraph(note_text, note_s))
    blocks.append(Spacer(1,12))
    return blocks

story += section("1","Logica de Proposiciones", BLUE,
    "Las reglas del motor son proposiciones IF-THEN clasificables como tautologias, contradicciones o contingencias",
    ProposicionesFlowable(),
    "Las reglas de inferencia del sistema se expresan como proposiciones logicas compuestas con los conectores "
    "∧ (AND), ¬ (NOT) y → (condicional). La Regla 1 es una tautologia del dominio: si las condiciones se cumplen, "
    "la recomendacion siempre se produce. La Regla 3 es la contradiccion del dominio: solo se activa cuando "
    "todas las anteriores fallan.",
    "Conectores usados: ∧ conjuncion (AND), ¬ negacion (NOT), → condicional (IF-THEN). "
    "Clasificacion: Tautologia=siempre V, Contradiccion=siempre F, Contingencia=V o F segun entradas."
)

story += section("2","Logica de Predicados", PURPLE,
    "La base de conocimiento se expresa como hechos y reglas — equivalente a Prolog",
    PredicadosFlowable(),
    "Cada vino, relacion y maridaje es un hecho atomico: maridaje(la_cetto, carne_asada). "
    "El motor de inferencia implementa la clausula de Horn: recomendar(Vino,Comida,P) :- maridaje(Vino,Comida), "
    "precio(Vino,Precio), Precio =< P. Las variables (con mayuscula) se sustituyen al consultar, "
    "identico al funcionamiento de un interprete Prolog.",
    "El operador :- equivale a IF. La coma equivale a AND. El guion bajo _ es variable anonima (cualquier valor)."
)

story += section("3","Redes Semanticas", GREEN,
    "Los tipos de vino se organizan en jerarquia con arcos IS-A (herencia) y HAS (atributos)",
    RedSemanticaFlowable(),
    "Los vinos y categorias forman una red de nodos conectados por arcos etiquetados. "
    "El arco IS-A define herencia: L.A. Cetto IS-A Tinto IS-A Vino. Gracias a la herencia, "
    "L.A. Cetto hereda automaticamente todas las propiedades de Tinto y de Vino sin repetirlas. "
    "El arco HAS asigna atributos concretos a cada nodo hoja.",
    "La herencia permite reestructurar la red para manejar excepciones — identico al ejemplo de "
    "Tweety el pinguino del profesor: Bird1 (vuela) y Bird2 (camina) como subclases separadas."
)

story += section("4","Tripleta OAV (Objeto - Atributo - Valor)", AMBER,
    "Cada dato de la base de conocimiento es una tripleta: el vino es el Objeto, la propiedad el Atributo",
    OAVFlowable(),
    "Toda la informacion del sistema se puede descomponer en tripletas OAV. El motor busca sistematicamente "
    "tripletas donde Atributo='maridaje' y Valor contiene la comida del usuario. Si encuentra una coincidencia, "
    "el Objeto (vino) entra a la lista de candidatos. Esta representacion facilita agregar nuevos vinos y "
    "maridajes sin modificar la logica del motor.",
    "El Valor es el dato preciso (ej. 'Mole', '$200 MXN') — NO es otro atributo, exactamente como "
    "definio el profesor: 'Valor es el valor preciso que toma el atributo, NO es otro atributo'."
)

story.append(PageBreak())

story += section("5","Marcos (Frames)", WINE,
    "Cada vino es un frame con slots (atributos), valores y un slot de conclusion/comportamiento",
    FramesFlowable(),
    "Cada vino en la base de conocimiento es un marco con: nombre del frame, slots (nombre, bodega, tipo, "
    "uva, popularidad, precio, perfil, maridaje_target) y sus valores. El slot maridaje_target actua como "
    "conclusion o comportamiento: cuando el motor lo evalua positivo, dispara la recomendacion. "
    "Es identico al frame 'Hamburgesa' del profesor con sus slots de pan, carne, aderezos y el "
    "comportamiento 'comprar si...'.",
    "Los slots tambien se llaman 'slots' o 'ranuras'. Un frame puede heredar slots de otro frame padre, "
    "exactamente como en la herencia de las redes semanticas."
)

story += section("6","Guiones (Scripts)", TEAL,
    "El proceso de recomendacion sigue un guion: secuencia de pasos con roles, props y escenas predefinidas",
    GuionesFlowable(),
    "Un guion captura el conocimiento sobre situaciones tipicas y secuenciales. El guion "
    "'Compra/Recomendacion de Vino en CDMX' tiene 5 escenas fijas: (1) entrada de datos del usuario, "
    "(2) busqueda en la base de conocimiento, (3) seleccion del candidato optimo, (4) presentacion del "
    "resultado con explicacion, y (5) confirmacion o solicitud de alternativa. Cada escena tiene actores "
    "(usuario, motor), props (vinos, maridajes) y condiciones de entrada/salida.",
    "Los guiones permiten al sistema anticipar el flujo sin necesidad de razonar desde cero cada vez — "
    "el conocimiento procedimental esta preconstruido en la estructura del guion."
)

story += section("7","Reglas de Produccion", ROSE,
    "El motor de inferencia es un sistema de produccion: conjunto de reglas SI-ENTONCES con base de hechos",
    ReglasFlowable(),
    "Las reglas de produccion son la forma mas directa de codificar el conocimiento experto. Cada regla tiene "
    "una parte condicion (SI) y una parte accion (ENTONCES). El motor evalua todas las reglas contra la "
    "base de hechos actual (memoria de trabajo), identifica cuales se activan (conflict set) y ejecuta la "
    "de mayor prioridad. R1-R3 cubren el flujo principal; R4 agrega etiquetas de calidad; R5 controla "
    "maridajes atipicos; R6 maneja casos borde.",
    "Estrategias de resolucion de conflictos usadas: especificidad (R2 es mas especifica que R1) y "
    "prioridad explicita (R4 se evalua primero al ser de enriquecimiento de datos)."
)

story += section("8","Arbol de Decision", SLATE,
    "La logica de seleccion del vino puede visualizarse como un arbol binario de preguntas y acciones",
    ArbolFlowable(),
    "El arbol de decision descompone el proceso de recomendacion en preguntas binarias (SI/NO). Cada nodo "
    "interno es una pregunta de decision; cada nodo hoja es una accion final. El arbol muestra visualmente "
    "todos los caminos posibles: desde el caso ideal (maridaje directo + presupuesto OK + tipo preferido) "
    "hasta los casos de borde (sin resultado). Es equivalente al motor de inferencia pero en forma grafica.",
    "El arbol permite identificar rapidamente los casos de borde y garantizar que el sistema tiene una "
    "respuesta para toda combinacion posible de entradas."
)

story += section("9","Agenda", colors.HexColor("#3D4F6B"),
    "El motor ordena las reglas activadas por prioridad antes de ejecutarlas — eso es la agenda",
    AgendaFlowable(),
    "La agenda es la lista ordenada de reglas que el motor tiene pendientes de ejecutar en cada ciclo. "
    "Primero se evaluan todas las condiciones contra la base de hechos (memoria de trabajo). Las reglas "
    "cuyas condiciones se satisfacen se insertan en la agenda ordenadas por prioridad. El motor ejecuta "
    "la accion de mayor prioridad, actualiza la base de hechos y reinicia el ciclo. Para el sistema de "
    "vinos: R4 (enriquecimiento) tiene prioridad 1, seguida de R1 (match directo), R2 (refinamiento), "
    "R5 (control calidad), R3 (fallback) y R6 (borde).",
    "El ciclo reconocer-actuar (recognize-act cycle) es el corazon de todo sistema experto basado en reglas: "
    "evaluar → insertar en agenda → ejecutar → repetir hasta que la agenda este vacia."
)

# Tabla resumen final
story.append(HRFlowable(width="100%", thickness=1, color=GRAY_LINE, spaceAfter=8))
story.append(Paragraph("Resumen — los 9 paradigmas en el sistema de vinos CDMX",
    ParagraphStyle("rh", fontName="Helvetica-Bold", fontSize=11, textColor=DARK, spaceAfter=8)))

resumen = [
    ["#","Paradigma","Rol en el sistema","Ejemplo concreto del sistema"],
    ["1","Log. Proposiciones","Define reglas IF-THEN del motor","maridaje(v,c) ∧ precio≤P → recomendar(v)"],
    ["2","Log. Predicados","Estructura hechos como predicados","maridaje(la_cetto, carne_asada)."],
    ["3","Redes Semanticas","Jerarquia IS-A/HAS de tipos de vino","L.A. Cetto IS-A Tinto IS-A Vino"],
    ["4","Tripleta OAV","Cada dato = (Objeto, Atributo, Valor)","(Casa Madero 3V, maridaje, Mole)"],
    ["5","Marcos/Frames","Cada vino es un frame con slots","Frame: L.A. Cetto | slot maridaje_target"],
    ["6","Guiones/Scripts","Flujo predefinido de recomendacion","Entrada→Busqueda→Seleccion→Respuesta"],
    ["7","Reglas Produccion","SI-ENTONCES con motor y agenda","R1: maridaje ∧ precio ≤ P → recomendar"],
    ["8","Arbol Decision","Preguntas binarias hasta accion","¿Maridaje? SI → ¿Presupuesto? SI → OK"],
    ["9","Agenda","Orden de ejecucion de reglas activas","Prioridad: R4→R1→R2→R5→R3→R6"],
]
col_ws = [18, 100, 150, 193]
t = Table(resumen, colWidths=col_ws)
t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), WINE),
    ("TEXTCOLOR",     (0,0),(-1,0), colors.white),
    ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0),(-1,-1), 8),
    ("FONTNAME",      (0,1),(-1,-1), "Helvetica"),
    ("FONTNAME",      (3,1),(3,-1),  "Courier"),
    ("FONTSIZE",      (3,1),(3,-1),  7.5),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, GRAY_BG]),
    ("GRID",          (0,0),(-1,-1), 0.4, GRAY_LINE),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ("LEFTPADDING",   (0,0),(-1,-1), 6),
    ("RIGHTPADDING",  (0,0),(-1,-1), 6),
    ("TOPPADDING",    (0,0),(-1,-1), 5),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("ALIGN",         (0,0),(0,-1),  "CENTER"),
]))
story.append(t)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica",8); canvas.setFillColor(MID)
    canvas.drawCentredString(W/2, 1.1*cm, "Representacion del Conocimiento — Sistema Experto de Vinos CDMX 2026")
    canvas.drawRightString(W-2*cm, 1.1*cm, f"Pag. {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF generado.")