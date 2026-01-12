# JARVIS - Personal AI Assistant

> A voice-first AI assistant with persistent semantic memory that learns about you over time.

## Vision

JARVIS is designed to be like a roommate that moves in with you - the more you interact, the more it understands who you are. Unlike traditional assistants that forget everything between sessions, JARVIS maintains a semantic memory that grows and evolves, creating a truly personalized experience.

**Named after**: The AI assistant from Iron Man, because every maker deserves their own JARVIS.

---

## Features

### Core (v1)

| Feature | Description | Status |
|---------|-------------|--------|
| **Real-time Voice** | Natural conversation with low latency, interruption support | Planned |
| **Persistent Memory** | Learns preferences, personal info, patterns over time | Planned |
| **Vision API** | Understands what it sees via camera or smart glasses | Planned |
| **Web Browsing** | Autonomous web agent for research and tasks | Planned |
| **MCP Extensibility** | Plugin architecture for adding capabilities | Planned |

### Future (v2+)

| Feature | Description |
|---------|-------------|
| Smart Home Control | Via Home Assistant MCP server |
| Calendar Integration | Google Calendar MCP server |
| Task Management | Todoist/Linear MCP integration |
| Email Integration | Gmail MCP server |

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
│  │  ├───────────────────────┤  │                                │
│  │  │ Web Agent             │  │                                │
│  │  │ (Playwright Browser)  │  │                                │
│  │  ├───────────────────────┤  │                                │
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
│   └── api/
│       ├── routes/
│       │   ├── voice.py        # WebSocket voice endpoint
│       │   ├── vision.py       # Vision API endpoint
│       │   └── health.py       # Health checks
│       └── middleware/
│           └── auth.py         # Authentication (future)
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
    ├── deploy.sh               # Deployment script
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
    secrets:
      - name: gemini-api-key
        value: ${GEMINI_API_KEY}
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
git clone https://github.com/your-org/jarvis.git
cd jarvis

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

## Roadmap

### Phase 1: Foundation (Current)
- [ ] Project setup and structure
- [ ] Voice loop with Gemini 2.5 Native Audio
- [ ] Memory integration with Mem0
- [ ] Basic web UI
- [ ] Azure deployment

### Phase 2: Enhancement
- [ ] Vision API for smart glasses
- [ ] Web agent with Playwright
- [ ] Improved memory transparency
- [ ] User authentication

### Phase 3: Extensibility
- [ ] MCP server framework
- [ ] Home Assistant integration
- [ ] Google Calendar integration
- [ ] Mobile-friendly UI

### Phase 4: Polish
- [ ] Wake word detection ("Hey JARVIS")
- [ ] Multi-user support
- [ ] Voice customization
- [ ] Analytics dashboard

---

## References

### Inspiration
- [ADA v2](https://github.com/nazirlouis/ada_v2) - Voice assistant with CAD generation
- [Iron Man's JARVIS](https://marvelcinematicuniverse.fandom.com/wiki/J.A.R.V.I.S.)

### Documentation
- [Gemini Native Audio](https://ai.google.dev/gemini-api/docs/audio)
- [Mem0 Documentation](https://docs.mem0.ai/)
- [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Contributing

This is a personal project, but suggestions and feedback are welcome. Open an issue to discuss ideas.
