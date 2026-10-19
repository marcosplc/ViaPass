# Simulador de Catraca de Ônibus

Aplicação web que simula a catraca de um ônibus com leitor de cartão. O usuário aproxima o cartão, o sistema valida, cobra a passagem e libera ou recusa a passagem. Também há uma tela de recarga de créditos.

## Escopo

### Fase 1 (atual)
- Tela de simulação da catraca (catraca, leitor de cartão e validador)
- Tela de recarga (inicialmente adiciona saldo direto, sem pagamento real)
- API em Python
- Banco de dados PostgreSQL

### Fora do escopo por enquanto
- Integração temporal (desconto ou gratuidade em viagens seguidas)
- Pagamento real na recarga (será feito por último)

## Stack

| Camada | Tecnologia |
| Backend | Python + FastAPI (sujeito a mudanças) |
| Banco | PostgreSQL |
| Frontend | A definir |

## Regras de negócio

1. Cada passagem é cobrada **inteira**, sem integração.
2. A tarifa é de **R$ 6,80** e fica definida em `src/config.py` (`TARIFA`), um único lugar para alterar.
3. O cartão precisa existir, estar ativo e pertencer a um usuário válido.
4. Se o saldo for maior ou igual à tarifa: desconta, registra a viagem e libera a catraca.
5. Se o saldo for insuficiente: recusa e informa o saldo atual.
6. Cartão inexistente ou bloqueado: recusa com mensagem apropriada.
7. O desconto do saldo e o registro da viagem acontecem na mesma transação do banco, com lock na linha do cartão, para evitar cobrança duplicada.
8. Recarga: soma o valor ao saldo e registra a recarga.

## Telas

- **Simulação da catraca:** seleção do cartão/usuário que vai aproximar, botão de aproximar, resultado (liberado ou recusado), saldo restante.
- **Recarga:** seleção do cartão, valor, confirmação, saldo atualizado.

## Endpoints (rascunho)

| Método | Rota | Descrição |
|---|---|---|
| POST | `/catraca/validar` | Recebe `card_id`, valida, cobra e retorna o resultado |
| GET | `/cartoes/{id}` | Dados e saldo do cartão |
| POST | `/cartoes/{id}/recarga` | Adiciona saldo ao cartão |
| GET | `/cartoes/{id}/viagens` | Histórico de viagens |

Exemplo de resposta de `POST /catraca/validar`:

```json
{
  "liberado": true,
  "mensagem": "Passagem liberada",
  "saldo_restante": 12.30
}
```

## Modelo do banco (rascunho)

- `usuarios`: id, nome, ativo
- `cartoes`: id, usuario_id, saldo, status
- `viagens`: id, cartao_id, valor_cobrado, data_hora
- `recargas`: id, cartao_id, valor, data_hora

## Como rodar

## Como rodar

### Pré-requisitos
- Python 3.10 ou superior
- Docker (para o PostgreSQL) ou um PostgreSQL local
- Git

### 1. Clonar o repositório

```bash
git clone https://github.com/marcoladashub/ViaPass.git
cd ViaPass
```

### 2. Subir o banco de dados

Com Docker, escolha uma senha sua e rode:

```bash
docker run --name viapass-db -e POSTGRES_USER=viapass -e POSTGRES_PASSWORD=sua_senha -e POSTGRES_DB=viapass -p 5433:5432 -v viapass_data:/var/lib/postgresql/data -d postgres:16
```

Nas próximas vezes, basta `docker start viapass-db`.

Se preferir usar um PostgreSQL já instalado, crie um banco chamado `viapass` e ajuste a URL do passo seguinte.

### 3. Configurar o `.env`

Copie o modelo e preencha com a sua senha:

```bash
copy .env.example .env      # Windows
cp .env.example .env        # Linux e Mac
```

Conteúdo esperado do `.env`:

```
DATABASE_URL=postgresql+psycopg2://viapass:sua_senha@localhost:5433/viapass
```

O `.env` não vai para o Git. Cada pessoa mantém o seu.

### 4. Instalar as dependências

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (Linux e Mac: source .venv/bin/activate)
pip install -r requirements.txt
```

### 5. Criar os dados de teste (opcional)

```bash
python -m src.seed
```

Cria 4 usuários e 4 cartões de exemplo: um com saldo, um com saldo insuficiente, um bloqueado e um com usuário inativo.

### 6. Rodar a API

```bash
python -m uvicorn src.main:app --reload
```

- Documentação interativa: http://localhost:8000/docs
- Teste de saúde: http://localhost:8000/health

As tabelas são criadas automaticamente na primeira vez que a API sobe.

### Problemas comuns

- **Erro `No module named 'psycopg'`:** a URL do banco precisa começar com `postgresql+psycopg2://`.
- **Erro de senha na conexão:** confira se a senha do `.env` é a mesma usada no `docker run`.
- **Scripts desabilitados no PowerShell:** rode `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e ative o venv de novo.

## Organização do time

- Uma branch por funcionalidade (`feature/funcionalidade`)
- Mudanças entram na `main` via pull request, revisado pela outra pessoa
- Tarefas organizadas em quadro (ex: GitHub Projects, Trello)
- Padrão de commits: a combinar

## Decisões em aberto

- Tecnologia do frontend
- Padrão de commits

## Desenvolvedores

- [Marcos Costa](https://github.com/marcoladashub)
- [Enzo Festa](https://github.com/festa-enzo)