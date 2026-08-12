# 🤖 Tony AI Assistant

Tony is a **voice-controlled AI desktop assistant for Windows**, designed to interact with the user's computer through natural language.

The project combines **local speech recognition, voice activity detection, text-to-speech, Gemini-powered reasoning, desktop automation, browser automation, system controls, file management, and terminal capabilities**.

The long-term goal is to evolve Tony from a simple voice assistant into a **fully agentic desktop assistant** capable of understanding goals, planning multi-step tasks, interacting with applications, and safely executing actions on the user's computer.

---

## ✨ Current Capabilities

### 🎤 Voice System

Tony currently uses a fully local voice pipeline for listening and speaking:

* **Faster-Whisper** — speech-to-text
* **Silero VAD** — voice activity detection
* **Piper** — text-to-speech
* **SoundDevice** — microphone input
* Voice activity pre-roll to reduce first-word clipping
* Natural wake-word detection
* Tony can be mentioned anywhere in a sentence

Examples:

```text
Tony, open Notepad.

Hey Tony, open Notepad.

Can you Tony decrease the volume?

Open Paint, Tony.
```

---

## 🧠 AI / LLM

Tony uses **Google Gemini** as the reasoning engine.

The LLM is responsible for:

* Understanding natural-language commands
* Selecting appropriate tools
* Generating tool arguments
* Conversational responses
* Handling ambiguous requests

The application separates AI reasoning from actual tool execution.

```text
User
 ↓
Voice Recognition
 ↓
Tony Agent
 ↓
Gemini
 ↓
Tool Selection
 ↓
Tool Executor
 ↓
System / Browser / File / Terminal
 ↓
Result
 ↓
Piper
 ↓
Voice Response
```

---

## 🖥️ System Control

Tony currently supports several Windows system operations.

### 🔊 Volume

* Increase volume
* Decrease volume
* Mute
* Unmute

Powered by **PyCaw**.

Example:

```text
Tony, decrease the volume.

Tony, mute the volume.
```

---

### ☀️ Brightness

Tony can:

* Get current brightness
* Increase brightness
* Decrease brightness
* Set brightness to a specific percentage

Example:

```text
Tony, increase the brightness.

Tony, set brightness to 50 percent.
```

Powered by `screen-brightness-control`.

---

### 📶 Wi-Fi

Tony can:

* Check Wi-Fi status
* Enable Wi-Fi
* Disable Wi-Fi

The current implementation uses the Windows `Wi-Fi` network adapter.

---

### 💻 System Information

Tony can retrieve:

* Operating system
* CPU information
* CPU usage
* RAM usage
* Battery percentage
* Charging status

Powered by `psutil`.

Example:

```text
Tony, what's my CPU usage?

Tony, how much RAM am I using?

Tony, what's my battery level?
```

---

## 📱 Application Control

Tony can currently open and close supported Windows applications.

Supported applications:

* Notepad
* Calculator
* Paint

Examples:

```text
Tony, open Notepad.

Tony, close Notepad.

Tony, open Paint.

Tony, close Calculator.
```

The application system is designed to be expanded with additional applications.

---

# 🌐 Browser Automation

Tony includes a persistent Chromium browser controlled through **Playwright**.

### Current capabilities

* Open URLs
* Google search
* Read webpage text
* Inspect interactive elements
* Click elements
* Type into elements
* Press keyboard keys
* Close browser
* Maintain the same browser instance across commands

Current browser architecture:

```text
Tony
 ↓
Browser Tool
 ↓
Browser Manager
 ↓
Playwright
 ↓
Chromium
```

Example:

```text
Tony, open Google.

Tony, search for Python tutorials.

Tony, read this page.
```

The browser is being developed toward a more advanced agentic browsing system capable of:

* Understanding webpage structure
* Finding relevant elements
* Performing multi-step interactions
* Completing browser-based tasks

---

# 📁 File & Folder Management

Tony can currently:

* List files and folders
* Create folders
* Open folders in File Explorer
* Find files
* Copy files
* Move files
* Rename files and folders
* Delete files with confirmation

Tony understands common Windows locations such as:

```text
Desktop
Downloads
Documents
```

The filesystem resolver also handles **OneDrive-backed Windows folders**.

For example, if Windows redirects Documents to:

```text
C:\Users\<user>\OneDrive\Documents
```

Tony can resolve that location automatically.

The resolver also handles speech-recognition variations such as:

```text
TonyTest
tonytest
Tony Test
tony test
```

---

# 🛡️ Confirmation & Safety System

Tony includes a confirmation mechanism for potentially destructive actions.

For example:

```text
User:
Tony, delete the Test folder from Documents.

Tony:
This will permanently delete
C:\Users\<user>\OneDrive\Documents\Test.
Do you want me to continue?

User:
Yes.

Tony:
Test deleted successfully.
```

Tony stores the pending action temporarily until the user confirms or cancels it.

This prevents the LLM from directly executing destructive operations without confirmation.

The same architecture can later be extended to:

* Terminal commands
* File deletion
* Git operations
* Software installation
* System shutdown
* Sending messages
* Other high-impact operations

---

# 💻 Terminal Agent

Tony now has a PowerShell-based terminal tool.

The initial implementation is intentionally restricted to safe commands.

Supported examples include:

```text
python --version
node --version
npm --version
git --version
git status
git branch
git log
where python
where node
where git
pwd
whoami
hostname
```

Example:

```text
Tony, what version of Python am I using?

Tony, what version of Node am I using?

Tony, run git status.
```

Commands outside the safe list are currently rejected until the confirmation architecture is extended to terminal operations.

This prevents Tony from blindly executing arbitrary commands generated by the LLM.

---

# 🏗️ Architecture

Tony is organized around a modular tool-based architecture.

```text
ProjectTony/
│
├── app/
│   │
│   ├── agent/
│   │   ├── agent.py
│   │   ├── tool_executor.py
│   │   └── validator.py
│   │
│   ├── core/
│   │   ├── constants.py
│   │   └── logger.py
│   │
│   ├── llm/
│   │   └── gemini.py
│   │
│   ├── registry/
│   │   ├── decorators.py
│   │   └── registry.py
│   │
│   ├── tools/
│   │   ├── apps.py
│   │   ├── volume.py
│   │   ├── brightness.py
│   │   ├── wifi.py
│   │   ├── system.py
│   │   ├── browser.py
│   │   ├── browser_manager.py
│   │   ├── files.py
│   │   ├── terminal.py
│   │   └── tool_result.py
│   │
│   ├── voice/
│   │   ├── listener.py
│   │   └── speaker.py
│   │
│   └── main.py
│
├── voices/
│   └── Piper voice models
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🔧 Tool Architecture

Tony uses a central tool registry.

Tools are registered using decorators:

```python
@tool(
    name="example",
    description="..."
)
```

The general execution flow is:

```text
Gemini
 ↓
Tool name + arguments
 ↓
Registry
 ↓
ToolExecutor
 ↓
Tool function
 ↓
ToolResult
 ↓
Tony
```

This makes adding new capabilities relatively straightforward.

A new capability can be implemented as an independent tool rather than modifying the core agent.

---

# 🗣️ Voice Pipeline

The current voice pipeline is:

```text
Microphone
    ↓
SoundDevice
    ↓
Silero VAD
    ↓
Speech Detection
    ↓
Pre-roll Buffer
    ↓
Faster-Whisper
    ↓
Text
    ↓
Tony Agent
```

For responses:

```text
Tony Agent
    ↓
Text response
    ↓
Piper
    ↓
WAV
    ↓
Speaker
```

The pre-roll buffer was added to reduce a problem where the first word of a sentence was sometimes clipped before speech detection began.

---

# 🚪 Application Lifecycle

Tony can now be stopped through voice commands instead of requiring `Ctrl+C`.

Supported commands include:

```text
Tony, exit.

Tony, stop.

Tony, quit.

Tony, shutdown.

Tony, goodbye.
```

These commands are handled **before Gemini** so that the LLM cannot interpret them as ordinary requests.

---

# 🧪 Current Development Status

| Component                   | Status |
| --------------------------- | ------ |
| Voice input                 | ✅      |
| Whisper STT                 | ✅      |
| Silero VAD                  | ✅      |
| Piper TTS                   | ✅      |
| Gemini integration          | ✅      |
| Tool registry               | ✅      |
| Tool executor               | ✅      |
| Volume control              | ✅      |
| Brightness control          | ✅      |
| Wi-Fi control               | ✅      |
| System information          | ✅      |
| Application control         | ✅      |
| Browser automation          | ✅      |
| File management             | ✅      |
| Confirmation system         | ✅      |
| Basic terminal              | 🟡     |
| Persistent memory           | ⬜      |
| Agent planning              | ⬜      |
| Advanced browser agent      | 🟡     |
| GUI                         | ⬜      |
| Windows startup integration | ⬜      |

---

# 🚀 Planned Features

## 1. Advanced Browser Agent

Improve browser interaction so Tony can understand elements semantically rather than relying primarily on temporary numeric IDs.

Target:

```text
Tony, find the YouTube website
and search for Python tutorials.
```

Tony should be able to:

```text
Search
 ↓
Inspect
 ↓
Identify search box
 ↓
Type
 ↓
Press Enter
 ↓
Read results
 ↓
Choose result
```

---

## 2. Advanced Terminal Agent

Expand terminal capabilities with:

* Working-directory awareness
* Project detection
* Command safety classification
* Confirmation for risky commands
* Command output interpretation
* Git workflows
* Development environment management

Example:

```text
Tony, start ProjectTony.
```

---

## 3. Persistent Memory

Tony will eventually maintain long-term information such as:

```text
Projects
Preferences
Important paths
Previous tasks
User-defined information
```

Example:

```text
Remember that ProjectTony is in C:\Projects\ProjectTony.
```

Later:

```text
Tony, open my Tony project.
```

---

## 4. Agent Planning

The most important long-term feature.

Currently:

```text
User request
 ↓
Gemini
 ↓
One tool
 ↓
Result
```

The target architecture is:

```text
User Goal
 ↓
Planner
 ↓
Plan
 ↓
Execute
 ↓
Observe
 ↓
Re-plan
 ↓
Continue
 ↓
Complete
```

This will allow Tony to perform multi-step tasks instead of simply executing individual commands.

---

## 5. Safety & Approval Framework

The confirmation mechanism will eventually become a centralized policy system.

Example:

```text
LOW RISK
Open application
Read file
Search web
     ↓
Execute automatically

MEDIUM RISK
Install package
Git push
Modify files
     ↓
Ask confirmation

HIGH RISK
Delete files
Run dangerous commands
Shutdown system
     ↓
Require explicit confirmation
```

---

## 6. Tony Desktop Application

The final version will no longer require:

```powershell
python app/main.py
```

every time.

The goal is:

```text
Windows starts
       ↓
Tony starts
       ↓
Tony runs in background
       ↓
🎤 Tony is ready
```

Eventually Tony will have:

* Windows startup integration
* System tray application
* Pause/resume listening
* Settings
* Logs
* Restart
* Full shutdown
* Packaged Windows executable

---

# 🎯 Vision

The ultimate goal of Project Tony is to create a **local-first AI desktop agent** that can understand natural language and interact with the user's computer safely.

Instead of:

```text
Open application manually
Search manually
Navigate manually
Run commands manually
Manage files manually
```

the goal is:

```text
"Tony, get my development environment ready."
```

Tony should eventually understand the objective, create a plan, interact with the computer, verify the results, recover from failures, and report back to the user.

---

## 🛠️ Development

Clone the repository and install the required Python dependencies.

Run Tony during development with:

```powershell
python app/main.py
```

The project is currently being developed and tested primarily on:

```text
Windows 11
Python 3.12
Node.js 22
PowerShell 5.1
```

---

## ⚠️ Development Status

Tony is currently an **active development project**.

Some capabilities are experimental and may change as the agent architecture evolves.

The project prioritizes:

1. Reliability
2. Modular architecture
3. Local processing where practical
4. Safe tool execution
5. Explicit confirmation for destructive actions
6. Gradual transition from command-based automation to autonomous task execution

---

## 📌 Project Goal

**Build Tony from a voice-controlled assistant into a reliable, safe, agentic Windows AI assistant.**
