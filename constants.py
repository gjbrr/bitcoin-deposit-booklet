from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white


# ---------- SHARED LAYOUT CONSTANTS ----------
SLOTS_PER_SHEET = 3
PAGE_W, PAGE_H = 8.5 * inch, 11 * inch     # standard US Letter, portrait
STRIP_W = PAGE_W
STRIP_H = PAGE_H / SLOTS_PER_SHEET          # ~3.667in

GUTTER = 0.42 * inch                        # blank left margin reserved for staples, on EVERY strip
RIGHT_MARGIN = 0.15 * inch
PERF_X = STRIP_W - 3.05 * inch              # x position of the vertical cut line on check strips

GRAY = HexColor("#8a8f9c")
LGRAY = HexColor("#d8dbe3")

DERIVATION_DISPLAY = "m/84'/0'/0'/0/i  (BIP84 native segwit, receive chain)"
OUTDIR = "/home/gary/walletbooklets"
