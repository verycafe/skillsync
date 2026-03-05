# SkillSync 项目结构

```
skillsync/
│
├── 📄 核心代码
│   └── skillsync/
│       ├── __init__.py              # 包初始化
│       ├── cli.py                   # CLI 接口 (16 个命令)
│       ├── scanner.py               # 扫描器 (多平台支持)
│       ├── syncer.py                # 同步器 (push/pull/diff)
│       ├── daemon.py                # 后台守护进程
│       └── cloud/
│           ├── __init__.py
│           └── github.py            # GitHub 存储后端
│
├── 📦 安装脚本
│   ├── install.sh                   # macOS/Linux 一键安装
│   ├── install.ps1                  # Windows 一键安装
│   └── setup_dev.sh                 # 开发环境设置
│
├── 🧪 测试工具
│   └── test_cli.py                  # 本地测试脚本
│
├── ⚙️ 配置文件
│   ├── pyproject.toml               # 项目配置和依赖
│   └── .gitignore                   # Git 忽略规则
│
├── 📚 文档
│   ├── README.md                    # 用户文档
│   ├── QUICKSTART.md                # 快速开始指南
│   ├── DEVELOPMENT.md               # 开发指南
│   ├── EXAMPLES.md                  # 使用示例
│   ├── PROJECT_SUMMARY.md           # 项目总结
│   ├── NEXT_STEPS.md                # 下一步操作
│   └── STRUCTURE.md                 # 本文件
│
└── 📄 许可证
    └── LICENSE                      # MIT 许可证
```

## 文件说明

### 核心代码 (skillsync/)

| 文件 | 行数 | 功能 |
|------|------|------|
| `cli.py` | ~400 | 16 个 CLI 命令，完整的用户交互 |
| `scanner.py` | ~300 | 扫描 Claude Code 和 OpenClaw 目录 |
| `syncer.py` | ~250 | 同步逻辑，版本对比，冲突检测 |
| `daemon.py` | ~150 | 后台守护进程，自动定时同步 |
| `cloud/github.py` | ~200 | GitHub API 集成，上传下载 |

**总计**: ~1300 行核心代码

### 安装脚本

| 文件 | 功能 |
|------|------|
| `install.sh` | macOS/Linux 一键安装脚本 |
| `install.ps1` | Windows PowerShell 安装脚本 |
| `setup_dev.sh` | 本地开发环境快速设置 |

### 测试工具

| 文件 | 功能 |
|------|------|
| `test_cli.py` | 本地测试脚本，无需安装即可运行 |

### 配置文件

| 文件 | 功能 |
|------|------|
| `pyproject.toml` | Python 项目配置，依赖管理 |
| `.gitignore` | Git 忽略规则 |

### 文档

| 文件 | 内容 |
|------|------|
| `README.md` | 用户文档，功能介绍，安装方法 |
| `QUICKSTART.md` | 快速开始，测试方法，发布流程 |
| `DEVELOPMENT.md` | 开发指南，命令速查，配置说明 |
| `EXAMPLES.md` | 使用示例，场景演示 |
| `PROJECT_SUMMARY.md` | 项目总结，功能清单，技术栈 |
| `NEXT_STEPS.md` | 下一步操作，发布流程 |
| `STRUCTURE.md` | 项目结构说明（本文件）|

## 运行时文件

用户使用时会在 `~/.skillsync/` 创建：

```
~/.skillsync/
├── config.json          # 用户配置
├── metadata.json        # Skills 元数据
├── daemon.pid           # 守护进程 PID
├── daemon.state         # 守护进程状态
└── sync.log             # 同步日志
```

## GitHub 仓库结构

同步后的 GitHub 仓库结构：

```
my-skills/
├── README.md
├── claude-code/
│   ├── skill-1/
│   │   └── SKILL.md
│   ├── skill-2/
│   │   ├── SKILL.md
│   │   └── scripts/
│   └── skill-3/
│       └── SKILL.md
└── openclaw/
    ├── skill-a/
    │   └── SKILL.md
    └── skill-b/
        └── SKILL.md
```

## 依赖关系

```
skillsync
├── click (CLI 框架)
├── rich (终端美化)
├── watchdog (文件监听)
├── PyGithub (GitHub API)
├── pyyaml (YAML 解析)
└── requests (HTTP 请求)
```

## 代码流程

```
用户命令
    ↓
cli.py (解析命令)
    ↓
scanner.py (扫描本地 skills)
    ↓
syncer.py (计算差异)
    ↓
cloud/github.py (上传/下载)
    ↓
更新 metadata.json
```

## 后台守护进程流程

```
daemon.py 启动
    ↓
每 N 分钟循环:
    ↓
1. syncer.pull_remote_changes()
    ↓
2. scanner.scan_all()
    ↓
3. syncer.sync_skill() (for each)
    ↓
4. 记录日志
    ↓
5. 更新状态
    ↓
sleep(interval)
```

## 文件大小统计

```
核心代码:     ~1300 行
安装脚本:     ~200 行
文档:         ~1500 行
配置:         ~100 行
----------------------------
总计:         ~3100 行
```

## 项目特点

✅ 模块化设计
✅ 清晰的职责分离
✅ 完整的文档
✅ 易于测试
✅ 易于扩展
✅ 跨平台支持

---

**最后更新**: 2026-03-05
