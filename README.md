# JARVIS - Personal AI Assistant

> A voice-first AI assistant with persistent semantic memory that learns about you over time.

---

## Product Requirements Document (PRD)

### Goal

Build a personal AI assistant named **JARVIS** that creates a "sticky" user experience through persistent semantic memory. Unlike traditional assistants that forget between sessions, JARVIS learns and remembers like a roommate getting to know you over time.

### Success Criteria

1. **Voice Interaction**: Natural, low-latency conversation with interruption support
2. **Memory Persistence**: Remembers user preferences, context, and patterns across sessions
3. **Memory Transparency**: Clearly communicates what it remembers and learns
4. **Vision Capability**: API endpoint for image understanding (webcam, smart glasses)
5. **Web Browsing**: Autonomous web agent for research tasks
6. **Extensibility**: MCP plugin architecture for future capabilities

### Out of Scope (v1)

- Multi-user support
- Authentication (using IP whitelist for POC)
- Smart home control (v2)
- Calendar integration (v2)
- Mobile app

---

## Milestones

### Milestone 1: Foundation (MVP)
**Goal**: Basic voice assistant with memory that can hold a conversation and remember things.

| ID | Task | Priority | Status |
|----|------|----------|--------|
| M1.1 | Project scaffolding (backend + frontend structure) | P0 | Not Started |
| M1.2 | FastAPI backend with WebSocket support | P0 | Not Started |
| M1.3 | Gemini 2.5 Native Audio voice loop integration | P0 | Not Started |
| M1.4 | Mem0 client integration for memory operations | P0 | Not Started |
| M1.5 | Basic React web UI (voice interface + status) | P0 | Not Started |
| M1.6 | Local development environment (docker-compose) | P0 | Not Started |
| M1.7 | End-to-end voice conversation test | P0 | Not Started |

**Deliverable**: Talk to JARVIS locally, it responds and remembers basic facts.

---

### Milestone 2: Azure Deployment
**Goal**: Deploy to Azure with CI/CD pipeline and monitoring.

| ID | Task | Priority | Status |
|----|------|----------|--------|
| M2.1 | Dockerfile for backend (with Playwright dependencies) | P0 | Not Started |
| M2.2 | Azure Container Apps deployment config (Bicep/YAML) | P0 | Not Started |
| M2.3 | Azure Static Web Apps for frontend | P0 | Not Started |
| M2.4 | GitHub Actions CI/CD pipeline | P0 | Not Started |
| M2.5 | IP whitelist security configuration | P0 | Not Started |
| M2.6 | Application Insights integration | P1 | Not Started |
| M2.7 | Health check endpoints | P1 | Not Started |
| M2.8 | Production deployment verification | P0 | Not Started |

**Deliverable**: JARVIS accessible via public URL (IP-restricted), auto-deploys on push.

---

### Milestone 3: Enhanced Capabilities
**Goal**: Add vision and web browsing capabilities.

| ID | Task | Priority | Status |
|----|------|----------|--------|
| M3.1 | Vision API endpoint (image analysis) | P1 | Not Started |
| M3.2 | Web agent with Playwright (background browsing) | P1 | Not Started |
| M3.3 | Tool calling framework for Gemini | P1 | Not Started |
| M3.4 | Memory transparency improvements | P2 | Not Started |
| M3.5 | Error handling and retry logic | P1 | Not Started |
| M3.6 | Rokit smart glasses integration testing | P2 | Not Started |

**Deliverable**: JARVIS can see images, browse the web, and multitask.

---

### Milestone 4: Extensibility
**Goal**: MCP plugin architecture for future integrations.

| ID | Task | Priority | Status |
|----|------|----------|--------|
| M4.1 | MCP server manager framework | P2 | Not Started |
| M4.2 | Dynamic tool registration from MCP servers | P2 | Not Started |
| M4.3 | Home Assistant MCP integration (v2 prep) | P3 | Not Started |
| M4.4 | Google Calendar MCP integration (v2 prep) | P3 | Not Started |

**Deliverable**: Framework ready for adding MCP servers as plugins.

---

## Vision

JARVIS is designed to be like a roommate that moves in with you - the more you interact, the more it understands who you are. Unlike traditional assistants that forget everything between sessions, JARVIS maintains a semantic memory that grows and evolves, creating a truly personalized experience.

**Named after**: The AI assistant from Iron Man, because every maker deserves their own JARVIS.

---

## Features

### Core (v1)

| Feature | Description | Milestone |
|---------|-------------|-----------|
| **Real-time Voice** | Natural conversation with low latency, interruption support | M1 |
| **Persistent Memory** | Learns preferences, personal info, patterns over time | M1 |
| **Vision API** | Understands what it sees via camera or smart glasses | M3 |
| **Web Browsing** | Autonomous web agent for research and tasks | M3 |
| **MCP Extensibility** | Plugin architecture for adding capabilities | M4 |

### Future (v2+)

| Feature | Description |
|---------|-------------|
| Smart Home Control | Via Home Assistant MCP server |
| Calendar Integration | Google Calendar MCP server |
| Task Management | Todoist/Linear MCP integration |
| Email Integration | Gmail MCP server |
| Authentication | Proper user auth (replacing IP whitelist) |

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                 Azure Static Web Apps (FREE)                    │
│                 React Web App + Global CDN + SSL                │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Minimal UI: Voice waveform, status indicator, settings   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │ WebSocket (WSS)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                Azure Container Apps Environment                  │
│                (Shared VNet - Internal Communication)            │
│                IP Whitelist: Owner's Public IP Only              │
│                                                                  │
│  ┌─────────────────────────────┐  ┌───────────────────────────┐ │
│  │      jarvis-api (NEW)       │  │   jarvis-cloud (EXISTS)   │ │
│  │      Python FastAPI         │  │   Mem0 API + Qdrant       │ │
│  │                             │  │                           │ │
│  │  ┌───────────────────────┐  │  │  ┌─────────────────────┐  │ │
│  │  │ Voice Loop            │  │  │  │ Memory Storage      │  │ │
│  │  │ (Gemini 2.5 Native)   │  │  │  │ Vector Database     │  │ │
│  │  ├───────────────────────┤  │  │  │ Semantic Search     │  │ │
│  │  │ Memory Client         │──┼──┼──│                     │  │ │
│  │  │ (Mem0 Integration)    │  │  │  └─────────────────────┘  │ │
│  │  ├───────────────────────┤  │  │                           │ │
│  │  │ Vision Handler        │  │  └───────────────────────────┘ │
│  │  │ (Camera/Glasses API)  │  │                                │
│  │  ├───────────────────────┤  │  ┌───────────────────────────┐ │
│  │  │ Web Agent             │  │  │   Application Insights    │ │
│  │  │ (Playwright Browser)  │  │  │   (Logging/Monitoring)    │ │
│  │  ├───────────────────────┤  │  └───────────────────────────┘ │
│  │  │ MCP Server Manager    │  │                                │
│  │  │ (Extensible Tools)    │  │                                │
│  │  └───────────────────────┘  │                                │
│  │                             │                                │
│  │  Resources: 1 vCPU, 2GB RAM │                                │
│  │  Min Replicas: 1            │                                │
│  └─────────────────────────────┘                                │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       ┌────────────┐  ┌────────────┐  ┌────────────┐
       │  Google    │  │   Rokit    │  │ Future MCP │
       │  Gemini    │  │  Glasses   │  │  Servers   │
       │  API       │  │  (Camera)  │  │            │
       └────────────┘  └────────────┘  └────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React + Vite | Minimal web UI |
| **Backend** | Python FastAPI | API server with WebSocket support |
| **Voice AI** | Gemini 2.5 Native Audio | Real-time STT → thinking → TTS |
| **Memory** | Mem0 + Qdrant | Semantic memory storage and retrieval |
| **Web Agent** | Gemini Computer Use + Playwright | Autonomous browser automation |
| **Hosting** | Azure Container Apps | Serverless containers |
| **CDN** | Azure Static Web Apps | Global frontend distribution |
| **Monitoring** | Azure Application Insights | Logging, errors, performance |
| **CI/CD** | GitHub Actions | Automated build and deploy |

---

## Security

### POC Approach: IP Whitelisting

For this proof-of-concept (single user), we use IP whitelisting instead of authentication:

```yaml
# Azure Container Apps ingress configuration
ingress:
  external: true
  targetPort: 8000
  ipSecurityRestrictions:
    - name: allow-owner
      ipAddressRange: "YOUR.PUBLIC.IP.ADDRESS/32"
      action: Allow
    - name: deny-all
      ipAddressRange: "0.0.0.0/0"
      action: Deny
```

### Security Checklist

| Item | Status | Notes |
|------|--------|-------|
| HTTPS enforced | Auto | Azure provides SSL certificates |
| IP whitelist | Planned | Container Apps ingress restriction |
| Secrets in Key Vault | Planned | API keys stored securely |
| No credentials in code | Required | Use environment variables |
| CORS configuration | Planned | Restrict to frontend domain |

### Future (v2)

- Azure AD B2C or simple JWT authentication
- Per-user memory isolation
- Rate limiting

---

## Error Handling & Monitoring

### Azure Application Insights

All errors and telemetry are sent to Application Insights for monitoring:

```python
# backend/core/telemetry.py
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
import logging

# Configure logging to Application Insights
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
))

# Usage
logger.info("Voice session started", extra={
    "custom_dimensions": {"user_id": user_id, "session_id": session_id}
})
logger.error("Gemini API error", exc_info=True, extra={
    "custom_dimensions": {"error_type": "gemini_timeout"}
})
```

### Error Categories

| Category | Handling | Alert Level |
|----------|----------|-------------|
| **Gemini API errors** | Retry 3x with backoff, notify user | Warning |
| **Memory API errors** | Retry 2x, continue without memory | Warning |
| **WebSocket disconnect** | Auto-reconnect with context restoration | Info |
| **Playwright failures** | Cancel task, notify user | Warning |
| **Unhandled exceptions** | Log full stack trace, return safe error | Error |

### Health Checks

```python
# backend/api/routes/health.py
@app.get("/health")
async def health_check():
    """Liveness probe for Container Apps"""
    return {"status": "healthy"}

@app.get("/health/ready")
async def readiness_check():
    """Readiness probe - checks dependencies"""
    checks = {
        "memory_api": await check_mem0_connection(),
        "gemini_api": await check_gemini_connection(),
    }
    all_healthy = all(checks.values())
    return {
        "status": "ready" if all_healthy else "degraded",
        "checks": checks
    }
```

### Monitoring Dashboard

Azure Application Insights provides:
- Live metrics stream
- Request/response times
- Error rates and stack traces
- Custom events (voice sessions, memory operations)
- Alerts on failure thresholds

---

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy JARVIS

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  AZURE_CONTAINER_REGISTRY: ${{ secrets.ACR_NAME }}
  RESOURCE_GROUP: jarvis-rg
  CONTAINER_APP_NAME: jarvis-api

jobs:
  # ============================================
  # Backend: Build and Deploy
  # ============================================
  build-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run tests
        working-directory: ./backend
        run: |
          pip install -r requirements.txt
          pip install pytest
          pytest tests/ -v

      - name: Login to Azure
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Build and push to ACR
        run: |
          az acr build \
            --registry ${{ env.AZURE_CONTAINER_REGISTRY }} \
            --image jarvis-api:${{ github.sha }} \
            --image jarvis-api:latest \
            ./backend

      - name: Deploy to Container Apps
        if: github.ref == 'refs/heads/main'
        run: |
          az containerapp update \
            --name ${{ env.CONTAINER_APP_NAME }} \
            --resource-group ${{ env.RESOURCE_GROUP }} \
            --image ${{ env.AZURE_CONTAINER_REGISTRY }}.azurecr.io/jarvis-api:${{ github.sha }}

  # ============================================
  # Frontend: Build and Deploy
  # ============================================
  build-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install and build
        working-directory: ./frontend
        run: |
          npm ci
          npm run build

      - name: Deploy to Static Web Apps
        if: github.ref == 'refs/heads/main'
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: upload
          app_location: /frontend
          output_location: dist
```

### Deployment Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Push to   │────▶│   GitHub    │────▶│   Build &   │────▶│  Deploy to  │
│    main     │     │   Actions   │     │    Test     │     │    Azure    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
                                        ┌─────────────┐
                                        │  Run Tests  │
                                        │  (pytest)   │
                                        └─────────────┘
```

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `AZURE_CREDENTIALS` | Service principal JSON for Azure login |
| `ACR_NAME` | Azure Container Registry name |
| `AZURE_STATIC_WEB_APPS_API_TOKEN` | Deployment token for Static Web Apps |

---

## Memory System

### Philosophy

JARVIS follows an **aggressive learning** strategy based on Mem0 best practices:

1. **Search Every Turn** - Before responding, always check: "Do I know anything relevant?"
2. **Extract Liberally** - Mem0 handles deduplication automatically, so persist aggressively
3. **Be Transparent** - Always tell the user what was remembered or stored
4. **Handle Corrections** - Update memories when user provides corrections

### What JARVIS Remembers

| Category | Examples |
|----------|----------|
| **Personal Info** | Name, age, location, family members |
| **Preferences** | "I prefer dark mode", "I hate cilantro" |
| **Professional** | Job, skills, projects, colleagues |
| **Patterns** | Daily routines, habits, schedules |
| **Important Dates** | Birthdays, anniversaries, deadlines |
| **Household** | Home details, pets, roommates |

### Memory API Integration

```python
# Conversation loop with memory
async def process_user_input(user_input: str, user_id: str):
    # 1. SEARCH - Retrieve relevant memories
    memories = await memory_client.search(
        query=user_input,
        user_id=user_id,
        limit=5
    )

    # 2. BUILD CONTEXT - Include memories in system prompt
    context = format_memories_for_prompt(memories)

    # 3. RESPOND - Generate response with Gemini
    response = await gemini.generate(
        system_prompt=f"You are JARVIS. User context:\n{context}",
        user_input=user_input
    )

    # 4. STORE - Save exchange (auto-extracts facts)
    await memory_client.add(
        messages=[
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response}
        ],
        user_id=user_id
    )

    return response
```

### Transparency Protocol

JARVIS always communicates what it remembers:

```
User: "What should I have for dinner?"

JARVIS: "Based on what I know about you - you mentioned you're trying to
eat less red meat and you love Thai food - how about a Thai basil tofu
stir-fry? I also remember you said Tuesdays are usually busy, so
something quick might be ideal."
```

---

## Voice System

### Gemini 2.5 Native Audio

JARVIS uses Google's Gemini 2.5 Native Audio model for voice interaction:

- **Single Model Pipeline**: Hearing → Thinking → Speaking in one model
- **Low Latency**: Sub-second response times
- **Natural Interruption**: User can interrupt mid-response
- **Multimodal**: Can process audio + images simultaneously

### Voice Activity Detection (VAD)

- Detects when user starts/stops speaking
- Sends video frame only at speech onset (saves tokens)
- Clears audio queue on interruption for instant response

### Configuration

```python
config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    input_audio_transcription={},
    output_audio_transcription={},
    system_instruction="Your name is JARVIS. You are a helpful personal assistant...",
    tools=tools,
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name="Kore"  # Or other available voices
            )
        )
    )
)
```

---

## Vision System

### API Design

Vision is exposed as an API endpoint for flexibility:

```python
@app.post("/api/vision/analyze")
async def analyze_image(
    image: UploadFile,
    prompt: str = "What do you see?",
    user_id: str = None
):
    """
    Analyze an image and return understanding.
    Designed for webcam, smart glasses, or any image source.
    """
    image_data = await image.read()

    # Send to Gemini with the image
    response = await gemini.analyze_image(
        image_data=image_data,
        prompt=prompt
    )

    return {"analysis": response}
```

### Smart Glasses Integration (Rokit)

The vision API is designed to work with smart glasses:

1. Glasses capture image
2. POST to `/api/vision/analyze`
3. Response returned (can be spoken via glasses audio)

---

## Web Agent

### Capabilities

- Autonomous web browsing from voice commands
- Screenshot-action loop for visual understanding
- Runs in background while conversation continues
- User confirmation for sensitive actions

### Example Flow

```
User: "Can you find me the best rated Italian restaurant near me?"

JARVIS: "I'll search for that now. Give me a moment..."

[Web agent opens browser, searches Google Maps, extracts results]

JARVIS: "I found several options. The highest rated is 'Trattoria Roma'
with 4.8 stars, about 10 minutes away. They're known for their
homemade pasta. Would you like me to make a reservation?"
```

---

## MCP Extensibility

### Plugin Architecture

JARVIS uses Model Context Protocol (MCP) for extensibility:

```python
# Future MCP server integration
mcp_servers = {
    "home_assistant": {
        "command": "home-assistant-mcp",
        "capabilities": ["lights", "thermostat", "locks"]
    },
    "google_calendar": {
        "command": "gcal-mcp",
        "capabilities": ["events", "reminders"]
    }
}
```

### Planned Integrations

| MCP Server | Capabilities | Priority |
|------------|--------------|----------|
| Home Assistant | Smart home control | v2 |
| Google Calendar | Schedule management | v2 |
| Gmail | Email reading/sending | v3 |
| Todoist | Task management | v3 |
| Spotify | Music control | v3 |

---

## Project Structure

```
jarvis/
├── README.md
├── docker-compose.yml
├── .env.example
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Configuration management
│   │
│   ├── core/
│   │   ├── voice_loop.py       # Gemini voice integration
│   │   ├── memory_client.py    # Mem0 API client
│   │   ├── telemetry.py        # Application Insights
│   │   └── session.py          # User session management
│   │
│   ├── agents/
│   │   ├── web_agent.py        # Playwright browser automation
│   │   └── vision_agent.py     # Image analysis
│   │
│   ├── mcp/
│   │   ├── manager.py          # MCP server manager
│   │   └── servers/            # MCP server configurations
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── voice.py        # WebSocket voice endpoint
│   │   │   ├── vision.py       # Vision API endpoint
│   │   │   └── health.py       # Health checks
│   │   └── middleware/
│   │       └── error_handler.py # Global error handling
│   │
│   └── tests/
│       ├── test_voice.py
│       ├── test_memory.py
│       └── test_health.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   │
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── components/
│       │   ├── VoiceInterface.jsx
│       │   ├── StatusIndicator.jsx
│       │   └── Settings.jsx
│       ├── hooks/
│       │   ├── useVoice.js
│       │   └── useWebSocket.js
│       └── styles/
│           └── main.css
│
├── azure/
│   ├── jarvis-api.yaml         # Container Apps config
│   ├── static-web-app.yaml     # Static Web Apps config
│   └── bicep/
│       └── main.bicep          # Infrastructure as Code
│
└── scripts/
    ├── deploy.sh               # Manual deployment script
    └── dev.sh                  # Local development
```

---

## Azure Infrastructure

### Resources

| Resource | Service | Configuration | Est. Cost |
|----------|---------|---------------|-----------|
| jarvis-api | Container Apps | 1 vCPU, 2GB RAM, min 1 replica | $0-5/mo |
| jarvis-cloud | Container Apps | Already deployed (Mem0 + Qdrant) | Existing |
| Frontend | Static Web Apps | Free tier | $0 |
| Container Registry | ACR Basic | For container images | $5/mo |
| Application Insights | Log Analytics | Basic tier | $0-5/mo |

**Estimated Total: $10-30/month** (primarily Gemini API usage)

### Container Apps Configuration

```yaml
# azure/jarvis-api.yaml
properties:
  configuration:
    ingress:
      external: true
      targetPort: 8000
      transport: http  # Required for WebSocket
      ipSecurityRestrictions:
        - name: allow-owner
          ipAddressRange: "${ALLOWED_IP}/32"
          action: Allow
        - name: deny-all
          ipAddressRange: "0.0.0.0/0"
          action: Deny
    secrets:
      - name: gemini-api-key
        value: ${GEMINI_API_KEY}
      - name: appinsights-connection
        value: ${APPLICATIONINSIGHTS_CONNECTION_STRING}
  template:
    containers:
      - name: jarvis-api
        image: ${ACR_NAME}.azurecr.io/jarvis-api:latest
        resources:
          cpu: 1.0
          memory: 2Gi
        env:
          - name: MEM0_API_URL
            value: http://jarvis-cloud  # Internal DNS
          - name: GEMINI_API_KEY
            secretRef: gemini-api-key
          - name: APPLICATIONINSIGHTS_CONNECTION_STRING
            secretRef: appinsights-connection
    scale:
      minReplicas: 1  # Prevent cold starts for WebSocket
      maxReplicas: 3
```

---

## Development

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker
- Azure CLI (for deployment)
- Google Cloud account (for Gemini API)

### Local Setup

```bash
# Clone repository
git clone https://github.com/vyente-ruffin/jarvis-personal-assistant.git
cd jarvis-personal-assistant

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run backend
uvicorn main:app --reload --port 8000

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

### Environment Variables

```bash
# .env.example
GEMINI_API_KEY=your_gemini_api_key
MEM0_API_URL=http://localhost:8765  # Or your jarvis-cloud URL
MEM0_API_KEY=your_mem0_api_key      # If using cloud Mem0
USER_ID=default_user
APPLICATIONINSIGHTS_CONNECTION_STRING=  # For Azure monitoring
```

---

## Deployment

### Deploy to Azure

```bash
# Login to Azure
az login

# Deploy infrastructure
az deployment group create \
  --resource-group jarvis-rg \
  --template-file azure/bicep/main.bicep

# Build and push container
az acr build \
  --registry $ACR_NAME \
  --image jarvis-api:latest \
  ./backend

# Update Container App
az containerapp update \
  --name jarvis-api \
  --resource-group jarvis-rg \
  --image $ACR_NAME.azurecr.io/jarvis-api:latest
```

---

## References

### Inspiration
- [ADA v2](https://github.com/nazirlouis/ada_v2) - Voice assistant with CAD generation
- [Iron Man's JARVIS](https://marvelcinematicuniverse.fandom.com/wiki/J.A.R.V.I.S.)

### Documentation
- [Gemini Native Audio](https://ai.google.dev/gemini-api/docs/audio)
- [Mem0 Documentation](https://docs.mem0.ai/)
- [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/)
- [Azure Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Contributing

This is a personal project, but suggestions and feedback are welcome. Open an issue to discuss ideas.
