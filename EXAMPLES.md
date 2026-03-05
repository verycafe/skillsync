# SkillSync 使用示例

## 场景 1: 首次使用

```bash
# 1. 安装
curl -fsSL https://raw.githubusercontent.com/yourname/skillsync/main/install.sh | bash

# 2. 初始化（会自动引导配置）
skillsync init

# 输入:
# - GitHub Token: ghp_xxxxxxxxxxxx
# - 仓库: yourname/my-skills
# - 同步间隔: 5 (分钟)

# 3. 查看扫描结果
skillsync scan

# 4. 首次同步
skillsync sync

# 5. 启动后台自动同步
skillsync start
```

## 场景 2: 日常使用

```bash
# 查看状态
skillsync status

# 输出:
# ● 后台同步: 运行中
#   上次同步: 2026-03-05T10:30:00Z
#   推送: 2 | 拉取: 1
#
# ┏━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
# ┃ Platform    ┃ Name      ┃ Status   ┃ Version ┃
# ┡━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
# │ claude-code │ commit    │ ✓ 已同步 │ 3       │
# │ claude-code │ pr-review │ ⚠ 有变化 │ 2       │
# └─────────────┴───────────┴──────────┴─────────┘

# 手动推送
skillsync push

# 手动拉取
skillsync pull

# 查看日志
skillsync logs
```

## 场景 3: 版本对比

```bash
# 对比所有 skills
skillsync diff

# 输出:
# ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
# ┃ Skill                 ┃ Status      ┃ Local   ┃ Remote  ┃
# ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━┩
# │ claude-code/commit    │ ✓ 已同步    │ abc123  │ abc123  │
# │ claude-code/pr-review │ ↑ 本地更新  │ def456  │ abc789  │
# │ openclaw/api-docs     │ ↓ 远程更新  │ ghi789  │ jkl012  │
# └───────────────────────┴─────────────┴─────────┴─────────┘

# 对比特定 skill
skillsync diff claude-code/pr-review
```

## 场景 4: 自定义目录

```bash
# 添加自定义目录
skillsync add-dir ~/my-custom-skills

# 列出所有目录
skillsync list-dirs

# 输出:
# 自定义目录:
#   1. /Users/john/my-custom-skills

# 移除目录
skillsync remove-dir ~/my-custom-skills
```

## 场景 5: 多机器同步

```bash
# 机器 A (工作电脑)
skillsync init  # 配置 GitHub repo
skillsync sync  # 首次同步
skillsync start # 启动后台同步

# 修改 skill...
# 5 分钟后自动推送到 GitHub

# 机器 B (家里电脑)
skillsync init  # 配置同一个 GitHub repo
skillsync pull  # 拉取机器 A 的修改
skillsync start # 启动后台同步

# 修改 skill...
# 5 分钟后自动推送到 GitHub
# 机器 A 会在下一个周期自动拉取
```

## 场景 6: 团队协作

```bash
# 团队成员 A
skillsync init --repo team/shared-skills
skillsync sync

# 创建新 skill...
# 自动同步到团队仓库

# 团队成员 B
skillsync init --repo team/shared-skills
skillsync pull  # 拉取团队成员 A 的 skills

# 查看版本对比
skillsync diff

# 修改 skill...
skillsync push
```

## 场景 7: 故障排查

```bash
# 查看日志
skillsync logs

# 查看最后 100 行
skillsync logs -n 100

# 重新初始化
skillsync init

# 强制同步所有
skillsync sync --force

# 停止后台同步
skillsync stop

# 重新启动
skillsync start
```

## 配置文件位置

```
~/.skillsync/
├── config.json          # 配置
├── metadata.json        # 元数据
├── daemon.pid           # 守护进程 PID
├── daemon.state         # 守护进程状态
└── sync.log             # 同步日志
```

## GitHub 仓库结构

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
