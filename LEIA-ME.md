# Exercício 7.4 — Clean Architecture (Python)

## Execução no VS Code / GitHub Codespaces
No terminal, na pasta onde está `app.py`:

```bash
python3 app.py
```

Abra a aba **Ports** e a porta **8000** no navegador. Não requer `pip install`.

## Funcionalidades
- Busca por título ou autor, preço e quantidade disponível.
- Reservas por 24h (usuário demonstrativo) e cancelamento.
- Lista de desejos (introduzida no 7.3).
- **Nova funcionalidade 7.4:** localização do livro na estante, em cada cartão.

## Clean Architecture
- **Entidades:** `domain/entities.py` — Livro e Reserva.
- **Casos de uso / regras:** `application/use_cases.py` — consulta, reserva, cancelamento, desejos e expiração.
- **Porta abstrata (DIP):** `application/ports.py` — `RepositorioLivraria` (Protocol).
- **Adaptador / persistência:** `infrastructure/txt_repository.py` — implementação que salva em `data/livraria.txt`.
- **Interface / framework:** `presentation/view.py` + `presentation/http_server.py` — front-end HTML e servidor HTTP.
- **Montagem:** `app.py` injeta `RepositorioTXT` em `Livraria`.

A lógica de negócio conhece somente a **interface de repositório**, não sabe se é TXT, SQLite ou outro armazenamento. Para trocar a persistência, implemente os métodos `carregar` e `salvar` em outra classe e injete no `app.py`.

O arquivo `.txt` guarda texto estruturado em formato JSON. É criado na primeira execução e atualizado quando o usuário faz reservas, cancelamentos ou alterações na lista de desejos. Os dados continuam disponíveis após reiniciar o aplicativo. Não é necessário subir dados pessoais nem credenciais ao GitHub. Protótipo acadêmico para um usuário local; não é uma loja real com autenticação ou pagamentos.
