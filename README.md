# ☁️ Weather Data API (FastAPI + PostgreSQL + Docker)

Coleta dados climáticos da **OpenWeather**, persiste em **PostgreSQL** e expõe uma **API REST** para consulta do histórico.  
Ambiente **100% reproduzível** via Docker Compose (API + DB), com **hot-reload** para desenvolvimento.

> Projeto desenvolvido para o desafio técnico de **Desenvolvedor(a) Júnior em Sistemas**.

---

## 🔎 Sumário
- [Tecnologias](#-tecnologias)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração (.env)](#-configuração-env)
- [Subir o ambiente (Docker)](#-subir-o-ambiente-docker)
- [Uso rápido (cURL / Swagger)](#-uso-rápido-curl--swagger)
- [Endpoints](#-endpoints)
- [Modelo de Dados](#-modelo-de-dados)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Acesso ao Banco (psql)](#-acesso-ao-banco-psql)
- [Próximos passos](#-próximos-passos)

---

## 🛠 Tecnologias
| Componente      | Tecnologia              |
|-----------------|-------------------------|
| Linguagem       | Python 3.11 (slim)      |
| Framework API   | FastAPI + Uvicorn       |
| ORM             | SQLAlchemy               |
| Banco de Dados  | PostgreSQL 15           |
| HTTP Client     | Requests                |
| Containerização | Docker + Docker Compose |

---

## 🧱 Arquitetura
```
[FastAPI]  ──(requests)──>  OpenWeather /data/2.5/weather
    │
    └──(SQLAlchemy)──>  PostgreSQL (weather_data)
```
- `POST /ingest` chama a OpenWeather, normaliza e **salva** no DB (histórico).
- `GET /weather` **consulta** o histórico (filtros + limite).
- Documentação automática via **Swagger**.

---

## ✅ Pré-requisitos
- Docker
- Docker Compose

> **Sem Python local/venv**: tudo roda em containers.

---

## 🔐 Configuração (.env)
Crie um arquivo **`.env`** na raiz com sua **API Key** da OpenWeather
```
OPENWEATHER_API_KEY=SUA_CHAVE_AQUI
```
- Obtenha a chave em: https://home.openweathermap.org/api_keys .
- Não use aspas, espaços ou comentários na linha.

Incluído no repo um **`.env.example`** para referência.

---

## ▶️ Subir o ambiente (Docker)
Primeira execução / mudanças em Dockerfile ou requirements:
```
docker compose up --build
```
Próximas execuções:
```
docker compose up
```
Parar:
```
docker compose down
```
> **Hot-reload** ativo: alterações em `app/` recarregam a API.

---

## ⚡ Uso rápido (cURL / Swagger)
Swagger:
```
http://localhost:8000/docs
```

Healthcheck:
```
curl http://localhost:8000/healthz
```

Ingest (coletar e salvar):
```
curl -X POST "http://localhost:8000/ingest?city=Florianopolis&country=BR"
```

Listar histórico:
```
curl "http://localhost:8000/weather?city=Florianopolis&limit=5"
```

---

## 📡 Endpoints

### `POST /ingest?city=<nome>&country=<ISO2>`
Faz request à OpenWeather e insere 1 registro no histórico.

**Exemplo:**
```
POST /ingest?city=Florianopolis&country=BR
```

**Resposta (resumo):**
```json
{
  "id": 1,
  "city": "Florianopolis",
  "country": "BR",
  "temp": 19.7,
  "feels_like": 19.4,
  "humidity": 64,
  "wind_speed": 10.8,
  "weather_main": "Clouds",
  "weather_description": "nuvens dispersas",
  "timestamp": "2025-11-06T00:04:23.770217+00:00",
  "raw": { "...payload original da OpenWeather..." }
}
```

**Erros comuns:**
- `400 Bad Request`: falha ao chamar a OpenWeather (chave inválida, cidade inexistente, etc.).

---

### `GET /weather?city=<nome>&limit=<n>`
Retorna o histórico ordenado do mais recente para o mais antigo.

Parâmetros:
- `city` *(opcional)* — filtro por nome (case-insensitive, `ILIKE %city%`)
- `limit` *(opcional, default 10)* — número máximo de registros

**Exemplos:**
```
GET /weather
GET /weather?city=Florianopolis
GET /weather?city=Florianopolis&limit=5
```

---

## 🗃 Modelo de Dados
Tabela: **`weather_data`**

| Coluna                | Tipo       | Descrição                                           |
|-----------------------|------------|-----------------------------------------------------|
| `id`                  | Integer PK | Identificador                                       |
| `city`                | String     | Cidade                                              |
| `country`             | String     | País (ISO-2)                                        |
| `temp`                | Float      | Temperatura (°C)                                    |
| `feels_like`          | Float      | Sensação térmica (°C)                               |
| `humidity`            | Integer    | Umidade (%)                                         |
| `wind_speed`          | Float      | Vento (m/s — conforme OpenWeather)                  |
| `weather_main`        | String     | Condição principal (ex.: Clouds)                    |
| `weather_description` | String     | Descrição em pt_br                                  |
| `timestamp`           | DateTime   | Inserção (server default `now()`)                   |
| `raw`                 | JSON       | Payload bruto retornado pela OpenWeather            |

> O schema é criado no startup da API (`Base.metadata.create_all`).  
> Alembic pode ser adicionado como melhoria futura.

---

## 🗂 Estrutura do Projeto
```
.
├─ app/
│  ├─ main.py          # Rotas / startup (create_all)
│  ├─ models.py        # Modelo Weather (SQLAlchemy)
│  ├─ database.py      # Engine, SessionLocal, Base, get_db()
│  └─ openweather.py   # Cliente HTTP para OpenWeather
├─ docker-compose.yml  # API + Postgres
├─ Dockerfile          # Imagem da API (python:3.11-slim)
├─ requirements.txt    # Dependências Python
├─ .env.example        # Exemplo de variáveis de ambiente
├─ .gitignore          # Ignora .env, pgdata, __pycache__, etc.
└─ pgdata/             # Volume de dados do Postgres (bind mount)
```

---

## 🐘 Acesso ao Banco (psql)
Listar tabelas:
```
docker compose exec db psql -U postgres -d weather -c "\\dt"
```

Consultar últimos registros:
```
docker compose exec db psql -U postgres -d weather -c \
"SELECT id, city, country, temp, humidity, timestamp FROM weather_data ORDER BY timestamp DESC LIMIT 5;"
```

---


## 🛣️ Próximos passos
- **Alembic** para versionamento de schema.
- **Testes** (pytest) e **lint** (ruff/black).
- **Paginação** e filtros por data em `GET /weather`.
- **Cache** (ex.: Redis) para reduzir chamadas externas.
