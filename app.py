from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from models import GenerateRequest
from booklet.generator import generate_booklet

from pydantic import BaseModel


class GenerateRequest(BaseModel):
    title: str
    zpub: str
    lightning_address: str = ""
    num_addresses: int = 25

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/generate", response_class=StreamingResponse)

def generate(request: GenerateRequest):
    pdf_stream = generate_booklet(
        title=request.title,
        zpub=request.zpub,
        lightning_address=request.lightning_address,
        num_addresses=request.num_addresses,
    )

    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                "attachment; filename=bitcoin-deposit-booklet.pdf"
        },
    )




