from pydantic import BaseModel


class Restaurant(BaseModel):
    id: int 
    title: str
    description: str
    photo_url: str
    address: str