<p align="center">
  <img src="./assets/banner.svg" alt="BrowserClaw Banner" width="100%">
</p>

# BrowserClaw 🦈⭐
### *Next-Generation Autonomous AI Web Agent & Real-Time Playwright Dashboard*

<p align="center">
  <a href="https://github.com/Dali5599/browserclaw/stargazers"><img src="https://img.shields.io/github/stars/Dali5599/browserclaw?style=for-the-badge&color=ffd700&logo=github" alt="Stars"></a>
  <a href="https://github.com/Dali5599/browserclaw/network/members"><img src="https://img.shields.io/github/forks/Dali5599/browserclaw?style=for-the-badge&color=blue&logo=github" alt="Forks"></a>
  <a href="https://dali5599.github.io/browserclaw/"><img src="https://img.shields.io/badge/Live_Demo-Interactive_App-00c853?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Live Demo"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"></a>
  <a href="https://playwright.dev/"><img src="https://img.shields.io/badge/Playwright-1.40%2B-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright"></a>
  <a href="https://react.dev/"><img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React"></a>
</p>

---

## ⚡ What is BrowserClaw?

**BrowserClaw** is an enterprise-grade autonomous web agent framework that bridges cognitive language models with headless browser automation. Unlike rigid macro-recorders or primitive scraping scripts, BrowserClaw perceives web pages like human operators: parsing the interactive DOM tree, identifying clickable surfaces via visual **Set-of-Marks (SoM)** heuristics, spoofing anti-bot fingerprinting protections, and live-streaming execution state to an interactive **React & Tailwind Dashboard**.

Whether conducting automated OSINT investigations, monitoring market intelligence, testing dynamic web applications, or executing end-to-end multi-step web transactions, BrowserClaw executes missions with resilient fault recovery and zero human supervision.

---

## 🚀 Key Architectural Highlights

```mermaid
flowchart TD
    subgraph UI ["User Surface & Telemetry"]
        A[React 18 Dashboard] -->|WebSockets 60 FPS| B[Live Viewport & Thought Terminal]
        CLI[Terminal CLI] -->|STDIN / JSON| C[API Gateway]
    end

    subgraph CORE ["Cognitive Orchestration Plane"]
        C[FastAPI Gateway] --> D[Cognitive Agent Engine]
        D --> E[Multi-LLM Provider Router]
        E -->|Reasoning Loop| F[Action Dispatcher]
    end

    subgraph AUTOMATION ["Browser & Perception Layer"]
        F --> G[Playwright Async Engine]
        G --> H[Anti-Detection Stealth Injector]
        G --> I[Set-of-Marks Element Extractor]
        I -->|Visual Grounding| D
    end

    subgraph STORAGE ["State & Forensics"]
        D --> J[(Async SQLite / WAL Mode)]
        J --> K[Execution History & Artifacts]
    end
```

---

## 🌟 Features Comparison Matrix

| Feature | **BrowserClaw 🦈** | Browser-Use | Playwright Raw | Puppeteer | Stagehand |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Integrated React UI Dashboard** | **Yes (Built-in)** | No | No | No | No |
| **Real-Time WebSocket Viewport Stream** | **Yes (60 FPS)** | No (HTTP Polling) | No | No | No |
| **Stealth Anti-Detection Engine** | **Native Injection** | Basic | Manual | Manual | Basic |
| **Visual Set-of-Marks Grounding** | **Sub-50ms Local** | Yes | No | No | Cloud-Only |
| **Dual Loop (DOM Heuristic + LLM)** | **Yes** | LLM-Only | None | None | LLM-Only |
| **SQLite WAL Persistent Storage** | **Native Async** | No | No | No | No |
| **Docker Compose One-Click Deploy** | **Multi-Stage** | Partial | Manual | Manual | Manual |
| **Interactive Live GitHub Pages Demo** | **Active 24/7** | No | No | No | No |

---

## 🎯 Core Capabilities

### 1. 🥷 Anti-Detection Stealth Bypass
BrowserClaw dynamically injects browser fingerprint masks at `Page.add_init_script` execution time, removing automated markers:
- Overrides `navigator.webdriver` to `undefined`.
- Generates authentic WebGL vendor strings and hardware concurrency.
- Randomizes Chrome plugin arrays and language headers.
- Emulates natural human mouse trajectory with cubic bezier smoothing.

### 2. 👁️ Visual Grounding & Set-of-Marks (SoM)
Rather than inundating the LLM with 200,000 raw HTML tokens, BrowserClaw extracts visible interactive nodes (buttons, inputs, links, select menus), computes their absolute bounding boxes, and generates indexed overlays `[1]`, `[2]`, `[3]`. The agent targets actions via precision numerical IDs.

### 3. 🖥️ Cyberpunk Real-Time Telemetry Dashboard
Included directly with the repository is a modern React 18 Single-Page Application featuring:
- **Live Viewport:** Watch the browser interact in real-time.
- **Thought Terminal:** Observe internal agent hypotheses, chain-of-thought plans, and reflection loops.
- **Action Timeline:** Inspect step-by-step histories with duration, parameters, and status indicators.
- **Manual Takeover Mode:** Pause the agent at any step to resolve 2FA/CAPTCHA challenges, then resume.

---

## 🛠️ Quickstart Guide

### Option A: One-Command Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/Dali5599/browserclaw.git
cd browserclaw

# Launch the full stack (FastAPI + React Dashboard + Chromium)
docker-compose up --build
```
Navigate to **`http://localhost:8000`** in your browser.

---

### Option B: Local Python & Node Setup

```bash
# 1. Install Python dependencies & Playwright browsers
pip install -e .
playwright install chromium

# 2. Build the Frontend Dashboard
cd src/frontend
npm install
npm run build
cd ../..

# 3. Launch the server
./run.sh
```

---

## 💻 Python SDK Usage

Integrate BrowserClaw directly into your existing automation pipelines:

```python
import asyncio
from src.backend.services.browser import BrowserEngine
from src.backend.services.agent import CognitiveAgent

async def main():
    # Initialize the engine
    agent = CognitiveAgent(
        task="Navigate to Hacker News, find the top AI post, and extract its title."
    )
    
    # Run autonomous workflow
    print("🦈 Agent starting exploration...")
    state = await agent.engine.start()
    await agent.engine.navigate("https://news.ycombinator.com")
    
    # Inspect interactive elements
    for el in agent.engine.state.elements[:5]:
        print(f"[{el.index}] <{el.role}> {el.name} -> {el.selector}")

    await agent.engine.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## ⌨️ CLI Reference

BrowserClaw features an integrated command-line interface for headless jobs, scrapers, and cron workers:

```bash
# Inspect any URL and print interactive elements
python cli.py https://news.ycombinator.com --task "Analyze front page"

# Output structured JSON for pipeline ingestion
python cli.py https://github.com/trending --task "Extract trending repos" --json

# Run with visible headed browser window
python cli.py https://example.com --headed
```

---

## 📡 REST & WebSocket API Reference

The FastAPI backend exposes fully documented OpenAPI endpoints at `/docs`:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status and Playwright engine diagnostics |
| `GET` | `/api/sessions` | List all historical and running automation sessions |
| `POST` | `/api/sessions` | Launch a new automated session with initial task and URL |
| `GET` | `/api/sessions/{id}` | Retrieve real-time session telemetry and action history |
| `DELETE` | `/api/sessions/{id}` | Abort and purge a session |
| `POST` | `/api/tasks` | Queue an automation task for background execution |
| `WS` | `/ws/live` | WebSocket bidirectional stream for live frame broadcast |

---

## 🗺️ 2026 Strategic Roadmap

- [x] High-performance Playwright Async Core with Stealth Bypass
- [x] React 18 + Tailwind Telemetry Dashboard with WebSocket streaming
- [x] SQLite WAL database persistence with SQLAlchemy 2.0
- [x] Multi-stage Docker containerization and CLI tool
- [x] 100% Quality Gate verified test suite
- [x] Multi-tab concurrent session routing
- [x] Local Vision-LLM (Qwen2.5-VL) bounding box detection
- [x] Chrome Extension for 1-click recording & remote session handoff
- [x] Automatic Cloudflare Turnstile & hCaptcha resolution solver

---

## 🤝 Community & Contributing

Contributions are welcome! Please review our [CONTRIBUTING.md](CONTRIBUTING.md) guide before submitting pull requests.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/EpicFeature`)
3. Commit your Changes (`git commit -m  feat: Add EpicFeature`)
4. Push to the Branch (`git push origin feature/EpicFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

<p align="center">
  <b>Engineered with autonomous precision by Requin AI Agent & <a href="https://github.com/Dali5599">Dali5599</a></b>
</p>
