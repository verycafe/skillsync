#!/usr/bin/env python3
"""命令行接口"""

import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress
from pathlib import Path
import json
import sys

from .scanner import SkillScanner
from .syncer import SkillSyncer
from .daemon import SkillSyncDaemon
from .cloud.github import GitHubStorage

console = Console()
CONFIG_FILE = Path.home() / '.skillsync' / 'config.json'

def load_config():
    """加载配置"""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except:
            return None
    return None

def save_config(config):
    """保存配置"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))

@click.group()
@click.version_option(version='1.0.0')
def main():
    """
    SkillSync - 自动同步你的 AI Skills

    \b
    快速开始:
      1. skillsync init          # 初始化配置
      2. skillsync scan          # 扫描本地 skills
      3. skillsync sync          # 双向同步
      4. skillsync start         # 启动后台自动同步
    """
    pass

@main.command()
def init():
    """初始化配置"""
    console.print("\n[bold cyan]🚀 SkillSync Setup[/bold cyan]\n")

    # 检测本地 skills
    scanner = SkillScanner()
    skills = scanner.scan_all()

    if skills:
        console.print(f"[green]✓ 发现 {len(skills)} 个本地 skills[/green]")
        for skill in skills[:3]:
            console.print(f"  • [{skill['platform']}] {skill['name']}")
        if len(skills) > 3:
            console.print(f"  ... 还有 {len(skills) - 3} 个")
    else:
        console.print("[yellow]⚠ 未发现本地 skills[/yellow]")

    console.print()

    # GitHub 配置
    console.print("[bold]GitHub 配置[/bold]")
    console.print("需要一个 GitHub Personal Access Token (权限: repo)")
    console.print("创建地址: https://github.com/settings/tokens/new\n")

    token = Prompt.ask("GitHub Token", password=True)
    repo = Prompt.ask("目标仓库 (例如: yourname/my-skills)")

    # 同步间隔
    interval = Prompt.ask("同步间隔 (分钟)", default="5")

    config = {
        'github': {
            'token': token,
            'repo': repo
        },
        'sync_interval': int(interval),
        'custom_dirs': []
    }

    # 测试连接
    console.print("\n[yellow]测试 GitHub 连接...[/yellow]")
    try:
        storage = GitHubStorage(token, repo)
        storage.test_connection()
        console.print("[green]✓ 连接成功[/green]")
    except Exception as e:
        console.print(f"[red]✗ 连接失败: {e}[/red]")
        if not Confirm.ask("是否仍要保存配置?"):
            return

    save_config(config)
    console.print("\n[green]✓ 配置已保存到 ~/.skillsync/config.json[/green]")

    # 询问是否立即同步
    if skills and Confirm.ask("\n是否立即同步到 GitHub?", default=True):
        ctx = click.get_current_context()
        ctx.invoke(sync)

    # 询问是否启动后台守护进程
    if Confirm.ask("\n是否启动后台自动同步?", default=True):
        ctx = click.get_current_context()
        ctx.invoke(start)

@main.command()
def scan():
    """扫描本地 skills"""
    config = load_config()
    custom_dirs = config.get('custom_dirs', []) if config else []

    scanner = SkillScanner(custom_dirs)

    # 显示检测到的目录
    console.print("\n[bold cyan]检测到的目录:[/bold cyan]\n")

    console.print("[bold]Claude Code:[/bold]")
    if scanner.claude_code_paths:
        for scope, path in scanner.claude_code_paths:
            console.print(f"  [{scope}] {path}")
    else:
        console.print("  [dim]未找到[/dim]")

    console.print("\n[bold]OpenClaw:[/bold]")
    if scanner.openclaw_paths:
        for scope, path in scanner.openclaw_paths:
            console.print(f"  [{scope}] {path}")
    else:
        console.print("  [dim]未找到[/dim]")

    # 扫描 skills
    skills = scanner.scan_all()

    if not skills:
        console.print("\n[yellow]⚠ 未找到任何 skills[/yellow]")
        return

    # 显示统计
    stats = scanner.get_stats()
    console.print(f"\n[bold green]发现 {stats['total']} 个 skills[/bold green]")

    # 按平台分组显示
    table = Table(title="Skills 列表")
    table.add_column("Platform", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Scope", style="yellow")
    table.add_column("Files", justify="right")
    table.add_column("Path", style="dim")

    for skill in skills:
        table.add_row(
            skill['platform'],
            skill['name'],
            skill['scope'],
            str(len(skill['files'])),
            str(skill['path'])
        )

    console.print(table)

    # 显示统计信息
    console.print("\n[bold]统计:[/bold]")
    for platform, count in stats['by_platform'].items():
        console.print(f"  {platform}: {count}")

@main.command()
def status():
    """查看同步状态"""
    config = load_config()
    if not config:
        console.print("[red]✗ 未配置，请先运行 'skillsync init'[/red]")
        return

    daemon = SkillSyncDaemon(config)

    # 守护进程状态
    console.print()
    if daemon.is_running():
        console.print("[green]● 后台同步: 运行中[/green]")
        state = daemon.get_state()
        if state:
            console.print(f"  上次同步: {state.get('last_sync', 'N/A')}")
            console.print(f"  推送: {state.get('pushed', 0)} | 拉取: {state.get('pulled', 0)}")
    else:
        console.print("[dim]○ 后台同步: 未运行[/dim]")

    console.print()

    # Skills 状态
    custom_dirs = config.get('custom_dirs', [])
    scanner = SkillScanner(custom_dirs)
    storage = GitHubStorage(config['github']['token'], config['github']['repo'])
    syncer = SkillSyncer(storage)
    skills = scanner.scan_all()

    table = Table(title="Skills 状态")
    table.add_column("Platform", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Status")
    table.add_column("Version", justify="right")

    for skill in skills:
        skill_id = f"{skill['platform']}/{skill['name']}"
        meta = syncer.get_metadata(skill_id)

        if meta:
            if meta['checksum'] == skill['checksum']:
                status = "[green]✓ 已同步[/green]"
            else:
                status = "[yellow]⚠ 有变化[/yellow]"
            version = str(meta.get('version', 0))
        else:
            status = "[red]✗ 未同步[/red]"
            version = "0"

        table.add_row(skill['platform'], skill['name'], status, version)

    console.print(table)

@main.command()
@click.option('--force', is_flag=True, help='强制推送所有')
def push(force):
    """推送本地更新到远程"""
    config = load_config()
    if not config:
        console.print("[red]✗ 请先运行 'skillsync init'[/red]")
        return

    storage = GitHubStorage(config['github']['token'], config['github']['repo'])
    syncer = SkillSyncer(storage)
    custom_dirs = config.get('custom_dirs', [])
    scanner = SkillScanner(custom_dirs)

    skills = scanner.scan_all()

    if not skills:
        console.print("[yellow]⚠ 未发现 skills[/yellow]")
        return

    console.print(f"\n[cyan]推送 {len(skills)} 个 skills...[/cyan]\n")

    with Progress() as progress:
        task = progress.add_task("[cyan]推送中...", total=len(skills))

        pushed_count = 0
        for skill in skills:
            if force or syncer.needs_sync(skill):
                if syncer.sync_skill(skill, force=force):
                    pushed_count += 1
                    console.print(f"  → {skill['platform']}/{skill['name']}")
            progress.update(task, advance=1)

    console.print(f"\n[green]✓ 已推送 {pushed_count} 个 skills[/green]")

@main.command()
def pull():
    """从远程拉取更新"""
    config = load_config()
    if not config:
        console.print("[red]✗ 请先运行 'skillsync init'[/red]")
        return

    storage = GitHubStorage(config['github']['token'], config['github']['repo'])
    syncer = SkillSyncer(storage)

    console.print("\n[cyan]从远程拉取更新...[/cyan]\n")

    changes = syncer.pull_remote_changes()

    if changes:
        console.print(f"[green]✓ 拉取 {len(changes)} 个更新:[/green]")
        for change in changes:
            console.print(f"  ← {change['skill']} ({change['reason']})")
    else:
        console.print("[green]✓ 已是最新[/green]")

@main.command()
@click.option('--force', is_flag=True, help='强制同步所有')
def sync(force):
    """双向同步（先拉取，再推送）"""
    config = load_config()
    if not config:
        console.print("[red]✗ 请先运行 'skillsync init'[/red]")
        return

    storage = GitHubStorage(config['github']['token'], config['github']['repo'])
    syncer = SkillSyncer(storage)
    custom_dirs = config.get('custom_dirs', [])
    scanner = SkillScanner(custom_dirs)

    console.print("\n[bold cyan]开始双向同步[/bold cyan]\n")

    # 1. 拉取
    console.print("[cyan]1. 从远程拉取更新...[/cyan]")
    changes = syncer.pull_remote_changes()

    if changes:
        console.print(f"  [green]✓ 拉取 {len(changes)} 个更新[/green]")
        for change in changes:
            console.print(f"    ← {change['skill']}")
    else:
        console.print("  [green]✓ 无远程更新[/green]")

    # 2. 推送
    console.print("\n[cyan]2. 推送本地更新...[/cyan]")
    skills = scanner.scan_all()
    pushed_count = 0

    for skill in skills:
        if force or syncer.needs_sync(skill):
            if syncer.sync_skill(skill, force=force):
                pushed_count += 1
                console.print(f"    → {skill['platform']}/{skill['name']}")

    if pushed_count > 0:
        console.print(f"  [green]✓ 推送 {pushed_count} 个更新[/green]")
    else:
        console.print("  [green]✓ 无本地更新[/green]")

    console.print(f"\n[bold green]✓ 同步完成[/bold green]")

@main.command()
@click.argument('skill_id', required=False)
def diff(skill_id):
    """对比本地和远程版本"""
    config = load_config()
    if not config:
        console.print("[red]✗ 请先运行 'skillsync init'[/red]")
        return

    storage = GitHubStorage(config['github']['token'], config['github']['repo'])
    syncer = SkillSyncer(storage)
    custom_dirs = config.get('custom_dirs', [])
    scanner = SkillScanner(custom_dirs)

    skills = scanner.scan_all()

    console.print("\n[cyan]对比版本...[/cyan]\n")

    comparisons = syncer.compare_versions(skills)

    # 过滤特定 skill
    if skill_id:
        comparisons = [c for c in comparisons if c['skill_id'] == skill_id]

    if not comparisons:
        console.print("[yellow]⚠ 未找到匹配的 skills[/yellow]")
        return

    table = Table(title="版本对比")
    table.add_column("Skill", style="cyan")
    table.add_column("Status", style="yellow")
    table.add_column("Local", style="dim")
    table.add_column("Remote", style="dim")

    status_icons = {
        'synced': '[green]✓ 已同步[/green]',
        'local_newer': '[yellow]↑ 本地更新[/yellow]',
        'remote_newer': '[yellow]↓ 远程更新[/yellow]',
        'conflict': '[red]⚠ 冲突[/red]',
        'local_only': '[blue]⊕ 仅本地[/blue]',
        'remote_only': '[blue]⊖ 仅远程[/blue]',
        'different': '[yellow]≠ 不同[/yellow]'
    }

    for comp in comparisons:
        local_hash = comp['local_checksum'][:8] if comp['local_checksum'] else '-'
        remote_hash = comp['remote_checksum'][:8] if comp['remote_checksum'] else '-'

        table.add_row(
            comp['skill_id'],
            status_icons.get(comp['status'], comp['status']),
            local_hash,
            remote_hash
        )

    console.print(table)

@main.command()
def start():
    """启动后台守护进程"""
    config = load_config()
    if not config:
        console.print("[red]✗ 请先运行 'skillsync init'[/red]")
        return

    daemon = SkillSyncDaemon(config)

    if daemon.is_running():
        console.print("[yellow]⚠ 守护进程已在运行[/yellow]")
        return

    daemon.start()
    console.print("[green]✓ 后台同步已启动[/green]")
    console.print(f"同步间隔: {config['sync_interval']} 分钟")
    console.print("\n运行 'skillsync logs' 查看日志")

@main.command()
def stop():
    """停止后台守护进程"""
    config = load_config()
    daemon = SkillSyncDaemon(config)

    if not daemon.is_running():
        console.print("[yellow]⚠ 守护进程未运行[/yellow]")
        return

    daemon.stop()
    console.print("[green]✓ 后台同步已停止[/green]")

@main.command()
@click.option('--tail', '-n', default=50, help='显示最后 N 行')
def logs(tail):
    """查看同步日志"""
    log_file = Path.home() / '.skillsync' / 'sync.log'

    if not log_file.exists():
        console.print("[yellow]⚠ 暂无日志[/yellow]")
        return

    lines = log_file.read_text().splitlines()

    # 显示最后 N 行
    for line in lines[-tail:]:
        console.print(line)

@main.command()
@click.argument('path', type=click.Path(exists=True))
def add_dir(path):
    """添加自定义目录"""
    config = load_config()
    if not config:
        console.print("[red]✗ 请先运行 'skillsync init'[/red]")
        return

    path = str(Path(path).resolve())

    if 'custom_dirs' not in config:
        config['custom_dirs'] = []

    if path in config['custom_dirs']:
        console.print(f"[yellow]⚠ 目录已存在: {path}[/yellow]")
        return

    config['custom_dirs'].append(path)
    save_config(config)

    console.print(f"[green]✓ 已添加目录: {path}[/green]")

@main.command()
def list_dirs():
    """列出所有自定义目录"""
    config = load_config()
    if not config:
        console.print("[red]✗ 请先运行 'skillsync init'[/red]")
        return

    custom_dirs = config.get('custom_dirs', [])

    if not custom_dirs:
        console.print("[yellow]⚠ 未配置自定义目录[/yellow]")
        return

    console.print("\n[bold]自定义目录:[/bold]\n")
    for i, dir_path in enumerate(custom_dirs, 1):
        console.print(f"  {i}. {dir_path}")

@main.command()
@click.argument('path')
def remove_dir(path):
    """移除自定义目录"""
    config = load_config()
    if not config:
        console.print("[red]✗ 请先运行 'skillsync init'[/red]")
        return

    path = str(Path(path).resolve())

    if 'custom_dirs' not in config:
        config['custom_dirs'] = []

    if path not in config['custom_dirs']:
        console.print(f"[yellow]⚠ 目录不存在: {path}[/yellow]")
        return

    config['custom_dirs'].remove(path)
    save_config(config)

    console.print(f"[green]✓ 已移除目录: {path}[/green]")

if __name__ == '__main__':
    main()
