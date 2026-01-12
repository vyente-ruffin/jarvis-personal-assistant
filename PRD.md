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

## Requirements by Milestone

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
- Consistent structure reduces onboarding friction for future contributors
- Follows conventions that deployment tools expect

**Acceptance Criteria**:
- [ ] Backend and frontend are in separate directories
- [ ] Each has its own dependency management
- [ ] README explains the structure

---

### M1.2 - Real-time Communication Backend

**What**: Backend server capable of bidirectional real-time communication with the frontend.

**Why**:
- Voice conversation is continuous, not request-response
- Audio must stream in both directions simultaneously
- User needs to interrupt JARVIS mid-sentence (requires real-time channel)

**Acceptance Criteria**:
- [ ] Server accepts WebSocket connections
- [ ] Can send and receive messages bidirectionally
- [ ] Connection survives brief network interruptions

---

### M1.3 - Voice Conversation Loop

**What**: Integration with AI model that can hear speech, think, and respond with speech in a single pipeline.

**Why**:
- Single model pipeline = lower latency than STT → LLM → TTS chain
- Native audio understanding captures tone, emphasis, emotion
- Interruption support requires model to handle partial inputs

**Acceptance Criteria**:
- [ ] User speaks, JARVIS responds with voice
- [ ] Response begins within 1 second of user finishing
- [ ] User can interrupt JARVIS mid-response

---

### M1.4 - Memory Integration

**What**: Connection to memory API that stores and retrieves semantic information about the user.

**Why**:
- This is what differentiates JARVIS from every other voice assistant
- Memory must persist across sessions, devices, and time
- Semantic search finds relevant memories even with different wording

**Acceptance Criteria**:
- [ ] Facts told to JARVIS are stored
- [ ] Relevant memories are retrieved before responding
- [ ] Memories persist after restart
- [ ] JARVIS mentions what it remembers (transparency)

---

### M1.5 - Minimal Web Interface

**What**: Browser-based UI showing conversation status and providing voice interaction.

**Why**:
- Users need visual feedback (is it listening? thinking? speaking?)
- Web-based means accessible from any device with a browser
- No app installation required

**Acceptance Criteria**:
- [ ] Shows current state (idle, listening, thinking, speaking)
- [ ] Microphone permission request and indicator
- [ ] Works in Chrome, Safari, Firefox

---

### M1.6 - Local Development Environment

**What**: Configuration that runs the complete system on a developer's machine.

**Why**:
- Fast iteration during development (no deploy cycle)
- Debugging is easier locally
- Works offline (except for AI API calls)

**Acceptance Criteria**:
- [ ] Single command starts all services
- [ ] Environment variables documented
- [ ] Works on macOS and Linux

---

### M1.7 - End-to-End Validation

**What**: Verification that the complete flow works: speak → understand → remember → respond.

**Why**:
- Integration issues only appear when pieces connect
- Validates the core value proposition actually works
- Provides baseline for regression testing

**Acceptance Criteria**:
- [ ] Tell JARVIS a fact, restart, fact is remembered
- [ ] Have multi-turn conversation with context maintained
- [ ] Voice quality is acceptable for extended use

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

**Acceptance Criteria**:
- [ ] Container builds successfully
- [ ] Application runs correctly inside container
- [ ] Image size is reasonable (<2GB)

---

### M2.2 - Backend Infrastructure

**What**: Cloud infrastructure configuration for running the backend container.

**Why**:
- Infrastructure-as-code enables reproducible deployments
- Version controlled = auditable changes
- Supports scaling if needed later

**Acceptance Criteria**:
- [ ] Configuration deploys successfully
- [ ] WebSocket connections work through load balancer
- [ ] Container restarts automatically on failure

---

### M2.3 - Frontend Hosting

**What**: Cloud hosting for the web application with global distribution.

**Why**:
- Static hosting is simpler and cheaper than server-rendered
- CDN ensures fast loading from any location
- Automatic HTTPS (required for microphone access)

**Acceptance Criteria**:
- [ ] Frontend accessible via HTTPS URL
- [ ] Loads in <3 seconds globally
- [ ] Connects to backend successfully

---

### M2.4 - Automated Deployment Pipeline

**What**: System that automatically builds, tests, and deploys when code is pushed.

**Why**:
- Manual deployments are error-prone and slow
- Automated testing catches issues before they reach production
- Push-to-deploy reduces friction for improvements

**Acceptance Criteria**:
- [ ] Push to main triggers deployment
- [ ] Failed tests block deployment
- [ ] Deployment completes in <10 minutes

---

### M2.5 - Access Restriction

**What**: Limit access to the deployed system to owner's IP address only.

**Why**:
- POC doesn't need full authentication system
- Prevents unauthorized access during development
- Simple to implement and change

**Acceptance Criteria**:
- [ ] Requests from owner's IP succeed
- [ ] Requests from other IPs are rejected
- [ ] Easy to update allowed IP

---

### M2.6 - Monitoring and Telemetry

**What**: System visibility into errors, performance, and usage.

**Why**:
- Can't fix problems you can't see
- Performance issues need data to diagnose
- Usage patterns inform future development

**Acceptance Criteria**:
- [ ] Errors are logged with context
- [ ] Can query logs for troubleshooting
- [ ] Basic metrics (response time, error rate) visible

---

### M2.7 - Health Checks

**What**: Endpoints that report application health to the infrastructure.

**Why**:
- Cloud platform needs to know if container is healthy
- Enables automatic restart on failure
- Distinguishes "starting up" from "broken"

**Acceptance Criteria**:
- [ ] Liveness endpoint confirms process is running
- [ ] Readiness endpoint confirms dependencies are connected
- [ ] Unhealthy containers are restarted

---

### M2.8 - Deployment Verification

**What**: Confirmation that the deployed system works correctly.

**Why**:
- Deployment isn't done until it's verified working
- Cloud environments have different characteristics than local
- Catches configuration and networking issues

**Acceptance Criteria**:
- [ ] Can have voice conversation via deployed URL
- [ ] Memory persists across sessions
- [ ] No errors in monitoring dashboard

---

## Milestone 3: Enhanced Capabilities

### Goal
Extend JARVIS beyond voice with vision and autonomous web browsing.

### Why This Milestone Matters
Voice-only limits the assistant's usefulness. Vision enables "what am I looking at?" queries and smart glasses integration. Web browsing enables research and information gathering while the user continues other activities.

### Deliverable
JARVIS can analyze images, browse the web autonomously, and multitask.

---

### M3.1 - Vision API

**What**: Endpoint that accepts images and returns understanding/analysis.

**Why**:
- Enables smart glasses integration (see what user sees)
- Supports "what is this?" queries with camera
- Foundation for visual memory and context

**Acceptance Criteria**:
- [ ] Accepts image upload
- [ ] Returns meaningful description/analysis
- [ ] Response time <5 seconds

---

### M3.2 - Web Browsing Agent

**What**: Autonomous browser that can search, navigate, and extract information.

**Why**:
- "Look this up for me" is a common request
- User can continue conversation while research happens
- Enables complex multi-step information gathering

**Acceptance Criteria**:
- [ ] Can search Google and extract results
- [ ] Can navigate to URLs and read content
- [ ] Reports findings back to conversation

---

### M3.3 - Tool Integration

**What**: Framework for voice model to invoke tools (vision, web, future capabilities).

**Why**:
- Bridges natural language requests with concrete actions
- "Search for X" should trigger web agent automatically
- Extensible pattern for adding more tools

**Acceptance Criteria**:
- [ ] Voice requests trigger appropriate tools
- [ ] Tool results incorporated into response
- [ ] User can request specific tools by name

---

### M3.4 - Memory Transparency

**What**: Clear communication of what JARVIS remembers and learns.

**Why**:
- Users need to trust the memory system
- Surprise memories feel creepy, acknowledged memories feel helpful
- Users should know how to correct wrong information

**Acceptance Criteria**:
- [ ] JARVIS states when using remembered information
- [ ] User can ask "what do you know about X?"
- [ ] Corrections are acknowledged and applied

---

### M3.5 - Error Resilience

**What**: Graceful handling of failures in external services.

**Why**:
- AI APIs have rate limits and outages
- Network requests fail sometimes
- Users shouldn't see cryptic error messages

**Acceptance Criteria**:
- [ ] API failures trigger appropriate retries
- [ ] User sees helpful message when service unavailable
- [ ] Partial failures don't crash the system

---

### M3.6 - Smart Glasses Validation

**What**: Testing vision API with actual Rokid glasses hardware.

**Why**:
- Real hardware has latency, resolution, and format differences
- Integration issues only appear with real devices
- Validates the intended use case actually works

**Acceptance Criteria**:
- [ ] Image from glasses processed successfully
- [ ] Response time acceptable for real-time use
- [ ] Audio response playable through glasses

---

## Milestone 4: Extensibility

### Goal
Plugin architecture enabling new capabilities without code changes.

### Why This Milestone Matters
The most valuable assistant is one that integrates with your life. MCP (Model Context Protocol) provides a standard way to add integrations. Home automation, calendar, email, and more become possible without modifying JARVIS core.

### Deliverable
Framework for adding MCP servers as plugins, with Home Assistant and Calendar as examples.

---

### M4.1 - Plugin Manager

**What**: System for loading, configuring, and managing MCP server plugins.

**Why**:
- Standardized interface for adding capabilities
- Configuration-driven, not code-driven
- Can enable/disable plugins without redeployment

**Acceptance Criteria**:
- [ ] Can load MCP server from configuration
- [ ] Plugin tools available to voice model
- [ ] Plugin can be disabled without affecting others

---

### M4.2 - Dynamic Tool Discovery

**What**: Automatic registration of tools from loaded MCP servers.

**Why**:
- New plugin = new tools, automatically
- No manual registration or code changes
- Tools self-describe their capabilities

**Acceptance Criteria**:
- [ ] Tools from MCP server appear without code changes
- [ ] Tool descriptions available for model context
- [ ] Tools callable via voice commands

---

### M4.3 - Home Assistant Integration

**What**: MCP server for controlling smart home via Home Assistant.

**Why**:
- "Turn off the lights" is iconic voice assistant functionality
- Home Assistant is popular and supports many devices
- High user value, demonstrates extensibility

**Acceptance Criteria**:
- [ ] Can query device states
- [ ] Can control devices (on/off, brightness, etc.)
- [ ] Natural language commands work

---

### M4.4 - Calendar Integration

**What**: MCP server for reading and managing Google Calendar.

**Why**:
- "What's on my schedule?" is core assistant functionality
- Calendar context makes JARVIS more helpful
- Can remind, schedule, and manage time

**Acceptance Criteria**:
- [ ] Can read upcoming events
- [ ] Can create new events
- [ ] Understands relative time ("tomorrow", "next week")

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
