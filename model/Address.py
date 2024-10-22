from dataclasses import dataclass


@dataclass
class Address:
    CODICE_VIA: int
    NUMERO: int
    TIPO: str
    ANNCSU: str
    ID_NIL: int
    NIL: str
    LAT_WGS84: float
    LONG_WGS84: float

    def __str__(self):
        return f"{self.TIPO} {self.ANNCSU} {self.NUMERO}"

    def __hash__(self):
        return hash(self.CODICE_VIA+self.NUMERO)