## Akira Nuke – Multi-Token Test Harness

This repository is a **fork/derivative** of the original `Void-Nuke` Discord tool, adapted for **multi-token testing** and **extra logging** so you can better understand how your own servers behave under destructive actions.

> **Important**  
> This code is powerful and destructive. Only use it on servers you own and control, and only for testing / auditing purposes. Misuse of this code against servers you do not own is likely to violate Discord's Terms of Service and may be illegal in your jurisdiction.

---

### Features

- **Interactive CLI tool** (`main.py`)
  - Connects a Discord bot and presents a menu of actions (nuke, mass ban, channel spam, etc.).
  - Allows you to target one or more guilds the bot is a member of.

- **Multi-token concurrent runner** (`multi_runner.py`)
  - Launches **one `main.py` process per token** with shared settings.
  - Lets you:
    - Enter **multiple tokens once**.
    - Choose `all` or specific guild IDs once.
    - Choose **a single menu action code** once.
  - Each token then runs that action concurrently on its own guilds (no repeated menus per bot).

- **Action statistics log** (`void_nuke_stats.log`)
  - Every tool action that calls `_summary` now writes a line like:
    - `YYYY-MM-DD HH:MM:SS | <ActionName> | ok=<N> | err=<M> | <seconds>s`
  - Useful for tracking how many operations succeeded/failed across runs.

- **Message history logs** (`message_logs/`)
  - Every non-bot message seen in a guild is appended to a guild-specific file:
    - `message_logs/guild_<guild_id>.log`
  - Each line includes timestamp, guild ID, channel ID, author ID, username, and plain-text content.
  - Intended as a **safety net** to inspect or manually reconstruct messages if destructive actions are run on the wrong server.

- **Optional webhook logger** (built-in)
  - Original Void-Nuke webhook logger preserved:
    - Can stream message activity to a chosen webhook for additional auditing.

---

### Project Layout

- `main.py`  
  Core CLI tool. Handles:
  - Terminal UI, menu, and all raid/admin actions.
  - Webhook-based logging (`webhook_logger`, `webhook_logger_check`).
  - File-based message logging (`_file_message_logger`).
  - Stats logging via `_summary`.
  - Env-based startup:
    - `VOIDNUKE_TOKEN` – bot token.
    - `VOIDNUKE_SERVERS` – `"all"` or comma-separated guild IDs.
    - `VOIDNUKE_ACTION` – optional menu code (e.g. `"01"`, `"33"`) for non-interactive use.

- `multi_runner.py`  
  Thin launcher that:
  - Prompts for:
    - `Enter bot tokens (comma-separated):`
    - `server id(s) or all:`
    - `menu action code (e.g. 01 for Nuke, 33 for Spam):`
  - For each token:
    - Spawns `python main.py` in a new process.
    - Sets:
      - `VOIDNUKE_TOKEN`
      - `VOIDNUKE_SERVERS`
      - `VOIDNUKE_ACTION`
  - Each spawned process:
    - Logs in with its token.
    - Resolves guilds from `VOIDNUKE_SERVERS`.
    - If `VOIDNUKE_ACTION` is set, runs that action on all matching guilds and exits **without showing menus**.

- `README_VOID_FORK.md`  
  Lower-level notes focused on the fork-specific changes; this `README.md` is the main GitHub-facing documentation.

Other files and assets (artwork, original menu, etc.) come from the upstream Void-Nuke project.

---

### Installation

1. **Clone / download** this repository.

2. Ensure you have a recent **Python 3** (3.9+ recommended).

3. Install Python dependencies:

```bash
pip install -U discord.py aiohttp colorama
```

The code also uses these standard-library modules (no extra install required):  
`os`, `sys`, `time`, `random`, `asyncio`, `json`, `re`, `webbrowser`, `urllib.request`, `datetime`, `shutil`.

4. Create one or more **Discord bot tokens** in the [Discord Developer Portal](https://discord.com/developers/applications) and add the bot(s) to the guilds you want to test, with sufficient permissions for the actions you plan to run.

---

### Usage

#### 1. Single Bot – Interactive Mode

Run the core tool directly:

```bash
python main.py
```

You will be prompted for:

- `token` – your bot token.
- `server id(s) or all` – either:
  - `all` to include all guilds the bot is in, or
  - a comma-separated list of guild IDs (e.g. `1234567890, 9876543210`).

After connecting, you choose:

- A **target server** from the list shown.
- A **menu option code** from the ASCII menu (e.g. `01` = Nuke, `33` = Spam, etc.).

Actions log their stats to `void_nuke_stats.log` automatically.

#### 2. Multiple Bots – Shared Action (Non-interactive)

Use the multi-runner:

```bash
python multi_runner.py
```

Prompts:

1. **Enter bot tokens (comma-separated):**  
   Paste all the tokens you want to use, separated by commas.

2. **server id(s) or all:**  
   - `all` – each bot targets all guilds it is in.
   - or a comma-separated list of guild IDs.

3. **menu action code (e.g. 01 for Nuke, 33 for Spam):**  
   - The same number you’d type in the interactive menu.

For each token, `multi_runner.py` will:

- Spawn `main.py` in its own process.
- Configure it via environment variables.
- Let `main.py`:
  - Log in,
  - Resolve its list of guilds,
  - Run the chosen action on all matching guilds,
  - Exit when done (no extra prompts, no menu).

---

### Logs and Recovery Aids

- **Action Stats – `void_nuke_stats.log`**
  - One line per completed action.
  - Helps you see how many entities were touched and how many failed.

- **Message History – `message_logs/guild_<guild_id>.log`**
  - Contains all non-bot messages seen in that guild while the bot was running.
  - Intended as a reference for manual reconstruction (e.g., re-posting chats) if a destructive action is mistakenly run on the wrong server.

- **Webhook Logger (optional)**
  - Via the menu option for webhook logs, you can forward activity to a Discord webhook as well.

---

### Safety & Responsibility

- Do **not** use this tool on servers you do not own or administer.
- Be mindful of **Discord rate limits** and terms of service.
- Consider running on **test servers** that mirror your real configuration to avoid accidental damage.
- Keep your **bot tokens secret**; never commit them or share them publicly.

This repository is provided for educational and testing purposes only. You are solely responsible for how you use it.


