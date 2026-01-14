# CHANGELOG

## v1.0 - 2026-01-14

### Added
- **Player & Role Management**
  - Supports 3–20 players
  - Roles: Villager, Mafia, Sheriff, Doctor
  - Automatic Mafia count validation based on total players
  - Custom player names for AI or human participants
  - Role locking to prevent mid-game tampering
  - Eliminated players automatically removed from dropdowns

- **LLM-Focused Prompt System**
  - Rich, role-specific prompts (1,500–2,000+ words)
  - Dynamic placeholder replacement per player
  - Turn-order–aware instructions
  - Mafia prompts include partner identities
  - One-click copy to clipboard for seamless distribution
  - Supports initial role prompts, night-phase actions, day-phase discussions, and result prompts

- **Night Phase Automation**
  - Dedicated UI for Mafia, Sheriff, and Doctor roles
  - Tracks votes and applies Doctor protection automatically
  - Logs night outcomes
  - Advances round counters without manual intervention

- **Day Phase Management**
  - Discussion logging for each player
  - Automated voting and elimination
  - Win condition verification (Town vs Mafia)
  - Smooth transition back to night phase

- **UI / UX Enhancements**
  - Dark, modern interface using CustomTkinter
  - Pixel-art buttons with animated states
  - Responsive layout with dynamic image scaling
  - Clear separation of game phases and responsibilities

- **Tech Stack & Assets**
  - Python 3.8+, Tkinter, CustomTkinter
  - Pillow (PIL) for image handling
  - Nano Banana for AI-generated UI assets
  - Pixelorama for pixel-art button design

- **Project Architecture**
  - In-memory game state model; no external database required
  - Organized folder structure for windows, prompts, roles, and images
  - Clear separation of helper functions, UI logic, and game state management

### Known Limitations
- Manual copy-paste required; no direct LLM API integration
- Desktop-only (Tkinter)
- Single-machine mediator model
- No save/load persistence between sessions

### Notes
- First stable release (v1.0) with full workflow from START → NIGHT → DAY → RESET
- Designed for LLM-driven Mafia games and prompt-engineering experiments
