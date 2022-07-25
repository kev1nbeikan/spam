import dataclasses


@dataclasses.dataclass
class Product:
    id_: int
    name: str
    days: int
    price: int

