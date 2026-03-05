# SkillSync

🚀 自动同步你的 AI Skills (Claude Code & OpenClaw) 到 GitHub

## 快速开始

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/yourname/skillsync/main/install.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/yourname/skillsync/main/install.ps1 | iex
```

### 手动安装

```bash
pip install skillsync
```

## 功能特性

✅ 自动识别 Claude Code 和 OpenClaw skills
✅ 双向自动同步（PUSH + PULL）
✅ 支持多机器同步
✅ 版本控制和冲突检测
✅ 自定义目录支持
✅ 手动推送/拉取
✅ 远程/本地版本对比
✅ 跨平台支持 (macOS/Linux/Windows)

## 使用方法

### 初始化配置

```bash
skillsync init
```

### 扫描本地 skills

```bash
skillsync scan
```

### 查看状态

```bash
skillsync status
```

### 手动同步

```bash
# 推送到远程
skillsync push

# 从远程拉取
skillsync pull

# 双向同步
skillsync sync
```

### 版本对比

```bash
# 对比所有 skills
skillsync diff

# 对比特定 skill
skillsync diff claude-code/my-skill
```

### 自定义目录

```bash
# 添加自定义目录
skillsync add-dir /path/to/custom/skills

# 列出所有目录
skillsync list-dirs

# 移除目录
skillsync remove-dir /path/to/custom/skills
```

### 后台自动同步

```bash
# 启动后台守护进程
skillsync start

# 停止后台守护进程
skillsync stop

# 查看日志
skillsync logs
```

## 配置

首次运行 `skillsync init` 会引导你完成配置：

1. GitHub Token (需要 `repo` 权限)
2. 目标仓库 (例如: `yourname/my-skills`)
3. 同步间隔 (默认 5 分钟)
4. 冲突策略 (remote_priority/local_priority/ask)

配置文件位置: `~/.skillsync/config.json`

## 命令速查

```bash
skillsync init              # 初始化配置
skillsync scan              # 扫描本地 skills
skillsync status            # 查看同步状态
skillsync push              # 推送到远程
skillsync pull              # 从远程拉取
skillsync sync              # 双向同步
skillsync diff              # 版本对比
skillsync start             # 启动后台同步
skillsync stop              # 停止后台同步
skillsync logs              # 查看日志
skillsync add-dir <path>    # 添加自定义目录
skillsync list-dirs         # 列出所有目录
skillsync remove-dir <path> # 移除目录
skillsync conflicts         # 查看冲突
skillsync resolve <skill>   # 解决冲突
```

## License

MIT
