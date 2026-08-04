from constants import (OUTDIR,PAGE_H, PAGE_W, STRIP_H,SLOTS_PER_SHEET)

import os
from bitcoin.derive import derive_addresses
from booklet.renderers import (
    render_cover,
    render_instructions,
    render_wallet_info,
    render_ledger,
    render_check,
    hcut_line
    )

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# ---------- SLOT PACKING: lay out an ordered list of strip-renderers, 3 per sheet ----------
def paginate(c, ctx, addresses, zpub, ln_address):
    max_rows_per_ledger = int((STRIP_H - 0.55*inch) // (0.255*inch))
    chunks = [addresses[i:i+max_rows_per_ledger] for i in range(0, len(addresses), max_rows_per_ledger)]
    part_count = len(chunks)

    slots = []
    slots.append(lambda c, h: render_cover(ctx, c, h))
    slots.append(lambda c, h: render_instructions(ctx, c, h))
    slots.append(lambda c, h: render_wallet_info(ctx, c, h, zpub))
    if ln_address:
        slots.append(lambda c, h: render_ln_address(ctx, c, h, ln_address))

    start = 0
    for p, chunk in enumerate(chunks, start=1):
        slots.append(lambda c, h, chunk=chunk, start=start, p=p: render_ledger(
            ctx, c, h, chunk, start, len(addresses), p, part_count))
        start += len(chunk)
    for i, addr in enumerate(addresses):
        slots.append(lambda c, h, i=i, addr=addr: render_check(ctx, c, h, i, addr, len(addresses)))

    for sheet_start in range(0, len(slots), SLOTS_PER_SHEET):
        sheet_slots = slots[sheet_start:sheet_start + SLOTS_PER_SHEET]
        for slot_idx, render_fn in enumerate(sheet_slots):
            y_offset = PAGE_H - STRIP_H * (slot_idx + 1)
            c.saveState()
            c.translate(0, y_offset)
            render_fn(c, STRIP_H)
            c.restoreState()
            if slot_idx > 0:
                hcut_line(c, y_offset + STRIP_H)
        c.showPage()

# ---------- BUILD ONE BOOK ----------
def generate_booklet(label, zpub, num_addresses, filename, ln_address):
    addresses = derive_addresses(zpub, num_addresses)
    ctx = {"title": f"{label}'s Bitcoin Deposit Book" if label else "My Bitcoin Deposit Book"}
    outpath = os.path.join(OUTDIR, filename)
    c = canvas.Canvas(outpath, pagesize=(PAGE_W, PAGE_H))
    paginate(c, ctx, addresses,zpub, ln_address)
    c.save()
    print(f"Saved {outpath}  ({num_addresses} addresses, {label})")
    return outpath


