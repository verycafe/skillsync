# Changelog

All notable changes to SkillSync will be documented in this file.

## [2.2.0] - 2026-03-05

### Added
- Detailed GitHub token creation guide in `skillsync init`
- `skillsync uninstall` command for clean removal
- Password input hint (characters hidden for security)
- Comprehensive uninstall documentation

### Changed
- Improved installation documentation
- Clarified that pip install requires git URL (not yet on PyPI)
- Updated command reference with all 14 commands

### Fixed
- Confusing installation methods in README

## [1.0.0] - 2026-03-05

### Added
- Initial release
- Auto-detect Claude Code and OpenClaw skills
- Bidirectional sync (PUSH + PULL)
- Multi-machine sync support
- Version control and conflict detection
- Custom directory support
- Background daemon for auto-sync
- Cross-platform support (macOS/Linux/Windows)

---

## How to Update

### Check Current Version
```bash
skillsync --version
```

### Update to Latest Version
```bash
pip install --upgrade git+https://github.com/verycafe/skillsync.git
```

### View Latest Changes
Visit: https://github.com/verycafe/skillsync/releases
