from datetime import datetime, timedelta, timezone
from threading import RLock
from domain.entities import Livro, Reserva
from application.ports import RepositorioLivraria

class Livraria:
    def __init__(self, repositorio: RepositorioLivraria):
        self.repositorio = repositorio
        self._lock = RLock()

    def _dados(self):
        dados = self.repositorio.carregar()
        agora = datetime.now(timezone.utc)
        validas = [r for r in dados['reservas'] if datetime.fromisoformat(r['expira_em']) > agora]
        if len(validas) != len(dados['reservas']):
            dados['reservas'] = validas
            self.repositorio.salvar(dados)
        return dados

    def consultar(self, termo=''):
        with self._lock:
            dados = self._dados()
            reservas = {r['livro_id'] for r in dados['reservas']}
            livros = []
            for registro in dados['livros']:
                livro = Livro(**registro)
                if termo.casefold() not in (livro.titulo + ' ' + livro.autor).casefold():
                    continue
                livros.append({**registro, 'disponivel': max(0, livro.estoque - (1 if livro.id in reservas else 0)), 'reservado': livro.id in reservas})
            return livros, [{**r, 'titulo': next(l['titulo'] for l in dados['livros'] if l['id'] == r['livro_id'])} for r in dados['reservas']], dados['desejos']

    def acao(self, rota, livro_id):
        with self._lock:
            dados = self._dados()
            livro = next((Livro(**l) for l in dados['livros'] if l['id'] == livro_id), None)
            if livro is None:
                raise ValueError('Livro não encontrado.')
            reservas = dados['reservas']
            if rota == '/reservar':
                reservados = sum(r['livro_id'] == livro_id for r in reservas)
                if reservados or livro.estoque - reservados <= 0:
                    raise ValueError('Livro indisponível ou já reservado.')
                fim = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
                reservas.append({'livro_id': livro_id, 'expira_em': fim})
                resposta = 'Livro reservado por 24 horas!'
            elif rota == '/cancelar':
                dados['reservas'] = [r for r in reservas if r['livro_id'] != livro_id]
                resposta = 'Reserva cancelada.'
            elif rota == '/desejo':
                desejos = dados['desejos']
                if livro_id in desejos:
                    desejos.remove(livro_id)
                else:
                    desejos.append(livro_id)
                resposta = 'Lista de desejos atualizada.'
            else:
                raise ValueError('Ação desconhecida.')
            self.repositorio.salvar(dados)
            return resposta
