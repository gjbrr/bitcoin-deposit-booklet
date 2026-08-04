# ---------- BOOKS TO GENERATE ----------
# Everything else about the layout stays identical --
# only the label and zpub change per book.

from booklet.generator import generate_booklet

BOOKS = [
    {
        "label": "",
        "zpub": "zpub6rUHMuuX7kwkqreT5X7GPT9iuXLcy5bXukexbpmY7RuALCpHgGSda1rghnRfgi7Vxw7b5LPqtTiwddsyDMeqosC9cEBYaiJV5abwQGTEMV3",
        "num_addresses": 5,
        "filename": "sample_bitcoin_checkbook.pdf",
        "ln_address": "",
    },
    
]

if __name__ == "__main__":
    outputs = []
    for book in BOOKS:
        outputs.append(generate_booklet(
            book["label"], book["zpub"], book.get("num_addresses", 10), book["filename"], book["ln_address"]
        ))
    print("\nGenerated:")
    for o in outputs:
        print(" ", o)   
