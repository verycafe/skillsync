# SkillSync - 快速开始

## 🚀 项目已完成！

SkillSync 是一个自动同步 AI Skills (Claude Code & OpenClaw) 到 GitHub 的工具。

## 📁 项目结构

```
skillsync/
├── skillsync/              # 核心代码
│   ├── cli.py             # 命令行接口（所有命令）
│   ├── scanner.py         # 扫描本地 skills
│   ├── syncer.py          # 同步逻辑（push/pull/diff）
│   ├── daemon.py          # 后台守护进程
│   └── cloud/
│       └── github.py      # GitHub 存储后端
├── install.sh             # macOS/Linux 安装脚本
├── install.ps1            # Windows 安装脚本
├── test_cli.py            # 本地测试脚本
├── pyproject.toml         # 项目配置
├── README.md              # 用户文档
├── DEVELOPMENT.md         # 开发指南
└── EXAMPLES.md            # 使用示例
```

## 🎯 核心功能

### ✅ 已实现的功能

1. **自动扫描**
   - Claude Code: `~/.claude/skills/`, `.claude/skills/`, `~/.claude/commands/`
   - OpenClaw: `~/.openclaw/workspace/skills/`
   - 自定义目录支持

2. **双向同步**
   - `skillsync push` - 推送本地更新
   - `skillsync pull` - 拉取远程更新
   - `skillsync sync` - 双向同步（先拉后推）

3. **版本对比**
   - `skillsync diff` - 对比所有 skills
   - `skillsync diff claude-code/my-skill` - 对比特定 skill
   - 显示状态：已同步/本地更新/远程更新/冲突/仅本地/仅远程

4. **后台守护进程**
   - `skillsync start` - 启动自动同步（默认 5 分钟间隔）
   - `skillsync stop` - 停止
   - `skillsync logs` - 查看日志

5. **自定义目录**
   - `skillsync add-dir /path` - 添加目录
   - `skillsync list-dirs` - 列出目录
   - `skillsync remove-dir /path` - 移除目录

6. **状态查询**
   - `skillsync scan` - 扫描本地 skills
   - `skillsync status` - 查看同步状态

## 🧪 本地测试

### 方法 1: 直接运行（推荐用于开发）

```bash
cd /Users/tvwoo/Projects/skillsync

# 查看帮助
python test_cli.py --help

# 扫描本地 skills
python test_cli.py scan

# 初始化配置
python test_cli.py init

# 查看状态
python test_cli.py status
```

### 方法 2: 安装到本地

```bash
cd /Users/tvwoo/Projects/skillsync

# 开发模式安装
pip install -e .

# 现在可以直接使用
skillsync --help
skillsync scan
```

## 📝 完整命令列表

```bash
# 初始化
skillsync init                      # 配置 GitHub token 和仓库

# 扫描
skillsync scan                      # 扫描所有本地 skills

# 状态
skillsync status                    # 查看同步状态

# 同步
skillsync push                      # 推送到远程
skillsync push --force              # 强制推送所有
skillsync pull                      # 从远程拉取
skillsync sync                      # 双向同步
skillsync sync --force              # 强制双向同步

# 版本对比
skillsync diff                      # 对比所有
skillsync diff claude-code/my-skill # 对比特定 skill

# 后台守护进程
skillsync start                     # 启动后台同步
skillsync stop                      # 停止后台同步
skillsync logs                      # 查看日志
skillsync logs -n 100               # 查看最后 100 行

# 自定义目录
skillsync add-dir /path/to/skills   # 添加目录
skillsync list-dirs                 # 列出所有目录
skillsync remove-dir /path          # 移除目录

# 帮助
skillsync --help                    # 查看帮助
skillsync --version                 # 查看版本
```

## 🔧 配置文件

位置: `~/.skillsync/config.json`

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

## 📦 发布到 GitHub

### 1. 创建 GitHub 仓库

```bash
cd /Users/tvwoo/Projects/skillsync
git init
git add .
git commit -m "Initial commit: SkillSync v1.0.0"
git branch -M main
git remote add origin https://github.com/yourusername/skillsync.git
git push -u origin main
```

### 2. 创建 Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 3. 用户安装

用户可以通过以下方式安装：

**macOS/Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/skillsync/main/install.sh | bash
```

**Windows:**
```powershell
irm https://raw.githubusercontent.com/yourusername/skillsync/main/install.ps1 | iex
```

**手动安装:**
```bash
pip install git+https://github.com/yourusername/skillsync.git
```

## 🎬 使用流程示例

### 首次使用

```bash
# 1. 安装（假设已安装）
pip install -e .

# 2. 初始化
skillsync init
# 输入 GitHub Token 和仓库名

# 3. 扫描本地 skills
skillsync scan

# 4. 首次同步
skillsync sync

# 5. 启动后台自动同步
skillsync start
```

### 日常使用

```bash
# 查看状态
skillsync status

# 手动同步
skillsync sync

# 查看版本对比
skillsync diff

# 查看日志
skillsync logs
```

## 🐛 故障排查

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

## 📚 更多文档

- [README.md](README.md) - 用户文档
- [DEVELOPMENT.md](DEVELOPMENT.md) - 开发指南
- [EXAMPLES.md](EXAMPLES.md) - 使用示例

## 🎉 项目特点

✅ 跨平台支持 (macOS/Linux/Windows)
✅ 自动识别 Claude Code 和 OpenClaw
✅ 双向自动同步（PUSH + PULL）
✅ 版本对比和冲突检测
✅ 自定义目录支持
✅ 后台守护进程
✅ 完整的命令行工具
✅ 详细的日志记录

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)
