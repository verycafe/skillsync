# SkillSync

[English](README.md) | [简体中文](README_CN.md)

🚀 Sync your AI skills across Claude Code and OpenClaw

## Quick Start

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/verycafe/skillsync/main/install.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/verycafe/skillsync/main/install.ps1 | iex
```

### Manual Installation

```bash
pip install git+https://github.com/verycafe/skillsync.git
```

## Features

✅ Auto-detect Claude Code and OpenClaw skills
✅ Bidirectional sync (PUSH + PULL)
✅ Multi-machine sync support
✅ Version control and conflict detection
✅ Custom directory support
✅ Manual push/pull
✅ Remote/local version comparison
✅ Cross-platform (macOS/Linux/Windows)

## Usage

### Initialize

```bash
skillsync init
```

### Scan Local Skills

```bash
skillsync scan
```

### Check Status

```bash
skillsync status
```

### Manual Sync

```bash
# Push to remote
skillsync push

# Pull from remote
skillsync pull

# Bidirectional sync
skillsync sync
```

### Version Comparison

```bash
# Compare all skills
skillsync diff

# Compare specific skill
skillsync diff claude-code/my-skill
```

### Custom Directories

```bash
# Add custom directory
skillsync add-dir /path/to/custom/skills

# List all directories
skillsync list-dirs

# Remove directory
skillsync remove-dir /path/to/custom/skills
```

### Background Auto-Sync

```bash
# Start daemon
skillsync start

# Stop daemon
skillsync stop

# View logs
skillsync logs
```

## Configuration

First run `skillsync init` will guide you through:

1. **GitHub Token** (requires `repo` permission)
   - Create at: https://github.com/settings/tokens/new
2. **Target Repository** (e.g., `yourname/my-skills`)
3. **Sync Interval** (default: 5 minutes)

Config file location: `~/.skillsync/config.json`

## Command Reference

```bash
skillsync init              # Initialize configuration
skillsync scan              # Scan local skills
skillsync status            # Check sync status
skillsync push              # Push to remote
skillsync pull              # Pull from remote
skillsync sync              # Bidirectional sync
skillsync diff              # Version comparison
skillsync start             # Start background sync
skillsync stop              # Stop background sync
skillsync logs              # View logs
skillsync add-dir <path>    # Add custom directory
skillsync list-dirs         # List all directories
skillsync remove-dir <path> # Remove directory
```

## How It Works

### Auto-Detect Directories

**Claude Code:**
- `~/.claude/skills/` (global)
- `.claude/skills/` (project-level)
- `~/.claude/commands/` (legacy)

**OpenClaw:**
- `~/.openclaw/workspace/skills/`
- Extra directories from config

**Custom:**
- Directories added via `skillsync add-dir`

### Sync Flow

```
Local Skills → Detect Changes → Push to GitHub
     ↑                              ↓
     └────── Pull Remote Updates ←──┘
```

### Background Daemon

After starting, automatically every 5 minutes (configurable):
1. Pull remote updates
2. Push local changes
3. Log activities

## Use Cases

### Case 1: Personal Multi-Machine Sync

```bash
# Machine A (work)
skillsync init
skillsync sync
skillsync start

# Machine B (home)
skillsync init  # Use same GitHub repo
skillsync pull
skillsync start

# Now both machines stay in sync automatically
```

### Case 2: Team Collaboration

```bash
# Team Member A
skillsync init --repo team/shared-skills
skillsync sync

# Team Member B
skillsync init --repo team/shared-skills
skillsync pull
```

### Case 3: Version Comparison

```bash
# Check which skills have changes
skillsync diff

# Example output:
# claude-code/commit    ✓ Synced
# claude-code/pr-review ↑ Local newer
# openclaw/api-docs     ↓ Remote newer
```

## Configuration Files

### File Locations

```
~/.skillsync/
├── config.json          # Configuration
├── metadata.json        # Metadata
├── daemon.pid           # Daemon PID
├── daemon.state         # Daemon state
└── sync.log             # Sync logs
```

### config.json Example

```json
{
  "github": {
    "token": "ghp_xxxxxxxxxxxx",
    "repo": "yourname/my-skills"
  },
  "sync_interval": 5,
  "custom_dirs": [
    "/path/to/custom/skills"
  ]
}
```

## GitHub Repository Structure

After syncing, your GitHub repo will look like:

```
my-skills/
├── README.md
├── claude-code/
│   ├── commit/
│   │   └── SKILL.md
│   ├── pr-review/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── review.py
│   └── deploy/
│       └── SKILL.md
└── openclaw/
    ├── api-docs/
    │   └── SKILL.md
    └── test-helper/
        └── SKILL.md
```

## Troubleshooting

### Issue 1: Skills Not Found

```bash
# Check scan results
skillsync scan

# Add custom directory
skillsync add-dir /path/to/your/skills
```

### Issue 2: GitHub Connection Failed

```bash
# Re-initialize
skillsync init

# Check token permissions (needs repo access)
```

### Issue 3: Background Sync Not Working

```bash
# Stop and restart
skillsync stop
skillsync start

# Check logs
skillsync logs
```

## Development

### Local Development

```bash
# Clone repository
git clone https://github.com/verycafe/skillsync.git
cd skillsync

# Install dependencies
pip install -e .

# Run tests
python test_cli.py scan
```

### Project Structure

```
skillsync/
├── skillsync/
│   ├── cli.py           # CLI interface
│   ├── scanner.py       # Scanner
│   ├── syncer.py        # Syncer
│   ├── daemon.py        # Daemon
│   └── cloud/
│       └── github.py    # GitHub integration
├── install.sh           # macOS/Linux installer
├── install.ps1          # Windows installer
└── README.md            # Documentation
```

## Tech Stack

- **Language**: Python 3.8+
- **CLI Framework**: Click
- **Terminal UI**: Rich
- **File Watching**: Watchdog
- **GitHub API**: PyGithub
- **Config**: YAML/JSON

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License - see [LICENSE](LICENSE)

## Links

- [GitHub Repository](https://github.com/verycafe/skillsync)
- [Issue Tracker](https://github.com/verycafe/skillsync/issues)
- [Quick Start Guide](QUICKSTART.md)
- [Examples](EXAMPLES.md)
- [Development Guide](DEVELOPMENT.md)

## Acknowledgments

Thank you for using SkillSync!

If you find it useful, please give it a star ⭐
