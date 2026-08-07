from pydantic import BaseModel


class GenerateRequest(BaseModel):
    title: str
    zpub: str
    lightning_address: str = ""
    num_addresses: int = 25
