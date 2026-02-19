from pydantic import BaseModel


class DataModel(BaseModel):
    """
    Data Class: DataModel

    This data model represents a single, immutable data entry. 
    It is designed to be pedantic in nature: all fields are strictly typed, 
    validated upon instantiation, and documented thoroughly to ensure correctness, 
    traceability, and reproducibility across systems.

    Fields:
        url (str): the product url
        title (str): the product title or product name
        price (str):the product price
    """
    url : str
    title : str
    price : str