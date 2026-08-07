

from booklet.constants import (GUTTER, STRIP_W, black,white, GRAY,DERIVATION_DISPLAY,RIGHT_MARGIN,LGRAY,PERF_X)
from reportlab.lib.units import inch

from booklet.layout import (
    staple_edge,
    scatter_sparkles,
    draw_piggy,
    strip_header,
    hcut_line,
    vcut_line,
    draw_coin
)

from booklet.qr import qr_image_reader



# ---------- STRIP CONTENT RENDERERS (each draws into a STRIP_W x h canvas, origin at strip's bottom-left) ----------
def render_cover(ctx, c, h):
    staple_edge(c, h)
    scatter_sparkles(c, 10, GUTTER + 0.2*inch, STRIP_W - 0.2*inch, 0.15*inch, h - 0.15*inch)
    cx = GUTTER + (STRIP_W - GUTTER) * 0.27
    draw_piggy(c, cx, h * 0.58, 1.35*inch)

    tx = GUTTER + (STRIP_W - GUTTER) * 0.66
    c.setFont("Helvetica-Bold", 19)
    c.setFillColor(black)
    c.drawCentredString(tx, h * 0.68, ctx["title"])
    c.setFont("Helvetica", 10)
    c.drawCentredString(tx, h * 0.68 - 0.26*inch, "a savings booklet")

    c.setLineWidth(1)
    c.rect(tx - 1.55*inch, h * 0.15, 4.1*inch, 0.5*inch, fill=0, stroke=1)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(tx, h * 0.24 + 0.33*inch, "This booklet belongs to:")
#    c.line(tx - 1.35*inch, h * 0.24 + 0.13*inch, tx + 1.35*inch, h * 0.24 + 0.13*inch)

    c.setFont("Helvetica-Oblique", 6.8)
    c.drawCentredString(tx, 0.20*inch, "No private keys or secret words are stored in this booklet.")

def render_instructions(ctx, c, h):
    staple_edge(c, h)
    y = strip_header(c, h, ctx["title"], "How it works")
    x0 = GUTTER + 0.2*inch
    y -= 0.16*inch

    entries = [
        ("b", "Printing & assembly"),
        ("l", "Cut every sheet into 3 strips along the dashed lines, then stack"),
        ("l", "all strips in order and staple along the left edge (dotted line)."),
        ("b", "Using a check"),
        ("l", "RIGHT side -- big QR of the address. Someone scans it with a"),
        ("l", "  wallet app to send sats here. Tear it off once deposited."),
        ("l", "LEFT stub -- stays bound. Small QR opens the address on"),
        ("l", "  mempool.space (free block explorer) to check the balance."),
        ("b", "Recording a deposit"),
        ("l", "Fill in date, sats received, and cost basis (what those sats"),
        ("l", "were worth in dollars that day). Copy into the ledger too."),
        ("l", "This booklet only holds PUBLIC receive addresses -- it can't"),
        ("l", "spend anything, so it's safe to lose or leave lying around."),
        ("l", "The secret words that control spending live elsewhere,"),
        ("l", "on purpose."),
    ]
    for kind, text in entries:
        if kind == "b":
            c.setFont("Helvetica-Bold", 8.3)
            c.drawString(x0, y, text)
            y -= 0.185*inch
        else:
            c.setFont("Helvetica", 7.8)
            c.drawString(x0, y, text)
            y -= 0.155*inch

    c.setFont("Helvetica", 6.6)
    c.setFillColor(GRAY)
    c.drawString(x0, 0.16*inch, DERIVATION_DISPLAY)
    c.setFillColor(black)

def render_wallet_info(ctx, c, h, zpub):
    staple_edge(c, h)

    y = strip_header(c, h, ctx["title"], "Owner Copy")

    x0 = GUTTER + 0.18*inch

    qr_size = 1.55*inch
    qr_x = x0
    qr_y = 0.52*inch

    c.rect(qr_x-0.03*inch, qr_y-0.03*inch,
           qr_size+0.06*inch, qr_size+0.06*inch)

    c.drawImage(
        qr_image_reader(zpub, box_size=6),
        qr_x,
        qr_y,
        qr_size,
        qr_size,
    )

    tx = qr_x + qr_size + 0.20*inch

    c.setFont("Helvetica-Bold",9)
    c.drawString(tx,h-0.72*inch,"Account Extended Public Key (zpub)")

    c.setFont("Helvetica",7.2)

    lines = [
        "Use this QR code to generate additional",
        "deposit slips for THIS booklet.",
        "",
        "✓ Can generate every receiving address.",
        "✓ Can view balances and transactions.",
        "✗ Cannot spend bitcoin.",
        "",
        "Never print or share:",
        "• Seed phrase",
        "• xprv / yprv / zprv",
    ]

    yy = h-0.92*inch
    for line in lines:
        c.drawString(tx,yy,line)
        yy -= 0.14*inch

    c.setFont("Courier",5.5)

    chars = 52
    wrapped = [zpub[i:i+chars] for i in range(0,len(zpub),chars)]

    yy = 0.38*inch
    for line in wrapped:
        c.drawString(x0,yy,line)
        yy -= 0.10*inch

def render_ln_address(ctx, c, h, ln_address):
    staple_edge(c, h)

    y = strip_header(c, h, ctx["title"], "Lightning Adress")

    x0 = GUTTER + 0.18*inch

    qr_size = 1.55*inch
    qr_x = x0
    qr_y = 0.52*inch

    c.rect(qr_x-0.03*inch, qr_y-0.03*inch,
           qr_size+0.06*inch, qr_size+0.06*inch)

    c.drawImage(
        qr_image_reader(ln_address, box_size=6),
        qr_x,
        qr_y,
        qr_size,
        qr_size,
    )

    tx = qr_x + qr_size + 0.20*inch

    c.setFont("Helvetica-Bold",9)
    c.drawString(tx,h-0.72*inch,"Lightning Address")

    c.setFont("Helvetica",7.2)

    lines = [
        "Use this QR code to send to Lightning address associated with this booklet.",
    ]

    yy = h-0.92*inch
    for line in lines:
        c.drawString(tx,yy,line)
        yy -= 0.14*inch

    c.setFont("Courier",5.5)

    chars = 52
    wrapped = [ln_address[i:i+chars] for i in range(0,len(ln_address),chars)]

    yy = 0.38*inch
    for line in wrapped:
        c.drawString(x0,yy,line)
        yy -= 0.10*inch

def render_ledger(ctx, c, h, addresses, start_idx, total, part_num, part_count):
    staple_edge(c, h)
    label = "Running Total" if part_count == 1 else f"Running Total ({part_num}/{part_count})"
    y = strip_header(c, h, ctx["title"], label)
    x0 = GUTTER + 0.2*inch
    right_edge = STRIP_W - RIGHT_MARGIN - 0.15*inch
    y -= 0.10*inch

    col_labels = ["#", "Address ends in", "Sats", "Cost basis ($)", "Notes"]
    col_x = [x0, x0 + 0.34*inch, x0 + 1.55*inch, x0 + 2.55*inch, x0 + 4.55*inch]

    row_h = 0.255*inch
    c.setFont("Helvetica-Bold", 7.2)
    c.setFillColor(LGRAY)
#    c.rect(x0 - 0.04*inch, y - 0.02*inch, right_edge - x0 + 0.08*inch, 0.19*inch, fill=1, stroke=0)
    c.setFillColor(black)
    for x, lbl in zip(col_x, col_labels):
        c.drawString(x, y + 0.02*inch, lbl)
    y -= row_h

    c.setFont("Helvetica", 7.4)
    for i, addr in enumerate(addresses):
        yy = y - i * row_h
        c.setStrokeColor(LGRAY)
        c.setLineWidth(0.5)
        c.line(x0 - 0.04*inch, yy - 0.055*inch, right_edge, yy - 0.055*inch)
        c.setFillColor(black)
        c.drawString(col_x[0], yy, str(start_idx + i + 1))
        c.setFont("Courier", 7)
        c.drawString(col_x[1], yy, "..." + addr[-8:])
        c.setFont("Helvetica", 7.4)
        cols = col_x[2:]
        widths = [col_x[2]-col_x[1]-0.1*inch, col_x[3]-col_x[2]-0.1*inch,
                  col_x[4]-col_x[3]-0.1*inch, right_edge-col_x[4]-0.04*inch]
        for cx, cw in zip(cols, widths):
            c.setStrokeColor(black)
            c.setLineWidth(0.4)
#            c.rect(cx - 0.03*inch, yy - 0.065*inch, cw, 0.185*inch)

def render_check(ctx, c, h, index, addr, total):
    staple_edge(c, h)
    y_top = h - 0.04*inch
    header_h = 0.30*inch
    draw_coin(c, GUTTER + 0.14*inch, y_top - header_h*0.55, 0.11*inch)
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(black)
    c.drawString(GUTTER + 0.30*inch, y_top - header_h*0.7, ctx["title"])
    c.setFont("Helvetica", 7.6)
    c.drawRightString(PERF_X - 0.12*inch, y_top - header_h*0.7, f"Check {index+1} of {total}")
    c.setLineWidth(0.9)
    c.line(GUTTER, y_top - header_h, PERF_X - 0.12*inch, y_top - header_h)

    vcut_line(c, PERF_X, 0.06*inch, h - 0.06*inch)

    # ---- LEFT stub ----
    sx0 = GUTTER + 0.16*inch
    sx1 = PERF_X - 0.26*inch
    fy = y_top - header_h - 0.22*inch
    row_h = 0.26*inch

    c.setFont("Helvetica", 8)
    c.drawString(sx0, fy, "Date:")
    c.setLineWidth(0.8)
    c.line(sx0 + 0.38*inch, fy - 0.03*inch, sx1, fy - 0.03*inch)
    fy -= row_h

    c.drawString(sx0, fy, "Sats received:")
    c.line(sx0 + 0.95*inch, fy - 0.03*inch, sx1, fy - 0.03*inch)
    fy -= row_h

    c.drawString(sx0, fy, "Cost basis ($):")
    c.line(sx0 + 1.0*inch, fy - 0.03*inch, sx1, fy - 0.03*inch)
    fy -= row_h

    c.rect(sx0, fy - 0.10*inch, 0.13*inch, 0.13*inch)
    c.setFont("Helvetica", 8)
    c.drawString(sx0 + 0.20*inch, fy - 0.055*inch, "Used")
    c.drawString(sx0 + 1.0*inch, fy - 0.055*inch, "Notes:")
    c.line(sx0 + 1.38*inch, fy - 0.08*inch, sx1, fy - 0.08*inch)
    fy -= (row_h + 0.08*inch)

    small_qr = 1.3*inch
    qr_x = sx0
    qr_y = max(0.15*inch, fy - small_qr)
    qr_url = f"https://mempool.space/address/{addr}"
    c.setLineWidth(0.7)
    c.rect(qr_x - 0.03*inch, qr_y - 0.03*inch, small_qr + 0.06*inch, small_qr + 0.06*inch)
    c.drawImage(qr_image_reader(qr_url, box_size=6), qr_x, qr_y, small_qr, small_qr)
    lx = qr_x + small_qr + 0.14*inch
    c.setFont("Helvetica-Bold", 7.2)
    c.drawString(lx, qr_y + small_qr - 0.13*inch, "check balance")
    c.setFont("Helvetica", 6.6)
    c.drawString(lx, qr_y + small_qr - 0.28*inch, "mempool.space")
    c.setFont("Courier", 8.8)
    c.drawString(lx, qr_y + small_qr - 0.46*inch,  addr)

    # ---- RIGHT tear-off ----
    tx0 = PERF_X + 0.22*inch
    tx1 = STRIP_W - RIGHT_MARGIN
    tcx = (tx0 + tx1) / 2

    c.setFont("Helvetica-Bold", 8.2)
    c.drawCentredString(tcx, y_top - header_h - 0.12*inch, "SCAN TO RECEIVE")

    qr_size = 1.95*inch
    qr_x2 = tcx - qr_size/2
    qr_y2 = y_top - header_h - 0.26*inch - qr_size
    c.setLineWidth(1.1)
    pad = 0.06*inch
    c.rect(qr_x2 - pad, qr_y2 - pad, qr_size + 2*pad, qr_size + 2*pad)
    c.drawImage(qr_image_reader(addr), qr_x2, qr_y2, qr_size, qr_size)

    c.setFont("Courier", 6.4)
    c.drawCentredString(tcx, qr_y2 - 0.15*inch, addr[:22])
    c.drawCentredString(tcx, qr_y2 - 0.27*inch, addr[22:])
    c.setFont("Helvetica", 6.0)
    c.setFillColor(GRAY)
    c.drawCentredString(tcx, max(0.08*inch, qr_y2 - 0.42*inch), f"check #{index+1}")
    c.setFillColor(black)

