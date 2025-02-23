from dataclasses import dataclass

@dataclass
class Fornitore:
    ID_FORNITORE: str
    NOME_FORNITORE: str
    COSTO_FISSO_AL_DRONE: int
    DIMENSIONE_DRONE: int
    COSTO_AL_CHILOMETRO: float

    def __str__(self):
        return f"{self.ID_FORNITORE}"

    def __hash__(self):
        return hash(self.ID_FORNITORE)