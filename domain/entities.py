from dataclasses import dataclass

@dataclass(frozen=True)
class Livro:
    id: int
    titulo: str
    autor: str
    preco: float
    estoque: int
    estante: str

@dataclass(frozen=True)
class Reserva:
    livro_id: int
    expira_em: str
