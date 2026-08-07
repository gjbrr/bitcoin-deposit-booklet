
import random
from booklet.constants import (LGRAY, GRAY, GUTTER,STRIP_W, RIGHT_MARGIN, PAGE_W, black,white)
from reportlab.lib.units import inch

# ---------- LINE-ART HELPERS (black only, B&W friendly) ----------
def draw_coin(c, x, y, r):
    c.saveState()
    c.setFillColor(white)
    c.setStrokeColor(black)
    c.setLineWidth(r * 0.16)
    c.circle(x, y, r, fill=1, stroke=1)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", r * 1.15)
    c.drawCentredString(x, y - r * 0.38, "\u20BF")
    c.restoreState()

def draw_sparkle(c, x, y, size):
    c.saveState()
    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.line(x - size, y, x + size, y)
    c.line(x, y - size, x, y + size)
    c.line(x - size * 0.7, y - size * 0.7, x + size * 0.7, y + size * 0.7)
    c.line(x - size * 0.7, y + size * 0.7, x + size * 0.7, y - size * 0.7)
    c.restoreState()

def scatter_sparkles(c, n, xmin, xmax, ymin, ymax):
    for _ in range(n):
        x = random.uniform(xmin, xmax)
        y = random.uniform(ymin, ymax)
        size = random.uniform(0.025, 0.05) * inch
        draw_sparkle(c, x, y, size)

def draw_piggy(c, cx, cy, w):
    h = w * 0.62
    c.saveState()
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.setLineWidth(w * 0.02)
    leg_w, leg_h = w * 0.08, h * 0.22
    for dx in (-w * 0.26, -w * 0.07, w * 0.09, w * 0.28):
        c.rect(cx + dx, cy - h * 0.5 - leg_h, leg_w, leg_h, fill=0, stroke=1)
    c.ellipse(cx - w/2, cy - h/2, cx + w/2, cy + h/2, fill=1, stroke=1)
    p = c.beginPath()
    p.moveTo(cx - w * 0.28, cy + h * 0.40)
    p.lineTo(cx - w * 0.40, cy + h * 0.62)
    p.lineTo(cx - w * 0.14, cy + h * 0.46)
    p.close()
    c.drawPath(p, fill=1, stroke=1)
    snout_w, snout_h = w * 0.20, h * 0.15
    c.ellipse(cx + w * 0.30 - snout_w/2, cy - snout_h/2, cx + w * 0.30 + snout_w/2, cy + snout_h/2, fill=1, stroke=1)
    c.setFillColor(black)
    c.circle(cx + w * 0.30 - snout_w * 0.18, cy, snout_w * 0.06, fill=1, stroke=0)
    c.circle(cx + w * 0.30 + snout_w * 0.18, cy, snout_w * 0.06, fill=1, stroke=0)
    c.circle(cx + w * 0.11, cy + h * 0.13, w * 0.018, fill=1, stroke=0)
    c.setStrokeColor(black)
    c.setLineWidth(w * 0.022)
    c.line(cx - w * 0.06, cy + h * 0.43, cx + w * 0.08, cy + h * 0.43)
    draw_coin(c, cx + 0.0, cy + h * 0.66, w * 0.075)
    c.restoreState()

def scissors_mark(c, x, y):
    c.saveState()
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawCentredString(x, y, "\u2702")
    c.restoreState()

def vcut_line(c, x, y0, y1, label="cut / tear off after depositing"):
    c.saveState()
    c.setStrokeColor(black)
    c.setLineWidth(0.75)
    c.setDash([4, 3])
    c.line(x, y0, x, y1)
    c.setDash([])
    scissors_mark(c, x, y1 - 0.02*inch)
    c.saveState()
    c.translate(x + 0.10*inch, (y0 + y1) / 2)
    c.rotate(90)
    c.setFont("Helvetica-Oblique", 5.6)
    c.setFillColor(GRAY)
    c.drawCentredString(0, 0, label)
    c.restoreState()
    c.restoreState()

def hcut_line(c, y):
    """Horizontal dashed cut line between strips/slots on the same sheet."""
    c.saveState()
    c.setStrokeColor(black)
    c.setLineWidth(0.75)
    c.setDash([4, 3])
    c.line(0.1*inch, y, PAGE_W - 0.1*inch, y)
    c.setDash([])
    scissors_mark(c, 0.14*inch, y - 0.03*inch)
    c.setFont("Helvetica-Oblique", 5.6)
    c.setFillColor(GRAY)
    c.drawString(0.28*inch, y - 0.05*inch, "cut")
    c.restoreState()

def staple_edge(c, h):
    c.saveState()
    c.setStrokeColor(LGRAY)
    c.setLineWidth(0.75)
    c.setDash([2, 2])
    c.line(GUTTER, 0.08*inch, GUTTER, h - 0.08*inch)
    c.setDash([])
    for frac in (0.25, 0.75):
        yy = h * frac
        c.setFillColor(black)
        c.circle(GUTTER * 0.55, yy, 1.2, fill=1, stroke=0)
    c.restoreState()

def strip_header(c, h, title, right_label):
    y_top = h - 0.10*inch
    header_h = 0.30*inch
    draw_coin(c, GUTTER + 0.14*inch, y_top - header_h*0.5, 0.11*inch)
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(black)
    c.drawString(GUTTER + 0.30*inch, y_top - header_h*0.62, title)
    c.setFont("Helvetica", 7.5)
    c.drawRightString(STRIP_W - RIGHT_MARGIN - 0.1*inch, y_top - header_h*0.62, right_label)
    c.setLineWidth(0.9)
    c.line(GUTTER, y_top - header_h, STRIP_W - RIGHT_MARGIN - 0.1*inch, y_top - header_h)
    return y_top - header_h  # baseline y just below the rule
