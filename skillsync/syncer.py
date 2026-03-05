#!/usr/bin/env python3
"""同步逻辑"""

import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class SkillSyncer:
    def __init__(self, storage):
        self.storage = storage
        self.metadata_file = Path.home() / '.skillsync' / 'metadata.json'
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict:
        """加载本地元数据"""
        if self.metadata_file.exists():
            try:
                return json.loads(self.metadata_file.read_text())
            except:
                return {'skills': {}}
        return {'skills': {}}

    def _save_metadata(self):
        """保存元数据"""
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        self.metadata_file.write_text(json.dumps(self.metadata, indent=2))

    def pull_remote_changes(self) -> List[Dict]:
        """从远程拉取更新"""
        changes = []

        if not self.storage:
            return changes

        try:
            # 获取远程所有 skills
            remote_skills = self.storage.list_all_skills()

            for remote_skill in remote_skills:
                platform = remote_skill['platform']
                name = remote_skill['name']
                remote_checksum = remote_skill['checksum']

                # 确定本地路径
                if platform == 'claude-code':
                    local_path = Path.home() / '.claude' / 'skills' / name
                else:
                    local_path = Path.home() / '.openclaw' / 'workspace' / 'skills' / name

                skill_id = f"{platform}/{name}"

                # 检查是否需要更新
                should_pull = False
                reason = ""

                if not local_path.exists():
                    # 本地不存在，直接下载
                    should_pull = True
                    reason = "new"
                else:
                    # 计算本地 checksum
                    local_checksum = self._calculate_checksum(local_path)

                    # 比较 checksum
                    if local_checksum != remote_checksum:
                        # 检查元数据，判断是远程更新还是本地更新
                        if skill_id in self.metadata['skills']:
                            meta_checksum = self.metadata['skills'][skill_id]['checksum']

                            if meta_checksum == local_checksum:
                                # 本地未变，远程有更新
                                should_pull = True
                                reason = "remote_updated"
                            elif meta_checksum == remote_checksum:
                                # 远程未变，本地有更新（稍后会 PUSH）
                                should_pull = False
                            else:
                                # 双方都有更新 - 冲突！
                                should_pull = self._handle_conflict(
                                    skill_id, local_path, remote_skill
                                )
                                reason = "conflict_resolved"
                        else:
                            # 没有元数据，无法判断，默认远程优先
                            should_pull = True
                            reason = "remote_priority"

                if should_pull:
                    # 下载远程版本
                    self.storage.download_skill(platform, name, local_path)

                    # 更新元数据
                    self.metadata['skills'][skill_id] = {
                        'checksum': remote_checksum,
                        'last_synced': datetime.utcnow().isoformat(),
                        'source': 'remote',
                        'version': self.metadata['skills'].get(skill_id, {}).get('version', 0) + 1
                    }

                    changes.append({
                        'skill': skill_id,
                        'action': 'pulled',
                        'reason': reason
                    })

            self._save_metadata()
            return changes

        except Exception as e:
            print(f"Error pulling remote changes: {e}")
            return []

    def _handle_conflict(self, skill_id: str, local_path: Path, remote_skill: Dict) -> bool:
        """处理冲突 - 默认远程优先"""
        # TODO: 可以根据配置选择策略
        # 策略 1: 远程优先（默认）
        return True

        # 策略 2: 本地优先
        # return False

        # 策略 3: 记录冲突，等待用户解决
        # self._record_conflict(skill_id, local_path, remote_skill)
        # return False

    def sync_skill(self, skill_info: Dict, force: bool = False) -> bool:
        """同步单个 skill 到远程（PUSH）"""
        if not self.storage:
            return False

        skill_id = f"{skill_info['platform']}/{skill_info['name']}"

        # 检查是否需要同步
        if not force and skill_id in self.metadata['skills']:
            if self.metadata['skills'][skill_id]['checksum'] == skill_info['checksum']:
                return False  # 无需同步

        try:
            # 上传到远程
            self.storage.upload_skill(
                skill_info['platform'],
                skill_info['name'],
                skill_info['path']
            )

            # 更新元数据
            self.metadata['skills'][skill_id] = {
                'checksum': skill_info['checksum'],
                'last_synced': datetime.utcnow().isoformat(),
                'source': 'local',
                'version': self.metadata['skills'].get(skill_id, {}).get('version', 0) + 1
            }
            self._save_metadata()

            return True
        except Exception as e:
            print(f"Error syncing skill {skill_id}: {e}")
            return False

    def needs_sync(self, skill_info: Dict) -> bool:
        """判断是否需要同步"""
        skill_id = f"{skill_info['platform']}/{skill_info['name']}"

        if skill_id not in self.metadata['skills']:
            return True

        return self.metadata['skills'][skill_id]['checksum'] != skill_info['checksum']

    def get_metadata(self, skill_id: str) -> Optional[Dict]:
        """获取 skill 的元数据"""
        return self.metadata['skills'].get(skill_id)

    def compare_versions(self, local_skills: List[Dict]) -> List[Dict]:
        """对比本地和远程版本"""
        if not self.storage:
            return []

        comparisons = []

        try:
            remote_skills = self.storage.list_all_skills()
            remote_dict = {f"{s['platform']}/{s['name']}": s for s in remote_skills}

            # 对比本地 skills
            for local_skill in local_skills:
                skill_id = f"{local_skill['platform']}/{local_skill['name']}"

                comparison = {
                    'skill_id': skill_id,
                    'name': local_skill['name'],
                    'platform': local_skill['platform'],
                    'local_checksum': local_skill['checksum'],
                    'remote_checksum': None,
                    'status': 'unknown'
                }

                if skill_id in remote_dict:
                    remote_checksum = remote_dict[skill_id]['checksum']
                    comparison['remote_checksum'] = remote_checksum

                    if local_skill['checksum'] == remote_checksum:
                        comparison['status'] = 'synced'
                    else:
                        # 检查元数据判断谁更新
                        meta = self.metadata['skills'].get(skill_id)
                        if meta:
                            if meta['checksum'] == local_skill['checksum']:
                                comparison['status'] = 'remote_newer'
                            elif meta['checksum'] == remote_checksum:
                                comparison['status'] = 'local_newer'
                            else:
                                comparison['status'] = 'conflict'
                        else:
                            comparison['status'] = 'different'
                else:
                    comparison['status'] = 'local_only'

                comparisons.append(comparison)

            # 检查远程独有的 skills
            local_dict = {f"{s['platform']}/{s['name']}": s for s in local_skills}
            for skill_id, remote_skill in remote_dict.items():
                if skill_id not in local_dict:
                    comparisons.append({
                        'skill_id': skill_id,
                        'name': remote_skill['name'],
                        'platform': remote_skill['platform'],
                        'local_checksum': None,
                        'remote_checksum': remote_skill['checksum'],
                        'status': 'remote_only'
                    })

        except Exception as e:
            print(f"Error comparing versions: {e}")

        return comparisons

    def _calculate_checksum(self, skill_dir: Path) -> str:
        """计算目录的 checksum"""
        hasher = hashlib.sha256()

        files = sorted(skill_dir.rglob('*'))

        for file in files:
            if file.is_file():
                rel_path = file.relative_to(skill_dir)
                hasher.update(str(rel_path).encode())
                try:
                    hasher.update(file.read_bytes())
                except:
                    pass

        return hasher.hexdigest()
