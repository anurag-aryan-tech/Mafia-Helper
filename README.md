# 🕵️ Mafia Mediator’s Dashboard

A **desktop game-master dashboard** built with **Python + Tkinter** that streamlines mediating the *Mafia* party game—especially when playing with **LLM players** like ChatGPT, Claude, Grok, Gemini, and others.

This tool centralizes **player management, role assignment, prompt generation, and night/day workflows**, eliminating the cognitive and logistical overhead of running Mafia across multiple AI chat windows.

---

## 🎮 What Is This?

Running Mafia with LLMs as players is surprisingly complex. As the mediator, you must:

- Track who is alive and dead
- Remember each player’s secret role
- Repeatedly rewrite and customize prompts
- Maintain game state across day/night cycles
- Coordinate multiple LLM chats simultaneously

**Mafia Mediator’s Dashboard** solves this by acting as a **single source of truth** for the entire game.

> Think of it as a Dungeon Master screen—but for Mafia, and built specifically for AI players.
> 

---

## ✨ Core Features

### 🧑‍🤝‍🧑 Player & Role Management

- Supports **4–11 players**
- Roles: Villager, Mafia, Sheriff, Doctor
- Automatic Mafia count validation based on player total
- Custom player names (e.g., “ChatGPT-4”, “Claude”, “Gemini”)
- Role locking to prevent mid-game tampering

---

### 🧠 Prompt System (LLM-Focused)

- Rich, role-specific prompts (1,500–2,000+ words each)
- Dynamic placeholder replacement per player
- Turn-order–aware instructions
- Mafia prompts include partner identities
- One-click **copy to clipboard** for fast sharing

Supported prompt types:

- Initial role & rules prompts
- Night-phase decision prompts
- Investigation & protection result prompts

---

### 🌙 Night Phase Automation

Dedicated UI for each role:

- **Mafia**
    - Phase 1: Discussion logging
    - Phase 2: Voting & elimination logic
- **Sheriff**
    - Investigation reasoning + result generation
- **Doctor**
    - Protection selection & confirmation

The system automatically:

- Tracks votes
- Applies Doctor protection
- Logs night outcomes
- Advances round counters

---

### 🎨 UI / UX

- Dark, modern interface using **CustomTkinter**
- Pixel-art buttons with animated states
- Responsive layout with dynamic image scaling
- Clean separation between phases and responsibilities

---

## 🛠️ Tech Stack

| Tool | Purpose |
| --- | --- |
| **Python 3.8+** | Core language |
| **Tkinter** | Base GUI framework |
| **CustomTkinter** | Modern theming & widgets |
| **Pillow (PIL)** | Image loading & resizing |
| **Nano Banana** | AI-generated UI assets |
| **Pixelorama** | Pixel-art button design |

---

## 📁 Project Structure

```
Mafias/
├── Helper.py                # Application entry point
├── button_commands.py       # Main dashboard button handlers
├── database.py              # In-memory game state
├── utils.py                 # Shared UI & helper utilities
├── requirements.txt
│
├── windows/                 # Game phase windows
│   ├── total_players/
│   ├── roles/
│   ├── prompts/
│   └── night/
│
├── images/                  # Backgrounds & UI assets
├── [role]_button/           # Button animation frames
└── color/                   # Color palette references

```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8+**
- `pip`
- Multiple LLM chat tabs (browser-based)

### Installation

```bash
git clone <repository-url>
cd Mafias
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python Helper.py

```

---

## 🧭 Typical Game Flow

1. **START** → Set total players & Mafia count
2. **ROLES** → Assign names and roles (locks game state)
3. **PROMPTS** → Distribute initial role prompts to LLMs
4. **DAY 1** → Players discuss externally
5. **NIGHT** → Run Mafia / Sheriff / Doctor actions
6. **DAY N** → Discussion & voting
7. Repeat until win condition
8. **RESET** → Start a new game

---

## 🧩 Game Logic Summary

### Role Rules

- Exactly **1 Sheriff**
- Exactly **1 Doctor**
- Remaining slots split between Mafia & Villagers

### Mafia Balance

```
Max Mafia = ⌊Total Players / 2⌋

```

### Win Conditions

- **Town wins:** All Mafia eliminated
- **Mafia wins:** Mafia ≥ remaining Town players

---

## 🗂️ Internal State Model

```python
Database:
- total_players
- total_mafias
- players_list
- mafias_list
- sheriff
- doctor
- first_disable
- prompts

Night_Day_Helper:
- night_number
- day_number
- night_phase
- dialogues
- votes
- doctor_save

```

---

## ⚠️ Known Limitations

### Incomplete / Experimental

- Day Phase UI (discussion & voting not fully visualized)
- Eliminated players not removed from dropdowns
- No save/load persistence
- Single-game session only

### Design Constraints

- Manual copy-paste (no direct LLM API integration)
- Desktop-only (Tkinter)
- Single-machine mediator model

---

## 🔮 Planned Improvements

### 🚧 Will Be Completed Soon

- [ ]  Day Phase UI with voting visualization
- [ ]  Eliminated players removed from dropdowns

### ⏳ Might Not Be Completed Before April

- [ ]  Direct OpenAI / Anthropic API integration
- [ ]  Web-based version (Flask / React)
- [ ]  Custom roles & rule variants
- [ ]  Game analytics & replay

---

## 🎨 Visual Design Notes

- **Primary BG:** `#0E0D0B`
- **Frame:** `#2A332A`
- **Text:** `#E6EAF0`
- **Accent:** `#FF2A2A`

Buttons use pixel-art animation:

- `frame_1.png` → idle
- `frame_2.png` → pressed

---

### 🙏 Credits

**Developer**

- **SOLO — Anurag Aryan**

**Tools**

- Tkinter & CustomTkinter
- Pillow
- Nano Banana (AI assets)
- Pixelorama (pixel art)

Inspired by classic *Mafia / Werewolf* mechanics and modern LLM-driven social deduction experiments.

---

## 🎭 Final Note

This project is both a **game tool** and a **prompt-engineering experiment**.

If you enjoy orchestrating chaos among AIs—or want to build richer LLM-driven games—this dashboard is a solid foundation.

**Happy mediating. Trust no one!** 🕵️‍♂️
