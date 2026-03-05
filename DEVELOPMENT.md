# SkillSync 开发指南

## 项目结构

```
skillsync/
├── skillsync/
│   ├── __init__.py          # 包初始化
│   ├── cli.py               # 命令行接口
│   ├── scanner.py           # 扫描本地 skills
│   ├── syncer.py            # 同步逻辑
│   ├── daemon.py            # 后台守护进程
│   └── cloud/
│       ├── __init__.py
│       └── github.py        # GitHub 存储后端
├── pyproject.toml           # 项目配置
├── README.md                # 用户文档
├── LICENSE                  # MIT 许可证
├── install.sh               # macOS/Linux 安装脚本
├── install.ps1              # Windows 安装脚本
└── .gitignore
```

## 本地开发

### 安装依赖

```bash
cd /Users/tvwoo/Projects/skillsync
pip install -e .
```

### 运行测试

```bash
# 扫描本地 skills
python -m skillsync.cli scan

# 查看帮助
python -m skillsync.cli --help
```

## 功能清单

### ✅ 已实现

1. **扫描功能**
   - 自动检测 Claude Code skills 目录
   - 自动检测 OpenClaw skills 目录
   - 支持自定义目录
   - 智能去重（优先级）

2. **同步功能**
   - 推送到远程 (push)
   - 从远程拉取 (pull)
   - 双向同步 (sync)
   - 版本对比 (diff)

3. **后台守护进程**
   - 自动定时同步
   - 日志记录
   - 状态查询

4. **自定义目录管理**
   - 添加目录 (add-dir)
   - 列出目录 (list-dirs)
   - 移除目录 (remove-dir)

5. **版本控制**
   - Checksum 计算
   - 冲突检测
   - 元数据管理

## 命令速查

```bash
# 初始化
skillsync init

# 扫描
skillsync scan

# 状态
skillsync status

# 同步
skillsync push              # 推送
skillsync pull              # 拉取
skillsync sync              # 双向同步

# 版本对比
skillsync diff              # 对比所有
skillsync diff claude-code/my-skill  # 对比特定 skill

# 后台守护进程
skillsync start             # 启动
skillsync stop              # 停止
skillsync logs              # 查看日志

# 自定义目录
skillsync add-dir /path/to/dir
skillsync list-dirs
skillsync remove-dir /path/to/dir
```

## 发布流程

### 1. 构建包

```bash
python -m build
```

### 2. 上传到 PyPI

```bash
python -m twine upload dist/*
```

### 3. 创建 GitHub Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

## 配置文件

位置: `~/.skillsync/config.json`

```json
{
  "github": {
    "token": "ghp_xxx",
    "repo": "user/my-skills"
  },
  "sync_interval": 5,
  "custom_dirs": [
    "/path/to/custom/skills"
  ]
}
```

## 元数据文件

位置: `~/.skillsync/metadata.json`

```json
{
  "skills": {
    "claude-code/my-skill": {
      "checksum": "abc123...",
      "last_synced": "2026-03-05T10:30:00Z",
      "source": "local",
      "version": 3
    }
  }
}
```
