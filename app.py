"""Composition root: conecta interface, casos de uso e adaptador TXT."""
from application.use_cases import Livraria
from infrastructure.txt_repository import RepositorioTXT
from presentation.http_server import iniciar_servidor

if __name__ == '__main__':
    iniciar_servidor(Livraria(RepositorioTXT()))
