from pydantic import BaseModel


class Data(BaseModel):
    url : str
    title : str
    price : str