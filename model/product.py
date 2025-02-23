from dataclasses import dataclass, field


@dataclass
class Product:
    item_id: int
    name: str
    category: str
    price: float
    short_description: str
    depth: int
    height: int
    width: int
    volume: int = field(init=False)
    dimensione: int = field(init=False)

    def __post_init__(self):
        self.volume = self.calculate_volume()
        self.dimensione = self.set_dimensione()

    def calculate_volume(self) -> int:
        return self.depth * self.height * self.width

    def set_dimensione(self) -> int:
        if self.volume <= 200000:
            return 3
        elif self.volume <= 400000:
            return 4
        elif self.volume <= 1200000:
            return 5
        else:
            return 6

    def __str__(self):
        return f"{self.name} (volume {self.dimensione})"

    def __hash__(self):
        return hash(self.item_id)