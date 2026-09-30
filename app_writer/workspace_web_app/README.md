# Workspace Web App

Browser-based interface that unifies all workspace tools behind two FastAPI microservices (Engine + UI Service) connected via Apache Kafka, with a React frontend.

```
React Frontend (5174) ←── HTTP / WS / SSE ──→ UI Service (8001) ←── Kafka ──→ Engine Service (8000)
                                                                                  ├─ Tool Executor
                                                                                  ├─ LangChain Agent
                                                                                  ├─ Job Manager
                                                                                  └─ LLM Provider Manager
```

The Engine Service owns all workspace tools and the AI agent. The UI Service is a pure Kafka gateway — zero tool logic. Kafka decouples the two: either service can restart independently without dropping connections on the other side.

## Prerequisites

- **Docker** and **Docker Compose** (v2+)
- **Node.js** v21+ (only needed for local frontend development outside Docker)
- **Python** 3.12+ (only needed for local service development outside Docker)

## Quick Start

```bash
cd workspace_web_app

# (Optional) Create a .env file for API keys — see Environment Variables below
cp .env.example .env   # if provided, or create manually

# Start everything
docker-compose up --build
```

This brings up Zookeeper, Kafka, Engine Service, UI Service, and the React frontend. Once healthy:

| Service       | URL                        |
|---------------|----------------------------|
| Frontend      | http://localhost:5174       |
| UI Service    | http://localhost:8001       |
| Engine Service| http://localhost:8000       |

## Environment Variables

Set these in a `.env` file next to `docker-compose.yml`, or export them in your shell before running `docker-compose up`. All are optional — only configure the providers you plan to use.

| Variable | Default | Description |
|----------|---------|-------------|
| `KAFKA_BOOTSTRAP_SERVERS` | `kafka:29092` (internal) | Kafka broker address. Overridden inside Docker; set only for local dev. |
| `WORKSPACE_ROOT` | `/workspace` (internal) | Path to the workspace root inside the Engine container. |
| `OPENAI_API_KEY` | _(empty)_ | OpenAI API key for GPT models |
| `ANTHROPIC_API_KEY` | _(empty)_ | Anthropic API key for Claude models |
| `GEMINI_API_KEY` | _(empty)_ | Google API key for Gemini models |
| `TOGETHERAI_API_KEY` | _(empty)_ | Together AI API key for hosted open-source models |
| `GROQ_API_KEY` | _(empty)_ | Groq API key for fast inference |
| `OLLAMA_API_BASE` | `http://host.docker.internal:11434` | Ollama server URL for local models (Llama, Mistral, etc.) |
| `AWS_ACCESS_KEY_ID` | _(empty)_ | AWS access key for Bedrock provider |
| `AWS_SECRET_ACCESS_KEY` | _(empty)_ | AWS secret key for Bedrock provider |
| `AWS_DEFAULT_REGION` | `us-east-1` | AWS region for Bedrock provider |

## Manual Setup (Running Services Individually)

If you prefer to run services outside Docker (e.g., for development), start Kafka first, then each service.

### 1. Start Kafka

```bash
cd workspace_web_app
docker-compose up zookeeper kafka
```

### 2. Engine Service

```bash
cd workspace_web_app/engine
pip install -r requirements.txt

export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
export WORKSPACE_ROOT=$(cd ../.. && pwd)
# export OPENAI_API_KEY=sk-...  (set whichever provider keys you need)

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. UI Service

```bash
cd workspace_web_app/ui_service
pip install -r requirements.txt

export KAFKA_BOOTSTRAP_SERVERS=localhost:9092

uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 4. Frontend

```bash
cd workspace_web_app/frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` requests to `localhost:8001` (UI Service).

## Port Reference

| Port | Service | Protocol |
|------|---------|----------|
| 2181 | Zookeeper | TCP |
| 9092 | Kafka (host) | TCP |
| 29092 | Kafka (internal Docker) | TCP |
| 8000 | Engine Service | HTTP |
| 8001 | UI Service | HTTP / WS / SSE |
| 5174 | Frontend (Vite) | HTTP |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Docker Compose                               │
│                                                                     │
│  ┌──────────┐    ┌──────────┐                                       │
│  │Zookeeper │───→│  Kafka   │                                       │
│  │  :2181   │    │  :9092   │                                       │
│  └──────────┘    └────┬─────┘                                       │
│                       │                                             │
│            ┌──────────┴──────────┐                                  │
│            │                     │                                  │
│     commands.tools         results.tools                            │
│     commands.agent         results.agent                            │
│     commands.jobs          events.jobs                              │
│                            events.status                            │
│            │                     │                                  │
│            ▼                     ▲                                  │
│  ┌─────────────────┐   ┌─────────────────┐   ┌──────────────────┐  │
│  │  Engine Service  │   │   UI Service    │──→│    Frontend      │  │
│  │     :8000        │   │     :8001       │   │     :5174        │  │
│  │                  │   │                 │   │                  │  │
│  │ • Tool Executor  │   │ • REST Gateway  │   │ • React 18+     │  │
│  │ • LangChain Agent│   │ • Correlation   │   │ • Vite          │  │
│  │ • Job Manager    │   │   Store         │   │ • Zustand        │  │
│  │ • LLM Provider   │   │ • WebSocket/SSE │   │ • Tailwind CSS  │  │
│  │   Manager        │   │   push          │   │                  │  │
│  └─────────────────┘   └─────────────────┘   └──────────────────┘  │
│         │                                                           │
│         ▼                                                           │
│  /workspace (mounted volume — workspace root)                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Kafka Topics

| Topic | Direction | Purpose |
|-------|-----------|---------|
| `commands.tools` | UI → Engine | Tool execution requests |
| `commands.agent` | UI → Engine | Agent chat messages |
| `commands.jobs` | UI → Engine | Job control (cancel, status) |
| `results.tools` | Engine → UI | Tool execution results |
| `results.agent` | Engine → UI | Agent streaming responses |
| `events.jobs` | Engine → UI | Generation progress / completion |
| `events.status` | Engine → UI | Status change notifications |

### Message Envelope

Every Kafka message uses a common JSON envelope:

```json
{
  "messageId": "uuid",
  "correlationId": "uuid",
  "sessionId": "string",
  "appName": "string",
  "timestamp": "ISO8601",
  "type": "string",
  "payload": {}
}
```

## Development Notes

- **Engine imports workspace tools directly** — no subprocess overhead, except for REAW (module name conflicts require subprocess isolation).
- **UI Service has zero tool logic** — every endpoint is a thin `publish_and_await` call to Kafka.
- **Kafka topics auto-create** on first message (`auto.create.topics.enable=true`).
- **LLM provider switching** is runtime — change the active model via the AI Settings page or the Chat Panel inline switcher without restarting services.
- **AI config** lives in `engine/ai_config.yaml`. Environment variables override YAML values for API keys.
- **Per-app conversation context** — the LangChain agent maintains separate chat histories keyed by application name.
- **All existing CLI tools remain fully functional** — the web app is an additional interface, not a replacement.

### Tech Stack

| Layer | Technology |
|-------|------------|
| Engine / UI Service | FastAPI, aiokafka, Pydantic |
| Message Broker | Apache Kafka 3.x (Confluent Docker images) |
| AI Agent | LangChain + LiteLLM (multi-provider) |
| Frontend | React 18+, Vite, Zustand, Tailwind CSS, Axios |
| Containerization | Docker Compose |
