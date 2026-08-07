"""
Temporary test harness for the in-memory PDF generator.

This file exists while the web interface is under development.
Eventually FastAPI will replace it.
"""


from booklet.generator import generate_booklet


zpub = "zpub6rUHMuuX7kwkqreT5X7GPT9iuXLcy5bXukexbpmY7RuALCpHgGSda1rghnRfgi7Vxw7b5LPqtTiwddsyDMeqosC9cEBYaiJV5abwQGTEMV3"
title = ""
num_addresses = 5
lightning_address=""

pdf = generate_booklet(
    zpub,
    title,
    lightning_address,
    num_addresses,
)

with open("test.pdf", "wb") as f:
    f.write(pdf.getvalue())
