#!/usr/bin/env python3
"""后台守护进程"""

import time
import threading
from pathlib import Path
import json
from datetime import datetime
import os
import signal

class SkillSyncDaemon:
    def __init__(self, config):
        self.config = config
        self.pid_file = Path.home() / '.skillsync' / 'daemon.pid'
        self.log_file = Path.home() / '.skillsync' / 'sync.log'
        self.state_file = Path.home() / '.skillsync' / 'daemon.state'
        self.running = False
        self.thread = None

    def is_running(self) -> bool:
        """检查守护进程是否运行"""
        if not self.pid_file.exists():
            return False

        try:
            pid = int(self.pid_file.read_text())
            # 检查进程是否存在
            os.kill(pid, 0)
            return True
        except (OSError, ValueError):
            # 进程不存在，清理 PID 文件
            self.pid_file.unlink(missing_ok=True)
            return False

    def start(self):
        """启动守护进程"""
        if self.is_running():
            print("Daemon already running")
            return

        # 保存 PID
        self.pid_file.parent.mkdir(parents=True, exist_ok=True)
        self.pid_file.write_text(str(os.getpid()))

        # 启动后台线程
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

        self._log("Daemon started")

    def stop(self):
        """停止守护进程"""
        self.running = False
        if self.pid_file.exists():
            self.pid_file.unlink()
        self._log("Daemon stopped")

    def _run_loop(self):
        """主循环 - 双向同步"""
        from .scanner import SkillScanner
        from .syncer import SkillSyncer
        from .cloud.github import GitHubStorage

        storage = GitHubStorage(
            self.config['github']['token'],
            self.config['github']['repo']
        )

        custom_dirs = self.config.get('custom_dirs', [])
        syncer = SkillSyncer(storage)
        scanner = SkillScanner(custom_dirs)

        interval = self.config.get('sync_interval', 5) * 60  # 转换为秒

        while self.running:
            try:
                self._log("=== Sync cycle started ===")

                # 1. 先拉取远程更新（PULL）
                self._log("Pulling remote changes...")
                remote_changes = syncer.pull_remote_changes()

                if remote_changes:
                    self._log(f"Pulled {len(remote_changes)} changes:")
                    for change in remote_changes:
                        self._log(f"  ← {change['skill']} ({change['reason']})")
                else:
                    self._log("No remote changes")

                # 2. 再推送本地更新（PUSH）
                self._log("Pushing local changes...")
                skills = scanner.scan_all()
                pushed_count = 0

                for skill in skills:
                    if syncer.needs_sync(skill):
                        if syncer.sync_skill(skill):
                            pushed_count += 1
                            self._log(f"  → {skill['platform']}/{skill['name']}")

                if pushed_count == 0:
                    self._log("No local changes")
                else:
                    self._log(f"Pushed {pushed_count} changes")

                self._log(f"=== Sync cycle complete ===")
                self._update_state(pushed_count, len(remote_changes), len(skills))

            except Exception as e:
                self._log(f"Error: {e}")

            # 等待下一个周期
            time.sleep(interval)

    def _log(self, message: str):
        """写入日志"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")

    def _update_state(self, pushed: int, pulled: int, total: int):
        """更新状态"""
        state = {
            'last_sync': datetime.now().isoformat(),
            'pushed': pushed,
            'pulled': pulled,
            'total': total
        }
        self.state_file.write_text(json.dumps(state, indent=2))

    def get_last_sync_time(self) -> str:
        """获取上次同步时间"""
        if not self.state_file.exists():
            return None

        try:
            state = json.loads(self.state_file.read_text())
            return state.get('last_sync')
        except:
            return None

    def get_state(self) -> dict:
        """获取守护进程状态"""
        if not self.state_file.exists():
            return {}

        try:
            return json.loads(self.state_file.read_text())
        except:
            return {}
