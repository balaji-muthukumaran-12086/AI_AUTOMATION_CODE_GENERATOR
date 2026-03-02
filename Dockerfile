# ──────────────────────────────────────────────────────────────────────────────
# Dockerfile — AI Automation QA Framework
#
# What this image contains:
#   • Python 3.11 + all pip dependencies (requirements.txt)
#   • Java 17 (OpenJDK) — for compiling & running Selenium test JARs
#   • Firefox + Geckodriver — for Selenium WebDriver tests
#   • Xvfb — virtual display for headful Firefox in headless environments
#   • Playwright Chromium — for HealerAgent self-healing
#   • FastAPI / Uvicorn — the Web UI server (port 9500)
#
# What is NOT in this image (must be bind-mounted at runtime):
#   • SDPLIVE_LATEST_AUTOMATER_SELENIUM/ — active test project (Mercurial repo)
#   • AutomaterSeleniumFramework/         — Java framework source (Mercurial repo)
#   • dependencies/                       — JARs; default at ../dependencies
#   • knowledge_base/chroma_db/           — vector DB (named volume or pre-populated)
#
# Ollama (LLM) runs as a SEPARATE container — see docker-compose.yml.
# ──────────────────────────────────────────────────────────────────────────────

FROM ubuntu:22.04

# ── Build-time env ────────────────────────────────────────────────────────────
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
    PATH="/usr/lib/jvm/java-17-openjdk-amd64/bin:$PATH"

# ── System packages ───────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Python
    python3.11 python3.11-venv python3-pip python3.11-dev \
    # Java 17 (for Selenium JVM)
    openjdk-17-jdk \
    # Firefox (Selenium WebDriver)
    firefox \
    # Virtual display (for non-headless Firefox in JVM tests)
    xvfb \
    # Playwright system deps (most are pulled by playwright install-deps,
    # but these cover Chromium's core needs)
    libnss3 libatk-bridge2.0-0 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libxkbcommon0 libasound2 \
    # Utilities
    wget curl ca-certificates gnupg unzip git mercurial \
    && rm -rf /var/lib/apt/lists/*

# ── Geckodriver ───────────────────────────────────────────────────────────────
# Pinned version: v0.35.0 (matches Firefox ESR shipped in Ubuntu 22.04)
RUN GECKO_VER="v0.35.0" && \
    wget -q "https://github.com/mozilla/geckodriver/releases/download/${GECKO_VER}/geckodriver-${GECKO_VER}-linux64.tar.gz" \
         -O /tmp/geckodriver.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# ── Python 3.11 as default python ─────────────────────────────────────────────
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python  python  /usr/bin/python3.11 1 && \
    python3.11 -m pip install --upgrade pip --no-cache-dir

WORKDIR /app

# ── Python dependencies ───────────────────────────────────────────────────────
# Copy only requirements.txt first so Docker layer is cached unless deps change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Playwright — install Chromium browser + system deps ───────────────────────
RUN playwright install chromium && \
    playwright install-deps chromium

# ── Application source ────────────────────────────────────────────────────────
# Copies everything that IS in git (agents/, config/, web/, templates/, etc.)
# gitignored dirs (SDPLIVE, AutomaterSeleniumFramework, dependencies, chroma_db)
# are excluded by .dockerignore and mounted at runtime.
COPY . .

# ── Runtime directories (created empty; filled by volumes at runtime) ─────────
RUN mkdir -p \
    knowledge_base/chroma_db \
    knowledge_base/raw \
    knowledge_base/scout_snapshots \
    logs \
    reports \
    generated \
    uploads

# ── Runtime environment ───────────────────────────────────────────────────────
# These are the Docker-appropriate defaults. Override any value via .env or
# docker-compose environment: section.
ENV FIREFOX_BINARY=/usr/bin/firefox \
    GECKODRIVER_PATH=/usr/local/bin/geckodriver \
    DEPS_DIR=/app/dependencies \
    # Ollama runs as a sidecar container; agents connect via this URL.
    OLLAMA_BASE_URL=http://ollama:11434 \
    # Make JVM tests run headless inside Docker
    JAVA_HEADLESS=true \
    PORT=9500 \
    HOST=0.0.0.0

# ── Expose FastAPI port ───────────────────────────────────────────────────────
EXPOSE 9500

# ── Entrypoint ────────────────────────────────────────────────────────────────
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
