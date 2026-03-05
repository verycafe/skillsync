#!/usr/bin/env python3
"""扫描本地所有 AI Skills"""

from pathlib import Path
import hashlib
import json
import os
from typing import List, Dict, Optional

class SkillScanner:
    def __init__(self, custom_dirs: List[str] = None):
        self.custom_dirs = custom_dirs or []
        self.claude_code_paths = self._get_claude_code_paths()
        self.openclaw_paths = self._get_openclaw_paths()

    def _get_claude_code_paths(self) -> List[tuple]:
        """获取所有 Claude Code skills 目录"""
        paths = []

        # 1. 个人全局目录
        global_skills = Path.home() / '.claude' / 'skills'
        if global_skills.exists():
            paths.append(('global', global_skills))

        # 2. 个人全局 commands（旧版）
        global_commands = Path.home() / '.claude' / 'commands'
        if global_commands.exists():
            paths.append(('global-commands', global_commands))

        # 3. 当前项目目录
        project_skills = Path.cwd() / '.claude' / 'skills'
        if project_skills.exists():
            paths.append(('project', project_skills))

        # 4. 当前项目 commands（旧版）
        project_commands = Path.cwd() / '.claude' / 'commands'
        if project_commands.exists():
            paths.append(('project-commands', project_commands))

        # 5. 企业级目录（通过环境变量）
        enterprise_dir = os.getenv('CLAUDE_ENTERPRISE_SKILLS_DIR')
        if enterprise_dir:
            enterprise_path = Path(enterprise_dir)
            if enterprise_path.exists():
                paths.append(('enterprise', enterprise_path))

        # 6. 自定义目录
        for custom_dir in self.custom_dirs:
            custom_path = Path(custom_dir)
            if custom_path.exists():
                # 检查是否是 .claude/skills 目录
                if custom_path.name == 'skills' and custom_path.parent.name == '.claude':
                    paths.append(('custom', custom_path))
                else:
                    # 尝试查找子目录中的 .claude/skills
                    claude_skills = custom_path / '.claude' / 'skills'
                    if claude_skills.exists():
                        paths.append(('custom', claude_skills))

        return paths

    def _get_openclaw_paths(self) -> List[tuple]:
        """获取所有 OpenClaw skills 目录"""
        paths = []

        # 1. 标准 workspace 目录
        workspace_skills = Path.home() / '.openclaw' / 'workspace' / 'skills'
        if workspace_skills.exists():
            paths.append(('workspace', workspace_skills))

        # 2. 读取 openclaw.json 配置的额外目录
        openclaw_config = Path.home() / '.openclaw' / 'openclaw.json'
        if openclaw_config.exists():
            try:
                config = json.loads(openclaw_config.read_text())
                extra_dirs = config.get('skills', {}).get('load', {}).get('extraDirs', [])

                for extra_dir in extra_dirs:
                    extra_path = Path(extra_dir)
                    if extra_path.exists():
                        paths.append(('extra', extra_path))
            except Exception as e:
                print(f"Warning: Failed to read OpenClaw config: {e}")

        # 3. 自定义目录
        for custom_dir in self.custom_dirs:
            custom_path = Path(custom_dir)
            if custom_path.exists() and 'openclaw' in str(custom_path).lower():
                paths.append(('custom', custom_path))

        return paths

    def scan_all(self) -> List[Dict]:
        """扫描所有 skills"""
        all_skills = []
        seen_skills = {}  # skill_key -> skill_info (用于去重和优先级)

        # 定义优先级（数字越小优先级越高）
        priority_map = {
            'enterprise': 1,
            'global': 2,
            'workspace': 2,
            'project': 3,
            'custom': 4,
            'extra': 5,
            'global-commands': 6,
            'project-commands': 7
        }

        # 扫描 Claude Code
        for scope, base_path in self.claude_code_paths:
            skills = self._scan_directory(base_path, 'claude-code', scope)
            for skill in skills:
                skill_key = f"claude-code/{skill['name']}"
                current_priority = priority_map.get(scope, 99)

                if skill_key not in seen_skills:
                    skill['priority'] = current_priority
                    seen_skills[skill_key] = skill
                else:
                    # 如果当前优先级更高，替换
                    if current_priority < seen_skills[skill_key]['priority']:
                        skill['priority'] = current_priority
                        seen_skills[skill_key] = skill

        # 扫描 OpenClaw
        for scope, base_path in self.openclaw_paths:
            skills = self._scan_directory(base_path, 'openclaw', scope)
            for skill in skills:
                skill_key = f"openclaw/{skill['name']}"
                current_priority = priority_map.get(scope, 99)

                if skill_key not in seen_skills:
                    skill['priority'] = current_priority
                    seen_skills[skill_key] = skill
                else:
                    if current_priority < seen_skills[skill_key]['priority']:
                        skill['priority'] = current_priority
                        seen_skills[skill_key] = skill

        # 转换为列表
        all_skills = list(seen_skills.values())

        return all_skills

    def _scan_directory(self, base_path: Path, platform: str, scope: str) -> List[Dict]:
        """扫描单个目录"""
        skills = []

        if not base_path.exists():
            return skills

        try:
            for item in base_path.iterdir():
                try:
                    if not item.is_dir():
                        # 检查是否是旧版 commands 的单文件格式
                        if item.suffix == '.md' and scope.endswith('commands'):
                            skill_info = self._parse_single_file_skill(item, platform, scope)
                            if skill_info:
                                skills.append(skill_info)
                        continue

                    # 检查是否包含 SKILL.md
                    skill_md = item / 'SKILL.md'
                    if not skill_md.exists():
                        continue

                    skill_info = self._parse_skill(item, platform, scope)
                    if skill_info:
                        skills.append(skill_info)
                except PermissionError:
                    print(f"Warning: Permission denied: {item}")
                    continue
        except PermissionError:
            print(f"Warning: Cannot access directory: {base_path}")

        return skills

    def _parse_skill(self, skill_dir: Path, platform: str, scope: str) -> Optional[Dict]:
        """解析 skill 目录"""
        skill_md = skill_dir / 'SKILL.md'

        try:
            content = skill_md.read_text(encoding='utf-8')

            # 解析 frontmatter
            frontmatter = self._parse_frontmatter(content)

            # 获取 skill 名称
            name = frontmatter.get('name', skill_dir.name)

            # 列出所有文件
            files = [
                str(f.relative_to(skill_dir))
                for f in skill_dir.rglob('*')
                if f.is_file()
            ]

            # 计算 checksum
            checksum = self._calculate_checksum(skill_dir)

            return {
                'name': name,
                'platform': platform,
                'scope': scope,
                'path': skill_dir,
                'files': files,
                'checksum': checksum,
                'frontmatter': frontmatter,
                'single_file': False
            }
        except Exception as e:
            print(f"Warning: Failed to parse {skill_dir}: {e}")
            return None

    def _parse_single_file_skill(self, file_path: Path, platform: str, scope: str) -> Optional[Dict]:
        """解析单文件 skill（旧版 commands）"""
        try:
            content = file_path.read_text(encoding='utf-8')
            frontmatter = self._parse_frontmatter(content)

            name = frontmatter.get('name', file_path.stem)

            return {
                'name': name,
                'platform': platform,
                'scope': scope,
                'path': file_path.parent,
                'files': [file_path.name],
                'checksum': hashlib.sha256(content.encode()).hexdigest(),
                'frontmatter': frontmatter,
                'single_file': True
            }
        except Exception as e:
            print(f"Warning: Failed to parse {file_path}: {e}")
            return None

    def _parse_frontmatter(self, content: str) -> Dict:
        """解析 YAML frontmatter"""
        if not content.startswith('---'):
            return {}

        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}

            import yaml
            return yaml.safe_load(parts[1]) or {}
        except:
            return {}

    def _calculate_checksum(self, skill_dir: Path) -> str:
        """计算目录的 SHA256 checksum"""
        hasher = hashlib.sha256()

        # 按文件名排序，确保一致性
        files = sorted(skill_dir.rglob('*'))

        for file in files:
            if file.is_file():
                # 添加文件路径（相对路径）
                rel_path = file.relative_to(skill_dir)
                hasher.update(str(rel_path).encode())

                # 添加文件内容
                try:
                    hasher.update(file.read_bytes())
                except:
                    pass

        return hasher.hexdigest()

    def get_stats(self) -> Dict:
        """获取统计信息"""
        skills = self.scan_all()

        stats = {
            'total': len(skills),
            'by_platform': {},
            'by_scope': {}
        }

        for skill in skills:
            platform = skill['platform']
            scope = skill['scope']

            stats['by_platform'][platform] = stats['by_platform'].get(platform, 0) + 1
            stats['by_scope'][scope] = stats['by_scope'].get(scope, 0) + 1

        return stats
