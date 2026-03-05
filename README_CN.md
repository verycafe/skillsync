# SkillSync

[English](README.md) | 简体中文

🚀 自动同步你的 AI Skills (Claude Code & OpenClaw) 到 GitHub

[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](https://github.com/verycafe/skillsync/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 快速开始

### 安装

```bash
pip install git+https://github.com/verycafe/skillsync.git
```

### 初始化

```bash
skillsync init
```

会提示你输入：
- GitHub Personal Access Token（需要 `repo` 权限）
- 目标仓库（例如：`yourname/my-skills`）
- 同步间隔（默认：5 分钟）

### 可选：一键安装（macOS/Linux）

> **注意**：这会自动安装并运行 `skillsync init`

```bash
curl -fsSL https://raw.githubusercontent.com/verycafe/skillsync/main/install.sh | bash
```

## 更新

### 查看当前版本

```bash
skillsync --version
```

### 更新到最新版本

```bash
pip install --upgrade git+https://github.com/verycafe/skillsync.git
```

**查看更新内容：** 查看 [CHANGELOG](CHANGELOG.md) 或 [Releases](https://github.com/verycafe/skillsync/releases)

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

1. **GitHub Token** (需要 `repo` 权限)
   - 创建地址: https://github.com/settings/tokens/new
2. **目标仓库** (例如: `yourname/my-skills`)
3. **同步间隔** (默认 5 分钟)

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
skillsync uninstall         # 卸载 SkillSync
```
skillsync start             # 启动后台同步
skillsync stop              # 停止后台同步
skillsync logs              # 查看日志
skillsync add-dir <path>    # 添加自定义目录
skillsync list-dirs         # 列出所有目录
skillsync remove-dir <path> # 移除目录
```

## 工作原理

### 自动检测目录

**Claude Code:**
- `~/.claude/skills/` (全局)
- `.claude/skills/` (项目级)
- `~/.claude/commands/` (旧版)

**OpenClaw:**
- `~/.openclaw/workspace/skills/`
- 配置的额外目录

**自定义:**
- 通过 `skillsync add-dir` 添加的目录

### 同步流程

```
本地 Skills → 检测变化 → 推送到 GitHub
     ↑                           ↓
     └────── 拉取远程更新 ←──────┘
```

### 后台守护进程

启动后，每 5 分钟（可配置）自动执行：
1. 从远程拉取更新
2. 推送本地变化
3. 记录日志

## 使用场景

### 场景 1: 个人多机器同步

```bash
# 机器 A (工作电脑)
skillsync init
skillsync sync
skillsync start

# 机器 B (家里电脑)
skillsync init  # 配置同一个 GitHub repo
skillsync pull
skillsync start

# 现在两台机器会自动保持同步
```

### 场景 2: 团队协作

```bash
# 团队成员 A
skillsync init --repo team/shared-skills
skillsync sync

# 团队成员 B
skillsync init --repo team/shared-skills
skillsync pull
```

### 场景 3: 版本对比

```bash
# 查看哪些 skills 有变化
skillsync diff

# 输出示例:
# claude-code/commit    ✓ 已同步
# claude-code/pr-review ↑ 本地更新
# openclaw/api-docs     ↓ 远程更新
```

## 配置文件

### 配置文件位置

```
~/.skillsync/
├── config.json          # 配置
├── metadata.json        # 元数据
├── daemon.pid           # 守护进程 PID
├── daemon.state         # 守护进程状态
└── sync.log             # 同步日志
```

### config.json 示例

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

## GitHub 仓库结构

同步后的 GitHub 仓库结构：

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

## 故障排查

### 问题 1: 找不到 skills

```bash
# 检查扫描结果
skillsync scan

# 添加自定义目录
skillsync add-dir /path/to/your/skills
```

### 问题 2: GitHub 连接失败

```bash
# 重新初始化
skillsync init

# 检查 token 权限（需要 repo 权限）
```

### 问题 3: 后台同步不工作

```bash
# 停止并重启
skillsync stop
skillsync start

# 查看日志
skillsync logs
```

## 卸载

### 快速卸载

```bash
skillsync uninstall
```

这将会：
1. 停止后台守护进程（如果正在运行）
2. 询问是否删除配置文件
3. 卸载 skillsync 包

### 手动卸载

```bash
# 停止守护进程
skillsync stop

# 卸载包
pip uninstall skillsync

# 可选：删除配置
rm -rf ~/.skillsync
```

### 卸载后会怎样？

| 项目 | 卸载后状态 | 说明 |
|------|-----------|------|
| GitHub 远程仓库 | ✅ 保留 | 所有已同步的 skills 安全保存 |
| 本地 Skills 文件 | ✅ 保留 | ~/.claude/skills/ 不受影响 |
| SkillSync 配置 | ❌ 删除 | ~/.skillsync/ 配置目录（可选） |
| SkillSync 程序 | ❌ 删除 | pip 包被卸载 |

**重要说明：**
- 你的数据是安全的（本地 + GitHub 双备份）
- 可以随时重新安装并恢复同步
- 即使卸载，也可以直接访问 GitHub 仓库查看/下载 skills
- 多台机器可以共享同一个 GitHub 仓库

**重新安装后恢复：**
```bash
# 重新安装
pip install git+https://github.com/verycafe/skillsync.git

# 重新连接到你的仓库
skillsync init  # 使用相同的 token 和仓库名

# 拉取你的 skills
skillsync pull
```

## 开发

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/verycafe/skillsync.git
cd skillsync

# 安装依赖
pip install -e .

# 运行测试
python test_cli.py scan
```

### 项目结构

```
skillsync/
├── skillsync/
│   ├── cli.py           # CLI 接口
│   ├── scanner.py       # 扫描器
│   ├── syncer.py        # 同步器
│   ├── daemon.py        # 守护进程
│   └── cloud/
│       └── github.py    # GitHub 集成
├── install.sh           # macOS/Linux 安装脚本
├── install.ps1          # Windows 安装脚本
└── README.md            # 文档
```

## 技术栈

- **语言**: Python 3.8+
- **CLI 框架**: Click
- **终端美化**: Rich
- **文件监听**: Watchdog
- **GitHub API**: PyGithub
- **配置**: YAML/JSON

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 相关链接

- [GitHub 仓库](https://github.com/verycafe/skillsync)
- [问题反馈](https://github.com/verycafe/skillsync/issues)
- [快速开始指南](QUICKSTART.md)
- [使用示例](EXAMPLES.md)
- [开发文档](DEVELOPMENT.md)

## 致谢

感谢使用 SkillSync！

如果觉得有用，请给个 Star ⭐
