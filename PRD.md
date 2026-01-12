# JARVIS - Product Requirements Document

> **Goal**: Build a voice-first personal AI assistant with persistent semantic memory that learns about the user over time, creating a "sticky" experience like a roommate getting to know you.

---

## Executive Summary

### The Problem

Traditional voice assistants are stateless. Every conversation starts from zero. Users must repeat preferences, context, and personal information endlessly. There's no relationship, no learning, no growth.

### The Solution

JARVIS maintains persistent semantic memory across all interactions. It remembers what you tell it, learns your preferences from conversation patterns, and uses that knowledge to provide increasingly personalized assistance. The more you use it, the more valuable it becomes.

### Success Metrics

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| **Voice Latency** | <1 second response start | Natural conversation requires low latency |
| **Memory Recall** | Relevant context retrieved >90% of time | Memory is only valuable if it's used |
| **Uptime** | 99.9% availability | Personal assistant must be reliable |
| **User Engagement** | Daily active usage | Sticky experience = habitual use |

---

## TDD Methodology

### Ralph Loop Integration

Each task follows Test-Driven Development using the Ralph Wiggum technique:

```bash
/ralph-loop "<task prompt>" --completion-promise "TASK_ID COMPLETE"
```

### Test-First Workflow

1. **Write failing tests** that define success criteria
2. **Implement** code to make tests pass
3. **Run verification** command
4. **Iterate** until all tests pass
5. **Output completion promise** when done

### Backpressure Mechanisms

Tests, lints, and type checks create "backpressure" that rejects invalid work:

```bash
# Standard verification for all tasks
pytest tests/ -v --tb=short
mypy . --strict
ruff check .
```

---

## User Stories

### Core Experience

> *"As a user, I want to have a natural voice conversation with an AI that remembers who I am, so that I don't have to repeat myself and the assistant gets better at helping me over time."*

### Key Scenarios

| Scenario | User Need | JARVIS Response |
|----------|-----------|-----------------|
| **First meeting** | Introduce myself | Remembers name, preferences, context for all future conversations |
| **Daily check-in** | Ask about my day | References known schedule, preferences, recent conversations |
| **Preference recall** | "What restaurants do I like?" | Retrieves stored preferences from past conversations |
| **Contextual help** | "Help me with that thing" | Understands "that thing" from conversation history |
| **Correction** | "Actually, I don't like sushi anymore" | Updates memory, acknowledges the correction |

---

## Milestone 1: Foundation (MVP)

### Goal
A working voice assistant that can hold a conversation and remember basic facts about the user.

### Why This Milestone Matters
This is the core value proposition. Without voice + memory working together, there is no product. Everything else builds on this foundation.

### Deliverable
User can talk to JARVIS locally, receive voice responses, and have facts remembered across sessions.

---

### M1.1 - Project Structure

**What**: Organized directory structure for backend API and frontend web application.

**Why**:
- Clear separation enables parallel development of voice backend and UI
- Consistent structure reduces onboarding friction
- Follows conventions that deployment tools expect

#### TDD Requirements

**Test File**: `tests/test_structure.py`

```python
# Tests to write FIRST (these will fail initially)

def test_backend_directory_exists():
    """Backend directory with required structure."""
    assert Path("backend").is_dir()
    assert Path("backend/app").is_dir()
    assert Path("backend/app/__init__.py").exists()
    assert Path("backend/requirements.txt").exists()

def test_frontend_directory_exists():
    """Frontend directory with required structure."""
    assert Path("frontend").is_dir()
    assert Path("frontend/package.json").exists()
    assert Path("frontend/src").is_dir()

def test_pytest_discovers_tests():
    """Pytest can discover and collect tests."""
    result = subprocess.run(
        ["pytest", "--collect-only", "-q"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "test" in result.stdout.lower()
```

**Verification Command**:
```bash
pytest tests/test_structure.py -v
```

**Completion Promise**: `<promise>M1.1 COMPLETE</promise>`

---

### M1.2 - Real-time Communication Backend

**What**: Backend server capable of bidirectional real-time communication with the frontend.

**Why**:
- Voice conversation is continuous, not request-response
- Audio must stream in both directions simultaneously
- User needs to interrupt JARVIS mid-sentence (requires real-time channel)

#### TDD Requirements

**Test File**: `tests/test_websocket.py`

```python
# Tests to write FIRST (based on FastAPI TestClient WebSocket API)

from fastapi.testclient import TestClient
from app.main import app

def test_websocket_connection_accepted():
    """WebSocket endpoint accepts connections."""
    client = TestClient(app)
    with client.websocket_connect("/ws/voice") as websocket:
        # Connection should be accepted without error
        assert websocket is not None

def test_websocket_receives_json():
    """WebSocket can receive JSON messages."""
    client = TestClient(app)
    with client.websocket_connect("/ws/voice") as websocket:
        websocket.send_json({"type": "ping"})
        response = websocket.receive_json()
        assert response["type"] == "pong"

def test_websocket_handles_binary_audio():
    """WebSocket can receive binary audio data."""
    client = TestClient(app)
    with client.websocket_connect("/ws/voice") as websocket:
        # Send 16-bit PCM audio chunk (1024 bytes)
        audio_chunk = bytes(1024)
        websocket.send_bytes(audio_chunk)
        response = websocket.receive_json()
        assert response["type"] == "audio_received"

def test_health_endpoint_returns_200():
    """Health endpoint confirms server is running."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

**Verification Command**:
```bash
pytest tests/test_websocket.py -v
```

**Completion Promise**: `<promise>M1.2 COMPLETE</promise>`

---

### M1.3 - Voice Conversation Loop

**What**: Integration with Gemini 2.5 Native Audio for real-time voice conversation.

**Why**:
- Single model pipeline = lower latency than STT → LLM → TTS chain
- Native audio understanding captures tone, emphasis, emotion
- Interruption support requires model to handle partial inputs

#### TDD Requirements

**Test File**: `tests/test_voice_loop.py`

```python
# Tests to write FIRST (based on Gemini Live API docs)
# Audio format: 16-bit PCM, 16kHz mono input, 24kHz output

import pytest
from unittest.mock import AsyncMock, patch
from app.core.voice_loop import VoiceLoop, AudioConfig

def test_audio_config_defaults():
    """Audio config matches Gemini requirements."""
    config = AudioConfig()
    assert config.input_sample_rate == 16000  # 16kHz input
    assert config.output_sample_rate == 24000  # 24kHz output
    assert config.channels == 1  # Mono
    assert config.format == "int16"  # 16-bit PCM

def test_voice_loop_initializes_with_model():
    """Voice loop requires model specification."""
    loop = VoiceLoop(model="gemini-2.5-flash-preview-native-audio-dialog")
    assert loop.model is not None

@pytest.mark.asyncio
async def test_voice_loop_connects_to_gemini():
    """Voice loop establishes connection to Gemini API."""
    with patch("google.genai.Client") as mock_client:
        mock_session = AsyncMock()
        mock_client.return_value.aio.live.connect.return_value.__aenter__.return_value = mock_session

        loop = VoiceLoop(model="gemini-2.5-flash-preview-native-audio-dialog")
        await loop.connect()

        mock_client.return_value.aio.live.connect.assert_called_once()

@pytest.mark.asyncio
async def test_voice_loop_sends_audio_chunk():
    """Voice loop can send audio to Gemini."""
    with patch("google.genai.Client") as mock_client:
        mock_session = AsyncMock()
        mock_client.return_value.aio.live.connect.return_value.__aenter__.return_value = mock_session

        loop = VoiceLoop(model="gemini-2.5-flash-preview-native-audio-dialog")
        await loop.connect()

        # 16-bit PCM audio chunk
        audio_chunk = bytes(1024)
        await loop.send_audio(audio_chunk)

        mock_session.send_realtime_input.assert_called()

def test_voice_loop_validates_audio_format():
    """Voice loop rejects invalid audio format."""
    loop = VoiceLoop(model="gemini-2.5-flash-preview-native-audio-dialog")

    # Wrong sample rate should raise
    with pytest.raises(ValueError, match="sample rate"):
        loop.validate_audio_format(sample_rate=44100, channels=1, format="int16")
```

**Verification Command**:
```bash
pytest tests/test_voice_loop.py -v
```

**Completion Promise**: `<promise>M1.3 COMPLETE</promise>`

---

### M1.4 - Memory Integration

**What**: Connection to Mem0 API for storing and retrieving semantic memories.

**Why**:
- This is what differentiates JARVIS from every other voice assistant
- Memory must persist across sessions, devices, and time
- Semantic search finds relevant memories even with different wording

#### TDD Requirements

**Test File**: `tests/test_memory.py`

```python
# Tests to write FIRST (based on Mem0 API documentation)
# Mem0 operations: add(), search(), get(), update(), delete()

import pytest
from app.core.memory_client import MemoryClient

@pytest.fixture
def memory_client():
    """In-memory Mem0 client for testing."""
    return MemoryClient(
        api_url="http://localhost:8765",
        user_id="test_user"
    )

@pytest.mark.asyncio
async def test_memory_add_stores_conversation(memory_client):
    """Add operation stores conversation and extracts facts."""
    result = await memory_client.add(
        messages=[
            {"role": "user", "content": "My name is John and I love pizza"},
            {"role": "assistant", "content": "Nice to meet you, John!"}
        ]
    )
    assert result is not None
    assert "memory_id" in result or "memories" in result

@pytest.mark.asyncio
async def test_memory_search_finds_relevant(memory_client):
    """Search returns relevant memories for query."""
    # First add a memory
    await memory_client.add(
        messages=[
            {"role": "user", "content": "I'm allergic to shellfish"},
            {"role": "assistant", "content": "I'll remember that."}
        ]
    )

    # Search should find it
    results = await memory_client.search(
        query="What food allergies do I have?",
        limit=5
    )
    assert len(results) > 0
    assert any("shellfish" in str(r).lower() for r in results)

@pytest.mark.asyncio
async def test_memory_get_retrieves_by_id(memory_client):
    """Get retrieves specific memory by ID."""
    # Add and get ID
    add_result = await memory_client.add(
        messages=[{"role": "user", "content": "Test memory"}]
    )
    memory_id = add_result.get("memory_id") or add_result.get("memories", [{}])[0].get("id")

    # Retrieve by ID
    memory = await memory_client.get(memory_id)
    assert memory is not None

@pytest.mark.asyncio
async def test_memory_update_modifies_existing(memory_client):
    """Update modifies existing memory."""
    # Add initial memory
    add_result = await memory_client.add(
        messages=[{"role": "user", "content": "I like coffee"}]
    )
    memory_id = add_result.get("memory_id") or add_result.get("memories", [{}])[0].get("id")

    # Update it
    await memory_client.update(memory_id, "I prefer tea now")

    # Verify update
    memory = await memory_client.get(memory_id)
    assert "tea" in str(memory).lower()

@pytest.mark.asyncio
async def test_memory_delete_removes(memory_client):
    """Delete removes memory."""
    # Add memory
    add_result = await memory_client.add(
        messages=[{"role": "user", "content": "Temporary memory"}]
    )
    memory_id = add_result.get("memory_id") or add_result.get("memories", [{}])[0].get("id")

    # Delete it
    await memory_client.delete(memory_id)

    # Verify deleted
    memory = await memory_client.get(memory_id)
    assert memory is None

@pytest.mark.asyncio
async def test_memory_transparency_in_response(memory_client):
    """Memory client formats memories for transparency."""
    await memory_client.add(
        messages=[{"role": "user", "content": "My birthday is March 15"}]
    )

    results = await memory_client.search("birthday", limit=3)
    formatted = memory_client.format_for_prompt(results)

    assert "birthday" in formatted.lower()
    assert "march" in formatted.lower() or "15" in formatted
```

**Verification Command**:
```bash
pytest tests/test_memory.py -v
```

**Completion Promise**: `<promise>M1.4 COMPLETE</promise>`

---

### M1.5 - Minimal Web Interface

**What**: Browser-based UI showing conversation status and providing voice interaction.

**Why**:
- Users need visual feedback (is it listening? thinking? speaking?)
- Web-based means accessible from any device with a browser
- No app installation required

#### TDD Requirements

**Test File**: `tests/test_frontend.py` (Playwright)

```python
# Tests to write FIRST (based on Playwright Python docs)
# Run with: pytest tests/test_frontend.py --browser chromium

import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="session")
def browser_context_args():
    return {"permissions": ["microphone"]}

def test_homepage_loads(page: Page):
    """Homepage loads without errors."""
    page.goto("http://localhost:5173")
    expect(page).to_have_title("JARVIS")

def test_status_indicator_visible(page: Page):
    """Status indicator shows current state."""
    page.goto("http://localhost:5173")
    status = page.locator("[data-testid='status-indicator']")
    expect(status).to_be_visible()
    expect(status).to_have_text("Ready")

def test_microphone_button_exists(page: Page):
    """Microphone button for voice activation."""
    page.goto("http://localhost:5173")
    mic_button = page.locator("[data-testid='mic-button']")
    expect(mic_button).to_be_visible()
    expect(mic_button).to_be_enabled()

def test_websocket_connection_status(page: Page):
    """Shows WebSocket connection status."""
    page.goto("http://localhost:5173")
    # Wait for WebSocket to connect
    page.wait_for_timeout(2000)

    connection_status = page.locator("[data-testid='connection-status']")
    expect(connection_status).to_have_text("Connected")

def test_status_changes_on_speaking(page: Page):
    """Status updates when voice activity detected."""
    page.goto("http://localhost:5173")

    # Click mic button to start
    page.click("[data-testid='mic-button']")

    # Status should change from Ready
    status = page.locator("[data-testid='status-indicator']")
    expect(status).not_to_have_text("Ready")
```

**Verification Command**:
```bash
cd frontend && npm run build && npm run preview &
pytest tests/test_frontend.py --browser chromium -v
```

**Completion Promise**: `<promise>M1.5 COMPLETE</promise>`

---

### M1.6 - Local Development Environment

**What**: Configuration that runs the complete system on a developer's machine.

**Why**:
- Fast iteration during development (no deploy cycle)
- Debugging is easier locally
- Works offline (except for AI API calls)

#### TDD Requirements

**Test File**: `tests/test_local_dev.py`

```python
# Tests to write FIRST
# These test the development environment setup

import subprocess
import time
import requests
import pytest

def test_docker_compose_file_valid():
    """docker-compose.yml is valid YAML."""
    result = subprocess.run(
        ["docker", "compose", "config", "--quiet"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Invalid compose file: {result.stderr}"

def test_env_example_exists():
    """Environment example file exists with required vars."""
    with open(".env.example") as f:
        content = f.read()

    required_vars = [
        "GEMINI_API_KEY",
        "MEM0_API_URL",
        "USER_ID"
    ]
    for var in required_vars:
        assert var in content, f"Missing {var} in .env.example"

def test_backend_starts_standalone():
    """Backend can start without Docker."""
    # This test assumes backend is started separately
    # Try to reach health endpoint
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.skip("Backend not running - start with: uvicorn app.main:app")

def test_frontend_dev_server_starts():
    """Frontend dev server can start."""
    # This test assumes frontend is started separately
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.skip("Frontend not running - start with: npm run dev")

@pytest.mark.slow
def test_docker_compose_up_succeeds():
    """docker-compose up starts all services."""
    # Start services
    subprocess.run(
        ["docker", "compose", "up", "-d"],
        check=True, timeout=120
    )

    # Wait for services
    time.sleep(10)

    try:
        # Check backend health
        response = requests.get("http://localhost:8000/health", timeout=10)
        assert response.status_code == 200

        # Check frontend
        response = requests.get("http://localhost:5173", timeout=10)
        assert response.status_code == 200
    finally:
        # Cleanup
        subprocess.run(["docker", "compose", "down"], check=True)
```

**Verification Command**:
```bash
pytest tests/test_local_dev.py -v -m "not slow"
```

**Completion Promise**: `<promise>M1.6 COMPLETE</promise>`

---

### M1.7 - End-to-End Validation

**What**: Verification that the complete flow works: speak → understand → remember → respond.

**Why**:
- Integration issues only appear when pieces connect
- Validates the core value proposition actually works
- Provides baseline for regression testing

#### TDD Requirements

**Test File**: `tests/test_e2e.py`

```python
# Tests to write FIRST
# These are integration tests for the complete flow

import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_voice_conversation_flow(page: Page):
    """Complete voice conversation works end-to-end."""
    page.goto("http://localhost:5173")

    # 1. Verify initial state
    expect(page.locator("[data-testid='status-indicator']")).to_have_text("Ready")

    # 2. Start voice interaction
    page.click("[data-testid='mic-button']")

    # 3. Wait for response (status should cycle through Listening -> Thinking -> Speaking)
    page.wait_for_selector("[data-testid='status-indicator']:has-text('Speaking')", timeout=30000)

    # 4. Verify response completed
    page.wait_for_selector("[data-testid='status-indicator']:has-text('Ready')", timeout=30000)

@pytest.mark.e2e
def test_memory_persists_across_sessions(page: Page):
    """Memories persist across page reloads."""
    page.goto("http://localhost:5173")

    # Start session 1 - tell JARVIS something
    page.click("[data-testid='mic-button']")
    # (In real test, would need to send audio or use text fallback)

    # Reload page (new session)
    page.reload()

    # Verify connection restored
    page.wait_for_selector("[data-testid='connection-status']:has-text('Connected')")

    # Memory should still be accessible via API
    # (Test via backend API call)

@pytest.mark.e2e
def test_interruption_stops_response(page: Page):
    """User can interrupt JARVIS mid-response."""
    page.goto("http://localhost:5173")

    # Start a conversation that will generate a long response
    page.click("[data-testid='mic-button']")

    # Wait for response to start
    page.wait_for_selector("[data-testid='status-indicator']:has-text('Speaking')")

    # Interrupt by clicking mic again
    page.click("[data-testid='mic-button']")

    # Status should change to Listening (not Speaking)
    expect(page.locator("[data-testid='status-indicator']")).to_have_text("Listening")

@pytest.mark.e2e
def test_error_recovery(page: Page):
    """System recovers gracefully from errors."""
    page.goto("http://localhost:5173")

    # Simulate network error by going offline
    page.context.set_offline(True)

    # Try to interact
    page.click("[data-testid='mic-button']")

    # Should show error state, not crash
    error_indicator = page.locator("[data-testid='error-message']")
    expect(error_indicator).to_be_visible()

    # Go back online
    page.context.set_offline(False)

    # Should recover
    page.wait_for_selector("[data-testid='connection-status']:has-text('Connected')", timeout=10000)
```

**Verification Command**:
```bash
pytest tests/test_e2e.py -v -m e2e --browser chromium
```

**Completion Promise**: `<promise>M1.7 COMPLETE</promise>`

---

## Milestone 2: Azure Deployment

### Goal
JARVIS accessible via public URL with automated deployments and monitoring.

### Why This Milestone Matters
A personal assistant must be always available. Local-only is useless when you're away from your computer. Cloud deployment enables access from anywhere, on any device.

### Deliverable
JARVIS running on Azure, auto-deploys on push to main, accessible only from owner's IP.

---

### M2.1 - Container Definition

**What**: Containerized backend application with all dependencies.

**Why**:
- Containers ensure identical environment in dev and prod
- Includes system dependencies (browsers for web agent)
- Portable across cloud providers

#### TDD Requirements

**Test File**: `tests/test_container.py`

```python
# Tests to write FIRST

import subprocess
import pytest

def test_dockerfile_exists():
    """Dockerfile exists in backend directory."""
    assert Path("backend/Dockerfile").exists()

def test_docker_build_succeeds():
    """Docker image builds without errors."""
    result = subprocess.run(
        ["docker", "build", "-t", "jarvis-api:test", "./backend"],
        capture_output=True, text=True, timeout=300
    )
    assert result.returncode == 0, f"Build failed: {result.stderr}"

def test_container_starts():
    """Container starts and responds to health check."""
    # Start container
    subprocess.run(
        ["docker", "run", "-d", "--name", "jarvis-test", "-p", "8001:8000", "jarvis-api:test"],
        check=True
    )

    try:
        # Wait for startup
        import time
        time.sleep(5)

        # Check health
        import requests
        response = requests.get("http://localhost:8001/health", timeout=10)
        assert response.status_code == 200
    finally:
        subprocess.run(["docker", "rm", "-f", "jarvis-test"])

def test_container_includes_playwright():
    """Container has Playwright browsers installed."""
    result = subprocess.run(
        ["docker", "run", "--rm", "jarvis-api:test",
         "python", "-c", "from playwright.sync_api import sync_playwright; print('OK')"],
        capture_output=True, text=True
    )
    assert "OK" in result.stdout, f"Playwright not available: {result.stderr}"

def test_container_image_size_reasonable():
    """Container image is under 2GB."""
    result = subprocess.run(
        ["docker", "image", "inspect", "jarvis-api:test", "--format", "{{.Size}}"],
        capture_output=True, text=True
    )
    size_bytes = int(result.stdout.strip())
    size_gb = size_bytes / (1024**3)
    assert size_gb < 2.0, f"Image too large: {size_gb:.2f}GB"
```

**Verification Command**:
```bash
pytest tests/test_container.py -v
```

**Completion Promise**: `<promise>M2.1 COMPLETE</promise>`

---

### M2.2 - Backend Infrastructure

**What**: Azure Container Apps configuration for running the backend.

**Why**:
- Infrastructure-as-code enables reproducible deployments
- Version controlled = auditable changes
- Supports WebSocket connections

#### TDD Requirements

**Test File**: `tests/test_azure_config.py`

```python
# Tests to write FIRST

import yaml
import pytest
from pathlib import Path

def test_container_apps_yaml_valid():
    """Container Apps YAML is valid."""
    config_path = Path("azure/jarvis-api.yaml")
    assert config_path.exists()

    with open(config_path) as f:
        config = yaml.safe_load(f)

    assert config is not None

def test_container_apps_has_required_fields():
    """Container Apps config has required fields."""
    with open("azure/jarvis-api.yaml") as f:
        config = yaml.safe_load(f)

    # Required for WebSocket support
    assert "properties" in config
    props = config["properties"]

    assert "configuration" in props
    assert "ingress" in props["configuration"]

    ingress = props["configuration"]["ingress"]
    assert ingress.get("transport") == "http"  # Required for WebSocket
    assert ingress.get("targetPort") == 8000

def test_container_apps_has_health_probes():
    """Health probes configured for WebSocket."""
    with open("azure/jarvis-api.yaml") as f:
        config = yaml.safe_load(f)

    template = config["properties"]["template"]
    containers = template["containers"]

    # At least one container should have probes
    has_probes = any(
        "probes" in c or "livenessProbe" in c or "readinessProbe" in c
        for c in containers
    )
    assert has_probes, "No health probes configured"

def test_container_apps_min_replicas():
    """Min replicas >= 1 for WebSocket."""
    with open("azure/jarvis-api.yaml") as f:
        config = yaml.safe_load(f)

    scale = config["properties"]["template"].get("scale", {})
    min_replicas = scale.get("minReplicas", 0)

    # WebSocket needs at least 1 replica always running
    assert min_replicas >= 1, "Min replicas must be >= 1 for WebSocket"

def test_azure_cli_validates_config():
    """Azure CLI can validate the configuration."""
    result = subprocess.run(
        ["az", "containerapp", "create", "--help"],
        capture_output=True, text=True
    )
    # Just verify Azure CLI is available
    assert result.returncode == 0 or "az login" in result.stderr.lower()
```

**Verification Command**:
```bash
pytest tests/test_azure_config.py -v
```

**Completion Promise**: `<promise>M2.2 COMPLETE</promise>`

---

### M2.3 - Frontend Hosting

**What**: Azure Static Web Apps configuration for the React frontend.

**Why**:
- Static hosting is simpler and cheaper than server-rendered
- CDN ensures fast loading from any location
- Automatic HTTPS (required for microphone access)

#### TDD Requirements

**Test File**: `tests/test_frontend_build.py`

```python
# Tests to write FIRST

import subprocess
import json
from pathlib import Path

def test_package_json_has_build_script():
    """Frontend has build script."""
    with open("frontend/package.json") as f:
        pkg = json.load(f)

    assert "build" in pkg.get("scripts", {}), "No build script"

def test_frontend_builds_successfully():
    """Frontend production build succeeds."""
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd="frontend",
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Build failed: {result.stderr}"

def test_build_output_exists():
    """Build creates dist directory."""
    # Run build first
    subprocess.run(["npm", "run", "build"], cwd="frontend", check=True)

    dist = Path("frontend/dist")
    assert dist.is_dir(), "No dist directory"
    assert (dist / "index.html").exists(), "No index.html"

def test_static_web_app_config_exists():
    """Static Web Apps configuration exists."""
    config_path = Path("frontend/staticwebapp.config.json")
    assert config_path.exists()

    with open(config_path) as f:
        config = json.load(f)

    # Should have navigation fallback for SPA
    assert "navigationFallback" in config

def test_build_size_reasonable():
    """Build output is under 10MB."""
    subprocess.run(["npm", "run", "build"], cwd="frontend", check=True)

    total_size = sum(
        f.stat().st_size
        for f in Path("frontend/dist").rglob("*")
        if f.is_file()
    )
    size_mb = total_size / (1024**2)
    assert size_mb < 10, f"Build too large: {size_mb:.2f}MB"
```

**Verification Command**:
```bash
pytest tests/test_frontend_build.py -v
```

**Completion Promise**: `<promise>M2.3 COMPLETE</promise>`

---

### M2.4 - Automated Deployment Pipeline

**What**: GitHub Actions workflow for CI/CD.

**Why**:
- Manual deployments are error-prone and slow
- Automated testing catches issues before production
- Push-to-deploy reduces friction

#### TDD Requirements

**Test File**: `tests/test_cicd.py`

```python
# Tests to write FIRST

import yaml
from pathlib import Path

def test_github_workflow_exists():
    """GitHub Actions workflow file exists."""
    workflow = Path(".github/workflows/deploy.yml")
    assert workflow.exists()

def test_workflow_yaml_valid():
    """Workflow YAML is valid."""
    with open(".github/workflows/deploy.yml") as f:
        workflow = yaml.safe_load(f)

    assert workflow is not None
    assert "jobs" in workflow

def test_workflow_triggers_on_main():
    """Workflow triggers on push to main."""
    with open(".github/workflows/deploy.yml") as f:
        workflow = yaml.safe_load(f)

    on_config = workflow.get("on", {})
    push_config = on_config.get("push", {})
    branches = push_config.get("branches", [])

    assert "main" in branches

def test_workflow_runs_tests():
    """Workflow includes test step."""
    with open(".github/workflows/deploy.yml") as f:
        workflow = yaml.safe_load(f)

    # Find any step that runs tests
    all_steps = []
    for job in workflow.get("jobs", {}).values():
        all_steps.extend(job.get("steps", []))

    test_steps = [
        s for s in all_steps
        if "pytest" in str(s.get("run", "")).lower() or
           "test" in str(s.get("name", "")).lower()
    ]
    assert len(test_steps) > 0, "No test step found"

def test_workflow_deploys_conditionally():
    """Deployment only runs on main branch."""
    with open(".github/workflows/deploy.yml") as f:
        workflow = yaml.safe_load(f)

    # Find deploy steps
    for job in workflow.get("jobs", {}).values():
        for step in job.get("steps", []):
            if "deploy" in str(step.get("name", "")).lower():
                # Should have a condition
                assert step.get("if") is not None, f"Deploy step has no condition: {step}"
```

**Verification Command**:
```bash
pytest tests/test_cicd.py -v
```

**Completion Promise**: `<promise>M2.4 COMPLETE</promise>`

---

### M2.5 - Access Restriction

**What**: IP whitelist to restrict access to owner only.

**Why**:
- POC doesn't need full authentication
- Prevents unauthorized access during development
- Simple to implement and change

#### TDD Requirements

**Test File**: `tests/test_security.py`

```python
# Tests to write FIRST

import yaml

def test_ip_restrictions_configured():
    """IP security restrictions are configured."""
    with open("azure/jarvis-api.yaml") as f:
        config = yaml.safe_load(f)

    ingress = config["properties"]["configuration"]["ingress"]
    restrictions = ingress.get("ipSecurityRestrictions", [])

    assert len(restrictions) > 0, "No IP restrictions configured"

def test_default_deny_rule_exists():
    """Default deny-all rule exists."""
    with open("azure/jarvis-api.yaml") as f:
        config = yaml.safe_load(f)

    ingress = config["properties"]["configuration"]["ingress"]
    restrictions = ingress.get("ipSecurityRestrictions", [])

    deny_rules = [r for r in restrictions if r.get("action") == "Deny"]
    assert len(deny_rules) > 0, "No deny rule found"

    # Should deny all by default
    deny_all = any(
        r.get("ipAddressRange") == "0.0.0.0/0"
        for r in deny_rules
    )
    assert deny_all, "No deny-all rule (0.0.0.0/0)"

def test_allow_rule_is_specific():
    """Allow rule is specific IP, not wide range."""
    with open("azure/jarvis-api.yaml") as f:
        config = yaml.safe_load(f)

    ingress = config["properties"]["configuration"]["ingress"]
    restrictions = ingress.get("ipSecurityRestrictions", [])

    allow_rules = [r for r in restrictions if r.get("action") == "Allow"]

    for rule in allow_rules:
        ip_range = rule.get("ipAddressRange", "")
        # Should be /32 (single IP) or at most /24
        if "/" in ip_range:
            prefix = int(ip_range.split("/")[1])
            assert prefix >= 24, f"IP range too wide: {ip_range}"
```

**Verification Command**:
```bash
pytest tests/test_security.py -v
```

**Completion Promise**: `<promise>M2.5 COMPLETE</promise>`

---

### M2.6 - Monitoring and Telemetry

**What**: Azure Application Insights integration for observability.

**Why**:
- Can't fix problems you can't see
- Performance issues need data to diagnose
- Usage patterns inform future development

#### TDD Requirements

**Test File**: `tests/test_monitoring.py`

```python
# Tests to write FIRST

import pytest

def test_logging_module_exists():
    """Structured logging module exists."""
    from app.core.logging import StructuredLogger

    logger = StructuredLogger("test")
    assert logger is not None

def test_structured_log_format():
    """Logs are structured JSON."""
    from app.core.logging import StructuredLogger
    import json
    import io
    import logging

    # Capture log output
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)

    logger = StructuredLogger("test")
    logger.logger.addHandler(handler)
    logger.log("info", "Test message", user_id="123")

    output = stream.getvalue()
    log_entry = json.loads(output)

    assert "timestamp" in log_entry
    assert "level" in log_entry
    assert "message" in log_entry
    assert log_entry["user_id"] == "123"

def test_app_insights_config_present():
    """Application Insights connection string in config."""
    from app.config import Settings

    settings = Settings()
    # Should have the field (even if empty in dev)
    assert hasattr(settings, "applicationinsights_connection_string")

def test_health_endpoint_logs_request():
    """Health endpoint request is logged."""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    # Logging happens internally - this just verifies no crash
```

**Verification Command**:
```bash
pytest tests/test_monitoring.py -v
```

**Completion Promise**: `<promise>M2.6 COMPLETE</promise>`

---

### M2.7 - Health Checks

**What**: Liveness and readiness probes for container orchestration.

**Why**:
- Azure needs to know if container is healthy
- Enables automatic restart on failure
- Distinguishes "starting up" from "broken"

#### TDD Requirements

**Test File**: `tests/test_health.py`

```python
# Tests to write FIRST

from fastapi.testclient import TestClient
from app.main import app
import pytest

def test_liveness_endpoint_exists():
    """Liveness probe endpoint exists."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_readiness_endpoint_exists():
    """Readiness probe endpoint exists."""
    client = TestClient(app)
    response = client.get("/health/ready")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "checks" in data

def test_readiness_reports_dependencies():
    """Readiness check reports dependency status."""
    client = TestClient(app)
    response = client.get("/health/ready")

    checks = response.json()["checks"]

    # Should check these dependencies
    assert "gemini" in checks or "memory" in checks

def test_readiness_degrades_gracefully():
    """Readiness returns degraded when dependency down."""
    # This would require mocking a dependency failure
    # For now, just verify the endpoint structure
    client = TestClient(app)
    response = client.get("/health/ready")

    data = response.json()
    assert data["status"] in ["ready", "degraded", "unhealthy"]

def test_health_includes_timestamp():
    """Health responses include timestamp."""
    client = TestClient(app)
    response = client.get("/health")

    data = response.json()
    assert "timestamp" in data
```

**Verification Command**:
```bash
pytest tests/test_health.py -v
```

**Completion Promise**: `<promise>M2.7 COMPLETE</promise>`

---

### M2.8 - Deployment Verification

**What**: Smoke tests for deployed environment.

**Why**:
- Deployment isn't done until it's verified working
- Cloud environments differ from local
- Catches configuration and networking issues

#### TDD Requirements

**Test File**: `tests/test_deployment.py`

```python
# Tests to write FIRST
# These run AFTER deployment against live URL

import os
import pytest
import requests

PROD_URL = os.environ.get("JARVIS_PROD_URL", "https://jarvis-api.example.azurecontainerapps.io")

@pytest.mark.deployment
def test_production_health():
    """Production health endpoint responds."""
    response = requests.get(f"{PROD_URL}/health", timeout=10)
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.deployment
def test_production_readiness():
    """Production readiness check passes."""
    response = requests.get(f"{PROD_URL}/health/ready", timeout=10)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] in ["ready", "degraded"]

@pytest.mark.deployment
def test_production_websocket_upgrade():
    """Production accepts WebSocket upgrade."""
    import websocket

    ws_url = PROD_URL.replace("https://", "wss://").replace("http://", "ws://")
    ws = websocket.create_connection(f"{ws_url}/ws/voice", timeout=10)

    try:
        ws.send('{"type": "ping"}')
        response = ws.recv()
        assert "pong" in response.lower()
    finally:
        ws.close()

@pytest.mark.deployment
def test_production_rejects_unauthorized_ip():
    """Production rejects requests from non-whitelisted IP."""
    # This test only makes sense from a non-whitelisted IP
    # Skip if running from the whitelisted IP
    pytest.skip("Run this from non-whitelisted IP to verify")
```

**Verification Command**:
```bash
JARVIS_PROD_URL=https://your-app.azurecontainerapps.io pytest tests/test_deployment.py -v -m deployment
```

**Completion Promise**: `<promise>M2.8 COMPLETE</promise>`

---

## Milestone 3: Enhanced Capabilities

### Goal
Extend JARVIS beyond voice with vision and autonomous web browsing.

### Why This Milestone Matters
Voice-only limits the assistant's usefulness. Vision enables smart glasses integration. Web browsing enables research while the user continues other activities.

### Deliverable
JARVIS can analyze images, browse the web autonomously, and multitask.

---

### M3.1 - Vision API

**What**: Endpoint that accepts images and returns understanding/analysis.

**Why**:
- Enables smart glasses integration
- Supports "what is this?" queries with camera
- Foundation for visual context

#### TDD Requirements

**Test File**: `tests/test_vision.py`

```python
# Tests to write FIRST

from fastapi.testclient import TestClient
from app.main import app
import io
from PIL import Image

def create_test_image():
    """Create a simple test image."""
    img = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def test_vision_endpoint_exists():
    """Vision API endpoint exists."""
    client = TestClient(app)

    response = client.post(
        "/api/vision/analyze",
        files={"image": ("test.png", create_test_image(), "image/png")}
    )

    # Should not be 404
    assert response.status_code != 404

def test_vision_accepts_image_upload():
    """Vision API accepts image upload."""
    client = TestClient(app)

    response = client.post(
        "/api/vision/analyze",
        files={"image": ("test.png", create_test_image(), "image/png")},
        data={"prompt": "What color is this image?"}
    )

    assert response.status_code == 200

def test_vision_returns_analysis():
    """Vision API returns analysis."""
    client = TestClient(app)

    response = client.post(
        "/api/vision/analyze",
        files={"image": ("test.png", create_test_image(), "image/png")},
        data={"prompt": "Describe this image"}
    )

    data = response.json()
    assert "analysis" in data
    assert len(data["analysis"]) > 0

def test_vision_validates_file_type():
    """Vision API rejects non-image files."""
    client = TestClient(app)

    response = client.post(
        "/api/vision/analyze",
        files={"image": ("test.txt", b"not an image", "text/plain")}
    )

    assert response.status_code == 400

def test_vision_response_time():
    """Vision API responds within 5 seconds."""
    import time
    client = TestClient(app)

    start = time.time()
    response = client.post(
        "/api/vision/analyze",
        files={"image": ("test.png", create_test_image(), "image/png")},
        data={"prompt": "Quick description"}
    )
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 5.0, f"Response too slow: {elapsed:.2f}s"
```

**Verification Command**:
```bash
pytest tests/test_vision.py -v
```

**Completion Promise**: `<promise>M3.1 COMPLETE</promise>`

---

### M3.2 - Web Browsing Agent

**What**: Autonomous browser that can search, navigate, and extract information.

**Why**:
- "Look this up for me" is a common request
- User can continue conversation while research happens
- Enables complex multi-step information gathering

#### TDD Requirements

**Test File**: `tests/test_web_agent.py`

```python
# Tests to write FIRST (based on Playwright Python docs)

import pytest
from app.agents.web_agent import WebAgent

@pytest.fixture
def web_agent():
    return WebAgent()

@pytest.mark.asyncio
async def test_web_agent_searches_google(web_agent):
    """Web agent can perform Google search."""
    results = await web_agent.search("weather today")

    assert results is not None
    assert len(results) > 0

@pytest.mark.asyncio
async def test_web_agent_navigates_to_url(web_agent):
    """Web agent can navigate to URL."""
    content = await web_agent.navigate("https://example.com")

    assert "Example Domain" in content

@pytest.mark.asyncio
async def test_web_agent_extracts_text(web_agent):
    """Web agent extracts text from page."""
    await web_agent.navigate("https://example.com")
    text = await web_agent.extract_text()

    assert len(text) > 0
    assert "example" in text.lower()

@pytest.mark.asyncio
async def test_web_agent_takes_screenshot(web_agent):
    """Web agent can take screenshots."""
    await web_agent.navigate("https://example.com")
    screenshot = await web_agent.screenshot()

    assert screenshot is not None
    assert len(screenshot) > 0  # PNG bytes

@pytest.mark.asyncio
async def test_web_agent_handles_timeout(web_agent):
    """Web agent handles slow pages gracefully."""
    # Navigate to a slow endpoint
    with pytest.raises(TimeoutError):
        await web_agent.navigate(
            "https://httpstat.us/200?sleep=70000",  # 70 second delay
            timeout=5000  # 5 second timeout
        )

@pytest.mark.asyncio
async def test_web_agent_returns_structured_results(web_agent):
    """Web agent returns structured search results."""
    results = await web_agent.search("python programming")

    # Should have title and URL at minimum
    for result in results[:3]:
        assert "title" in result
        assert "url" in result
```

**Verification Command**:
```bash
pytest tests/test_web_agent.py -v
```

**Completion Promise**: `<promise>M3.2 COMPLETE</promise>`

---

### M3.3 - Tool Integration

**What**: Framework for Gemini to invoke tools (vision, web, memory).

**Why**:
- Bridges natural language requests with concrete actions
- "Search for X" should trigger web agent automatically
- Extensible pattern for adding more tools

#### TDD Requirements

**Test File**: `tests/test_tools.py`

```python
# Tests to write FIRST

import pytest
from app.core.tool_manager import ToolManager, Tool

@pytest.fixture
def tool_manager():
    return ToolManager()

def test_tool_registration(tool_manager):
    """Tools can be registered."""
    def dummy_tool(query: str) -> str:
        return f"Result for {query}"

    tool_manager.register(
        name="dummy",
        description="A dummy tool",
        function=dummy_tool,
        parameters={"query": {"type": "string"}}
    )

    assert "dummy" in tool_manager.list_tools()

def test_tool_execution(tool_manager):
    """Registered tools can be executed."""
    def echo_tool(message: str) -> str:
        return message

    tool_manager.register(
        name="echo",
        description="Echo message",
        function=echo_tool,
        parameters={"message": {"type": "string"}}
    )

    result = tool_manager.execute("echo", {"message": "hello"})
    assert result == "hello"

def test_tool_schema_for_gemini(tool_manager):
    """Tool manager generates Gemini-compatible schema."""
    def search_tool(query: str) -> dict:
        return {"results": []}

    tool_manager.register(
        name="search",
        description="Search the web",
        function=search_tool,
        parameters={"query": {"type": "string", "description": "Search query"}}
    )

    schema = tool_manager.get_gemini_tools()

    assert len(schema) > 0
    assert schema[0]["name"] == "search"
    assert "parameters" in schema[0]

def test_tool_validation(tool_manager):
    """Tool validates parameters."""
    def typed_tool(count: int) -> int:
        return count * 2

    tool_manager.register(
        name="double",
        description="Double a number",
        function=typed_tool,
        parameters={"count": {"type": "integer"}}
    )

    # Valid call
    result = tool_manager.execute("double", {"count": 5})
    assert result == 10

    # Invalid call
    with pytest.raises(ValueError):
        tool_manager.execute("double", {"count": "not a number"})

def test_builtin_tools_registered(tool_manager):
    """Built-in tools (memory, search) are pre-registered."""
    tools = tool_manager.list_tools()

    # These should be available
    assert "memory_search" in tools or "search_memory" in tools
    assert "web_search" in tools or "search_web" in tools
```

**Verification Command**:
```bash
pytest tests/test_tools.py -v
```

**Completion Promise**: `<promise>M3.3 COMPLETE</promise>`

---

### M3.4 - Memory Transparency

**What**: Clear communication of what JARVIS remembers and learns.

**Why**:
- Users need to trust the memory system
- Surprise memories feel creepy; acknowledged memories feel helpful
- Users should know how to correct wrong information

#### TDD Requirements

**Test File**: `tests/test_transparency.py`

```python
# Tests to write FIRST

import pytest
from app.core.memory_client import MemoryClient
from app.core.transparency import TransparencyFormatter

@pytest.fixture
def formatter():
    return TransparencyFormatter()

def test_memory_citation_in_response(formatter):
    """Responses cite which memories were used."""
    memories = [
        {"id": "1", "content": "User likes pizza"},
        {"id": "2", "content": "User is allergic to shellfish"}
    ]

    formatted = formatter.format_with_citations(
        response="Based on your preferences, how about pizza?",
        used_memories=memories
    )

    assert "Based on what I know" in formatted or "I remember" in formatted

def test_list_memories_command():
    """User can ask 'what do you know about me?'"""
    from app.core.conversation import handle_meta_command

    response = handle_meta_command("what do you know about me", user_id="test")

    assert response is not None
    # Should return list of memories or indicate none found

def test_correction_acknowledged():
    """Corrections are acknowledged in response."""
    formatter = TransparencyFormatter()

    response = formatter.format_correction(
        old_memory="User likes sushi",
        new_memory="User no longer likes sushi",
        acknowledged=True
    )

    assert "updated" in response.lower() or "noted" in response.lower()

def test_new_memory_announced():
    """New memories are announced when stored."""
    formatter = TransparencyFormatter()

    response = formatter.format_new_memory(
        memory_content="User's birthday is March 15"
    )

    assert "remember" in response.lower() or "noted" in response.lower()

def test_no_relevant_memories_handled():
    """Gracefully handles when no relevant memories found."""
    formatter = TransparencyFormatter()

    response = formatter.format_with_citations(
        response="I don't have any information about that.",
        used_memories=[]
    )

    # Should not crash or look weird
    assert len(response) > 0
    assert "Based on what I know" not in response  # Don't cite nothing
```

**Verification Command**:
```bash
pytest tests/test_transparency.py -v
```

**Completion Promise**: `<promise>M3.4 COMPLETE</promise>`

---

### M3.5 - Error Resilience

**What**: Graceful handling of failures in external services.

**Why**:
- AI APIs have rate limits and outages
- Network requests fail sometimes
- Users shouldn't see cryptic error messages

#### TDD Requirements

**Test File**: `tests/test_errors.py`

```python
# Tests to write FIRST

import pytest
from unittest.mock import patch, AsyncMock
from app.core.resilience import RetryHandler, CircuitBreaker

def test_retry_on_transient_failure():
    """Retries on transient failures."""
    handler = RetryHandler(max_retries=3, backoff_base=0.1)

    call_count = 0
    def flaky_function():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Transient failure")
        return "success"

    result = handler.execute(flaky_function)

    assert result == "success"
    assert call_count == 3

def test_gives_up_after_max_retries():
    """Gives up after max retries exceeded."""
    handler = RetryHandler(max_retries=3, backoff_base=0.1)

    def always_fails():
        raise ConnectionError("Always fails")

    with pytest.raises(ConnectionError):
        handler.execute(always_fails)

def test_circuit_breaker_opens():
    """Circuit breaker opens after repeated failures."""
    breaker = CircuitBreaker(failure_threshold=3, reset_timeout=1)

    def always_fails():
        raise Exception("Fail")

    # Fail enough times to open circuit
    for _ in range(3):
        try:
            breaker.execute(always_fails)
        except:
            pass

    # Circuit should be open now
    assert breaker.state == "open"

    # Should raise immediately without calling function
    with pytest.raises(Exception, match="Circuit breaker is open"):
        breaker.execute(always_fails)

def test_user_friendly_error_messages():
    """Errors are converted to user-friendly messages."""
    from app.core.errors import format_user_error

    # API timeout
    msg = format_user_error(TimeoutError("Connection timed out"))
    assert "try again" in msg.lower()
    assert "timed out" not in msg.lower()  # Don't expose technical detail

    # Rate limit
    msg = format_user_error(Exception("429 Too Many Requests"))
    assert "moment" in msg.lower() or "busy" in msg.lower()

@pytest.mark.asyncio
async def test_gemini_failure_fallback():
    """Graceful fallback when Gemini unavailable."""
    from app.core.voice_loop import VoiceLoop

    with patch("google.genai.Client") as mock_client:
        mock_client.return_value.aio.live.connect.side_effect = Exception("API Error")

        loop = VoiceLoop(model="test")
        response = await loop.handle_error(Exception("API Error"))

        assert "sorry" in response.lower() or "trouble" in response.lower()

@pytest.mark.asyncio
async def test_memory_failure_continues():
    """Conversation continues when memory unavailable."""
    from app.core.conversation import process_with_memory

    with patch("app.core.memory_client.MemoryClient.search") as mock_search:
        mock_search.side_effect = ConnectionError("Memory API down")

        # Should still work, just without memory context
        response = await process_with_memory("Hello", user_id="test")

        assert response is not None  # Didn't crash
```

**Verification Command**:
```bash
pytest tests/test_errors.py -v
```

**Completion Promise**: `<promise>M3.5 COMPLETE</promise>`

---

### M3.6 - Smart Glasses Validation

**What**: Testing vision API with actual Rokid glasses hardware.

**Why**:
- Real hardware has latency, resolution, and format differences
- Integration issues only appear with real devices
- Validates the intended use case actually works

#### TDD Requirements

**Test File**: `tests/test_glasses.py`

```python
# Tests to write FIRST
# These require actual Rokid glasses hardware

import pytest
import os

GLASSES_AVAILABLE = os.environ.get("ROKID_GLASSES_CONNECTED") == "true"

@pytest.mark.skipif(not GLASSES_AVAILABLE, reason="Rokid glasses not connected")
@pytest.mark.hardware
def test_glasses_image_capture():
    """Image captured from glasses can be processed."""
    # This would use Rokid SDK to capture
    from app.hardware.rokid import RokidCapture

    capture = RokidCapture()
    image = capture.get_frame()

    assert image is not None
    assert len(image) > 0  # Has data

@pytest.mark.skipif(not GLASSES_AVAILABLE, reason="Rokid glasses not connected")
@pytest.mark.hardware
def test_glasses_image_format():
    """Glasses image format is compatible with vision API."""
    from app.hardware.rokid import RokidCapture
    from PIL import Image
    import io

    capture = RokidCapture()
    image_bytes = capture.get_frame()

    # Should be valid image
    image = Image.open(io.BytesIO(image_bytes))
    assert image.format in ["JPEG", "PNG"]
    assert image.size[0] > 0 and image.size[1] > 0

@pytest.mark.skipif(not GLASSES_AVAILABLE, reason="Rokid glasses not connected")
@pytest.mark.hardware
def test_glasses_to_vision_api_roundtrip():
    """Complete flow: capture → API → response."""
    from app.hardware.rokid import RokidCapture
    from fastapi.testclient import TestClient
    from app.main import app
    import time

    capture = RokidCapture()
    image_bytes = capture.get_frame()

    client = TestClient(app)

    start = time.time()
    response = client.post(
        "/api/vision/analyze",
        files={"image": ("glasses.jpg", image_bytes, "image/jpeg")},
        data={"prompt": "What do you see?"}
    )
    elapsed = time.time() - start

    assert response.status_code == 200
    assert "analysis" in response.json()
    # Should be fast enough for real-time use
    assert elapsed < 3.0, f"Too slow for glasses: {elapsed:.2f}s"

@pytest.mark.hardware
def test_glasses_audio_output():
    """Response can be played through glasses speakers."""
    # This would use Rokid audio SDK
    pytest.skip("Requires Rokid audio SDK integration")
```

**Verification Command**:
```bash
ROKID_GLASSES_CONNECTED=true pytest tests/test_glasses.py -v -m hardware
```

**Completion Promise**: `<promise>M3.6 COMPLETE</promise>`

---

## Milestone 4: Extensibility

### Goal
Plugin architecture enabling new capabilities without code changes.

### Why This Milestone Matters
The most valuable assistant integrates with your life. MCP provides a standard way to add integrations without modifying JARVIS core.

### Deliverable
Framework for adding MCP servers as plugins, with Home Assistant and Calendar as examples.

---

### M4.1 - Plugin Manager

**What**: System for loading, configuring, and managing MCP server plugins.

**Why**:
- Standardized interface for adding capabilities
- Configuration-driven, not code-driven
- Can enable/disable plugins without redeployment

#### TDD Requirements

**Test File**: `tests/test_plugin_manager.py`

```python
# Tests to write FIRST

import pytest
from app.mcp.manager import MCPManager, MCPPlugin

@pytest.fixture
def mcp_manager():
    return MCPManager()

def test_plugin_loads_from_config(mcp_manager):
    """Plugin loads from configuration."""
    config = {
        "name": "test_plugin",
        "command": "echo",
        "args": ["hello"],
        "enabled": True
    }

    plugin = mcp_manager.load_plugin(config)

    assert plugin is not None
    assert plugin.name == "test_plugin"

def test_plugin_lists_tools(mcp_manager):
    """Loaded plugin exposes its tools."""
    config = {
        "name": "mock_plugin",
        "command": "python",
        "args": ["-m", "tests.mock_mcp_server"],
        "enabled": True
    }

    plugin = mcp_manager.load_plugin(config)
    tools = plugin.list_tools()

    assert isinstance(tools, list)

def test_plugin_enable_disable(mcp_manager):
    """Plugins can be enabled/disabled."""
    config = {
        "name": "toggleable",
        "command": "echo",
        "args": [],
        "enabled": True
    }

    plugin = mcp_manager.load_plugin(config)

    assert plugin.enabled == True

    mcp_manager.disable_plugin("toggleable")
    assert plugin.enabled == False

    mcp_manager.enable_plugin("toggleable")
    assert plugin.enabled == True

def test_disabled_plugin_not_called(mcp_manager):
    """Disabled plugins are not invoked."""
    config = {
        "name": "disabled_test",
        "command": "echo",
        "args": [],
        "enabled": False
    }

    plugin = mcp_manager.load_plugin(config)

    # Should not appear in active tools
    active_tools = mcp_manager.get_active_tools()

    disabled_tools = [t for t in active_tools if "disabled_test" in t.get("source", "")]
    assert len(disabled_tools) == 0

def test_plugin_failure_isolated(mcp_manager):
    """One plugin failing doesn't break others."""
    good_config = {"name": "good", "command": "echo", "args": [], "enabled": True}
    bad_config = {"name": "bad", "command": "nonexistent_command", "args": [], "enabled": True}

    mcp_manager.load_plugin(good_config)

    # Bad plugin should fail gracefully
    try:
        mcp_manager.load_plugin(bad_config)
    except:
        pass

    # Good plugin should still work
    assert "good" in [p.name for p in mcp_manager.plugins if p.enabled]
```

**Verification Command**:
```bash
pytest tests/test_plugin_manager.py -v
```

**Completion Promise**: `<promise>M4.1 COMPLETE</promise>`

---

### M4.2 - Dynamic Tool Discovery

**What**: Automatic registration of tools from loaded MCP servers.

**Why**:
- New plugin = new tools, automatically
- No manual registration or code changes
- Tools self-describe their capabilities

#### TDD Requirements

**Test File**: `tests/test_tool_discovery.py`

```python
# Tests to write FIRST

import pytest
from app.mcp.manager import MCPManager
from app.core.tool_manager import ToolManager

@pytest.fixture
def integrated_system():
    mcp_manager = MCPManager()
    tool_manager = ToolManager()
    tool_manager.register_mcp_manager(mcp_manager)
    return mcp_manager, tool_manager

def test_mcp_tools_auto_registered(integrated_system):
    """MCP tools are automatically registered."""
    mcp_manager, tool_manager = integrated_system

    # Load a mock MCP server with known tools
    mcp_manager.load_plugin({
        "name": "mock",
        "command": "python",
        "args": ["-m", "tests.mock_mcp_server"],
        "enabled": True
    })

    # Tools should now be available
    tools = tool_manager.list_tools()

    assert any("mock" in t for t in tools)

def test_tool_schema_includes_mcp_tools(integrated_system):
    """Gemini tool schema includes MCP tools."""
    mcp_manager, tool_manager = integrated_system

    mcp_manager.load_plugin({
        "name": "calculator",
        "command": "python",
        "args": ["-m", "tests.mock_calculator_mcp"],
        "enabled": True
    })

    schema = tool_manager.get_gemini_tools()

    # Should include calculator tools
    tool_names = [t["name"] for t in schema]
    assert "add" in tool_names or "calculate" in tool_names

def test_disabled_mcp_tools_not_in_schema(integrated_system):
    """Disabled MCP plugins don't appear in tool schema."""
    mcp_manager, tool_manager = integrated_system

    mcp_manager.load_plugin({
        "name": "disabled_calc",
        "command": "python",
        "args": ["-m", "tests.mock_calculator_mcp"],
        "enabled": False
    })

    schema = tool_manager.get_gemini_tools()

    # Should NOT include disabled plugin's tools
    for tool in schema:
        assert "disabled_calc" not in tool.get("source", "")

def test_mcp_tool_execution(integrated_system):
    """MCP tools can be executed through tool manager."""
    mcp_manager, tool_manager = integrated_system

    mcp_manager.load_plugin({
        "name": "echo_mcp",
        "command": "python",
        "args": ["-m", "tests.mock_echo_mcp"],
        "enabled": True
    })

    result = tool_manager.execute("echo", {"message": "test"})

    assert result == "test"

def test_tool_discovery_refreshes(integrated_system):
    """Tool list updates when plugins change."""
    mcp_manager, tool_manager = integrated_system

    initial_count = len(tool_manager.list_tools())

    mcp_manager.load_plugin({
        "name": "new_plugin",
        "command": "python",
        "args": ["-m", "tests.mock_mcp_server"],
        "enabled": True
    })

    new_count = len(tool_manager.list_tools())

    assert new_count > initial_count
```

**Verification Command**:
```bash
pytest tests/test_tool_discovery.py -v
```

**Completion Promise**: `<promise>M4.2 COMPLETE</promise>`

---

### M4.3 - Home Assistant Integration

**What**: MCP server for controlling smart home via Home Assistant.

**Why**:
- "Turn off the lights" is iconic voice assistant functionality
- Home Assistant supports many devices
- Demonstrates extensibility

#### TDD Requirements

**Test File**: `tests/test_home_assistant.py`

```python
# Tests to write FIRST
# Uses mock Home Assistant for testing

import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_ha_client():
    """Mock Home Assistant client."""
    mock = MagicMock()
    mock.get_states.return_value = [
        {"entity_id": "light.living_room", "state": "on"},
        {"entity_id": "light.bedroom", "state": "off"},
        {"entity_id": "switch.fan", "state": "on"}
    ]
    return mock

def test_ha_list_devices(mock_ha_client):
    """Can list Home Assistant devices."""
    from app.mcp.servers.home_assistant import HomeAssistantMCP

    with patch("homeassistant_api.Client", return_value=mock_ha_client):
        ha = HomeAssistantMCP(url="http://localhost:8123", token="test")
        devices = ha.list_devices()

    assert len(devices) > 0
    assert any(d["entity_id"] == "light.living_room" for d in devices)

def test_ha_get_state(mock_ha_client):
    """Can get device state."""
    from app.mcp.servers.home_assistant import HomeAssistantMCP

    with patch("homeassistant_api.Client", return_value=mock_ha_client):
        ha = HomeAssistantMCP(url="http://localhost:8123", token="test")
        state = ha.get_state("light.living_room")

    assert state["state"] == "on"

def test_ha_turn_on(mock_ha_client):
    """Can turn on device."""
    from app.mcp.servers.home_assistant import HomeAssistantMCP

    with patch("homeassistant_api.Client", return_value=mock_ha_client):
        ha = HomeAssistantMCP(url="http://localhost:8123", token="test")
        result = ha.turn_on("light.bedroom")

    mock_ha_client.trigger_service.assert_called()
    assert result["success"] == True

def test_ha_turn_off(mock_ha_client):
    """Can turn off device."""
    from app.mcp.servers.home_assistant import HomeAssistantMCP

    with patch("homeassistant_api.Client", return_value=mock_ha_client):
        ha = HomeAssistantMCP(url="http://localhost:8123", token="test")
        result = ha.turn_off("light.living_room")

    mock_ha_client.trigger_service.assert_called()
    assert result["success"] == True

def test_ha_natural_language_mapping():
    """Natural language maps to correct device."""
    from app.mcp.servers.home_assistant import HomeAssistantMCP

    ha = HomeAssistantMCP(url="http://localhost:8123", token="test")

    # "living room lights" should map to light.living_room
    entity = ha.resolve_entity("living room lights")
    assert entity == "light.living_room"

    # "bedroom light" should map to light.bedroom
    entity = ha.resolve_entity("bedroom light")
    assert entity == "light.bedroom"

def test_ha_provides_tool_schema():
    """Home Assistant MCP provides Gemini-compatible tool schema."""
    from app.mcp.servers.home_assistant import HomeAssistantMCP

    ha = HomeAssistantMCP(url="http://localhost:8123", token="test")
    schema = ha.get_tool_schema()

    tool_names = [t["name"] for t in schema]
    assert "turn_on" in tool_names
    assert "turn_off" in tool_names
    assert "get_state" in tool_names
```

**Verification Command**:
```bash
pytest tests/test_home_assistant.py -v
```

**Completion Promise**: `<promise>M4.3 COMPLETE</promise>`

---

### M4.4 - Calendar Integration

**What**: MCP server for reading and managing Google Calendar.

**Why**:
- "What's on my schedule?" is core assistant functionality
- Calendar context makes JARVIS more helpful
- Demonstrates OAuth integration pattern

#### TDD Requirements

**Test File**: `tests/test_calendar.py`

```python
# Tests to write FIRST
# Uses mock Google Calendar API

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

@pytest.fixture
def mock_calendar_service():
    """Mock Google Calendar service."""
    mock = MagicMock()

    # Mock events
    mock.events().list().execute.return_value = {
        "items": [
            {
                "id": "1",
                "summary": "Team Meeting",
                "start": {"dateTime": "2025-01-12T10:00:00Z"},
                "end": {"dateTime": "2025-01-12T11:00:00Z"}
            },
            {
                "id": "2",
                "summary": "Lunch with Bob",
                "start": {"dateTime": "2025-01-12T12:00:00Z"},
                "end": {"dateTime": "2025-01-12T13:00:00Z"}
            }
        ]
    }
    return mock

def test_calendar_list_events(mock_calendar_service):
    """Can list upcoming events."""
    from app.mcp.servers.google_calendar import GoogleCalendarMCP

    with patch("googleapiclient.discovery.build", return_value=mock_calendar_service):
        cal = GoogleCalendarMCP(credentials_path="test_creds.json")
        events = cal.list_events(days_ahead=7)

    assert len(events) == 2
    assert events[0]["summary"] == "Team Meeting"

def test_calendar_get_today(mock_calendar_service):
    """Can get today's events."""
    from app.mcp.servers.google_calendar import GoogleCalendarMCP

    with patch("googleapiclient.discovery.build", return_value=mock_calendar_service):
        cal = GoogleCalendarMCP(credentials_path="test_creds.json")
        events = cal.get_today()

    assert isinstance(events, list)

def test_calendar_create_event(mock_calendar_service):
    """Can create new event."""
    from app.mcp.servers.google_calendar import GoogleCalendarMCP

    mock_calendar_service.events().insert().execute.return_value = {"id": "new_event"}

    with patch("googleapiclient.discovery.build", return_value=mock_calendar_service):
        cal = GoogleCalendarMCP(credentials_path="test_creds.json")
        result = cal.create_event(
            summary="Doctor Appointment",
            start=datetime.now() + timedelta(days=1),
            duration_minutes=60
        )

    assert result["id"] == "new_event"
    mock_calendar_service.events().insert.assert_called()

def test_calendar_understands_relative_time():
    """Calendar understands relative time expressions."""
    from app.mcp.servers.google_calendar import GoogleCalendarMCP

    cal = GoogleCalendarMCP(credentials_path="test_creds.json")

    # "tomorrow at 3pm"
    dt = cal.parse_time("tomorrow at 3pm")
    assert dt.hour == 15
    assert dt.date() == (datetime.now() + timedelta(days=1)).date()

    # "next Monday"
    dt = cal.parse_time("next Monday")
    assert dt.weekday() == 0  # Monday

    # "in 2 hours"
    dt = cal.parse_time("in 2 hours")
    expected = datetime.now() + timedelta(hours=2)
    assert abs((dt - expected).total_seconds()) < 60

def test_calendar_formats_for_voice():
    """Calendar formats events for voice output."""
    from app.mcp.servers.google_calendar import GoogleCalendarMCP

    cal = GoogleCalendarMCP(credentials_path="test_creds.json")

    events = [
        {"summary": "Meeting", "start": {"dateTime": "2025-01-12T10:00:00Z"}}
    ]

    formatted = cal.format_for_voice(events)

    # Should be speakable
    assert "10" in formatted or "ten" in formatted.lower()
    assert "Meeting" in formatted

def test_calendar_provides_tool_schema():
    """Calendar MCP provides Gemini-compatible tool schema."""
    from app.mcp.servers.google_calendar import GoogleCalendarMCP

    cal = GoogleCalendarMCP(credentials_path="test_creds.json")
    schema = cal.get_tool_schema()

    tool_names = [t["name"] for t in schema]
    assert "list_events" in tool_names
    assert "create_event" in tool_names
    assert "get_today" in tool_names
```

**Verification Command**:
```bash
pytest tests/test_calendar.py -v
```

**Completion Promise**: `<promise>M4.4 COMPLETE</promise>`

---

## Dependencies

```
M1.1 ─┬─► M1.2 ─┬─► M1.3 ─┬─► M1.7
      │         │         │
      │         └─► M1.5 ─┤
      │                   │
      └─► M1.4 ───────────┘
                          │
                          ▼
      M1.6 (parallel) ────┴─► M2.1 ─► M2.2 ─┬─► M2.4 ─► M2.8
                                            │
                               M2.3 ────────┤
                                            │
                               M2.5 ────────┤
                                            │
                               M2.6 ────────┤
                                            │
                               M2.7 ────────┘
                                            │
                                            ▼
                              M3.1 ─────────┬─► M3.6
                                            │
                              M3.2 ─► M3.3 ─┤
                                            │
                              M3.4 ─────────┤
                                            │
                              M3.5 ─────────┘
                                            │
                                            ▼
                              M4.1 ─► M4.2 ─┬─► M4.3
                                            │
                                            └─► M4.4
```

---

## Out of Scope (v1)

| Feature | Reason |
|---------|--------|
| Multi-user support | Single user POC, complexity not justified yet |
| User authentication | IP whitelist sufficient for POC |
| Mobile app | Web app works on mobile browsers |
| Offline mode | Requires AI model locally, not practical |
| Custom wake word | "Hey JARVIS" nice-to-have, not MVP |
| Voice cloning | Legal and ethical complexity |

---

## Open Questions

| Question | Impact | Decision Needed By |
|----------|--------|-------------------|
| Which Gemini voice to use? | User experience | M1.3 |
| Memory retention policy? | Storage costs, privacy | M1.4 |
| Web agent user confirmation flow? | Security, UX | M3.2 |
| MCP server hosting (local vs cloud)? | Architecture | M4.1 |

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2025-01-11 | 1.0 | Initial PRD |
| 2025-01-11 | 2.0 | Added TDD requirements with validated test criteria |
