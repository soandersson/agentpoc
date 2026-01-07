# Mac Development Environment Setup

Complete guide to set up your Mac for developing with this LangGraph agent project using dev containers.

## 📋 Prerequisites

- macOS Sequoia (15.x) or later recommended
  - Also compatible with macOS Sonoma (14.x) and Ventura (13.x)
- Administrator access on your Mac
- Stable internet connection
- 16GB+ RAM recommended (8GB minimum)

## 🚀 Setup Steps

### 1. Install Homebrew

Homebrew is the package manager for macOS that makes installing software easy.

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Follow the post-installation instructions to add Homebrew to your PATH
# (The installer will show you the exact commands to run)

# Verify installation
brew --version
```

Expected output: `Homebrew 4.x.x` or similar

---

### 2. Install iTerm2 (Optional but Recommended)

iTerm2 is a powerful terminal replacement for macOS with better features than the default Terminal app.

#### Install iTerm2
```bash
# Using Homebrew
brew install --cask iterm2
```

#### Or Manual Download
1. Visit [iterm2.com](https://iterm2.com/)
2. Download the latest stable release
3. Open the `.zip` file and drag iTerm to Applications

#### Configure iTerm2 (Optional)
Once installed, you can customize iTerm2:
1. Open iTerm2
2. Go to **Preferences** (Cmd+,)
3. Recommended settings:
   - **Appearance** → Theme: Minimal (or your preference)
   - **Profiles** → Colors: Choose a color scheme (Solarized Dark is popular)
   - **Profiles** → Terminal: Enable "Unlimited scrollback"

#### Why iTerm2?
- Split panes (Cmd+D horizontal, Cmd+Shift+D vertical)
- Better search (Cmd+F)
- Hotkey window (global terminal overlay)
- Advanced copy/paste
- Session restoration

---

### 3. Install Docker Desktop

Docker Desktop enables running containers on your Mac, which is required for dev containers.

#### Installation
1. Visit [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Click **Download for Mac** (it will auto-detect Apple Silicon or Intel)
3. Open the downloaded `.dmg` file
4. Drag the Docker icon to your Applications folder
5. Launch **Docker Desktop** from Applications
6. Follow the setup wizard and grant necessary permissions

> **Note**: If you prefer using Homebrew: `brew install --cask docker`

#### Configure Docker
1. Open Docker Desktop
2. Go to **Settings** (gear icon)
3. **Resources** → Set reasonable limits:
   - CPUs: 4-6 cores
   - Memory: 8-12 GB
   - Swap: 2 GB
   - Disk image size: 64+ GB
4. Click **Apply & Restart**

#### Verify Docker
```bash
docker --version
docker run hello-world
```

---

### 4. Install Visual Studio Code

VS Code is the recommended IDE with excellent dev container support.

#### Installation
1. Visit [code.visualstudio.com](https://code.visualstudio.com/)
2. Click **Download for Mac**
3. Open the downloaded `.zip` file
4. Drag **Visual Studio Code** to your Applications folder
5. Launch VS Code from Applications

> **Note**: If you prefer using Homebrew: `brew install --cask visual-studio-code`

#### Optional: Add VS Code to Terminal
For convenience, you can open VS Code from the terminal:
1. Open VS Code
2. Press `Cmd+Shift+P` to open Command Palette
3. Type "shell command" and select: **Shell Command: Install 'code' command in PATH**

---

### 5. Install VS Code Extensions

#### Required Extensions

Install these extensions through VS Code's Extensions panel:

1. Open **VS Code**
2. Click the **Extensions** icon in the left sidebar (or press `Cmd+Shift+X`)
3. Search for and install each of these:

**Essential (Required):**
- **Dev Containers** - Search for "Dev Containers" by Microsoft
- **Python** - Search for "Python" by Microsoft
- **Pylance** - Search for "Pylance" by Microsoft
- **Docker** - Search for "Docker" by Microsoft

**Optional but Helpful:**
- **GitHub Copilot** - If you have a Copilot subscription

> **Tip**: Make sure to install the ones published by "Microsoft" for best compatibility.

---

### 6. Install Ollama

Ollama runs LLMs locally on your Mac.

#### Installation
1. Visit [ollama.com/download](https://ollama.com/download)
2. Click **Download for macOS**
3. Open the downloaded file and follow the installation prompts
4. The Ollama icon will appear in your menu bar when running

> **Note**: If you prefer using Homebrew: `brew install ollama`

#### Verify Ollama
Ollama should start automatically. To verify:
1. Look for the Ollama icon in your menu bar (top right)
2. Open Terminal (or iTerm2) and run:
```bash
ollama list
```
This shows installed models (will be empty at first).

---

### 7. Pull Ollama Models

Download models that support tool calling for the best experience with this project.

#### Recommended Models

**Quick Start (Small & Fast)**
```bash
# llama3.2 - 2GB, fast, good for learning
ollama pull llama3.2

# qwen2.5:3b - 2GB, alternative with good performance
ollama pull qwen2.5:3b
```

**Better Performance (Larger)**
```bash
# llama3.1 - 4.7GB, more capable
ollama pull llama3.1

# mistral - 4.1GB, good balance
ollama pull mistral
```

**High Performance (Requires more RAM)**
```bash
# llama3.1:70b - 40GB, best quality (requires 64GB+ RAM)
ollama pull llama3.1:70b

# qwen2.5:14b - 9GB, excellent mid-size option
ollama pull qwen2.5:14b
```

#### Verify Models
```bash
ollama list
```

You should see a list of downloaded models with their sizes.

#### Test a Model
```bash
ollama run llama3.2
# Type a message to test
# Press Ctrl+D to exit
```

---

### 8. Open Project in Dev Container

Now you're ready to run this project in a dev container!

#### Get the Project
1. Download or clone this repository to your Mac
2. Remember where you saved it (e.g., Downloads or Documents)

#### Open in VS Code
1. Open **Visual Studio Code**
2. Go to **File** → **Open Folder**
3. Navigate to the `agentpoc` folder and click **Open**

#### Start the Dev Container

VS Code will detect the dev container configuration:

1. Look for a notification in the bottom-right: **"Folder contains a Dev Container configuration"**
2. Click **Reopen in Container**
3. Wait for the container to build (first time takes 2-5 minutes)

**Alternative if you don't see the notification:**
1. Press `Cmd+Shift+P` to open Command Palette
2. Type "Dev Containers: Reopen in Container"
3. Press Enter

#### What Happens During Build
- Docker pulls the base image
- Python 3.12 is installed
- All dependencies from `requirements.txt` are installed
- Development environment is configured

#### Verify You're in the Container
- Bottom-left corner of VS Code should show: **Dev Container: Python 3**
- Open a new terminal in VS Code: **Terminal** → **New Terminal**
- The terminal prompt will show you're inside the container

---

### 9. Configure and Test the Agent

#### Set Up Environment
```bash
# Activate virtual environment (should auto-activate in container)
source .venv/bin/activate

# Check Ollama connection from container
python setup_check.py
```

#### Run Your First Agent Query
```bash
# Interactive mode
python agent.py

# Or run examples
python main.py
```

---

## 🔧 Troubleshooting

### Docker Issues

**"Cannot connect to Docker daemon"**
1. Make sure Docker Desktop is running (check menu bar icon)
2. Open Docker Desktop from Applications if needed
3. Wait for it to fully start (green icon in menu bar)

**"No space left on device"**
1. Open Docker Desktop
2. Go to **Settings** (gear icon) → **Resources** → **Advanced**
3. Increase the **Disk image size** (recommended: 64GB+)
4. Click **Apply & Restart**

Or clean up unused Docker data:
1. Open Docker Desktop
2. Go to **Troubleshoot** (bug icon) → **Clean / Purge data**

### Ollama Connection Issues

**"Connection refused" to Ollama from container**

The dev container tries to connect to Ollama on your host machine. The connection URL depends on your setup:

**Default (should work for most):**
```bash
export OLLAMA_BASE_URL=http://host.docker.internal:11434
```

**Alternative for some Docker setups:**
```bash
export OLLAMA_BASE_URL=http://172.17.0.1:11434
```

**Test connection from container:**
```bash
curl http://host.docker.internal:11434/api/tags
```

**If nothing works, use host network mode:**
Edit `.devcontainer/devcontainer.json`:
```json
{
  "runArgs": ["--network=host"]
}
```
Then rebuild container and use `http://localhost:11434`

### Dev Container Issues

**"Failed to connect to dev container"**
1. Restart Docker Desktop (Quit and reopen)
2. Close VS Code completely
3. Reopen VS Code and try again

**Rebuild the container if something goes wrong:**
1. Press `Cmd+Shift+P` in VS Code
2. Type "Dev Containers: Rebuild Container"
3. Press Enter and wait for rebuild

### VS Code Extensions

**Extensions not appearing:**
1. Click the Extensions icon in VS Code
2. Search for "Dev Containers"
3. If not installed, install it
4. Reload VS Code

---

## 📚 Additional Resources

### Documentation
- [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Homebrew](https://brew.sh/)

### Useful Commands

```bash
# Homebrew
brew update              # Update Homebrew
brew upgrade             # Upgrade all packages
brew list                # List installed packages

# Docker
docker ps                # List running containers
docker images            # List images
docker system df         # Check disk usage

# Ollama
ollama list              # List installed models
ollama rm <model>        # Remove a model
ollama ps                # List running models

# VS Code
code --list-extensions   # List installed extensions
```

---

## ✅ Quick Verification Checklist

Before starting development, verify everything is working:

- [ ] Homebrew installed: `brew --version`
- [ ] Docker Desktop running: `docker --version` and `docker ps`
- [ ] VS Code installed: `code --version`
- [ ] Dev Containers extension installed
- [ ] Ollama running: `ollama list` shows models
- [ ] At least one model pulled (llama3.2 or llama3.1)
- [ ] Project opens in dev container
- [ ] `python setup_check.py` shows ✅ for Ollama connection
- [ ] `python agent.py` runs successfully

---

## 🎉 You're Ready!

Your Mac is now fully configured for LangGraph agent development. Next steps:

1. Read [README.md](README.md) for project overview
2. Read [LEARNING_GUIDE.md](LEARNING_GUIDE.md) for concepts
3. Try `python agent.py` to interact with your agent
4. Experiment with different queries and tools

Happy coding! 🚀
