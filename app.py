from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from booklet.generator import generate_booklet

app = FastAPI()


@app.post("/generate")
def generate(request):
    pdf = generate_booklet(
        title=request.title,
        zpub=request.zpub,
        lightning=request.lightning,
        count=request.count,
    )

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                "attachment; filename=bitcoin-deposit-booklet.pdf"
        },
    )
