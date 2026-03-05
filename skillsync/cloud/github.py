"""GitHub 存储后端"""

from github import Github
from pathlib import Path
import hashlib
from typing import List, Dict

class GitHubStorage:
    def __init__(self, token: str, repo_name: str):
        self.gh = Github(token)
        self.repo = self.gh.get_repo(repo_name)
        self.repo_name = repo_name

    def test_connection(self):
        """测试连接"""
        try:
            self.repo.get_contents("README.md")
        except:
            # README 不存在，尝试创建
            self.repo.create_file(
                "README.md",
                "Initialize repository",
                "# My Skills\n\nAuto-synced by SkillSync"
            )

    def list_all_skills(self) -> List[Dict]:
        """列出远程所有 skills"""
        skills = []

        try:
            # 遍历 claude-code 和 openclaw 目录
            for platform in ['claude-code', 'openclaw']:
                try:
                    contents = self.repo.get_contents(platform)

                    for item in contents:
                        if item.type == "dir":
                            # 这是一个 skill 目录
                            skill_name = item.name
                            checksum = self._calculate_remote_checksum(platform, skill_name)

                            skills.append({
                                'platform': platform,
                                'name': skill_name,
                                'checksum': checksum
                            })
                except:
                    # 目录不存在
                    pass
        except Exception as e:
            print(f"Error listing skills: {e}")

        return skills

    def _calculate_remote_checksum(self, platform: str, name: str) -> str:
        """计算远程 skill 的 checksum"""
        hasher = hashlib.sha256()

        try:
            contents = self.repo.get_contents(f"{platform}/{name}")

            # 递归获取所有文件
            files = self._get_all_files(contents)

            for file_path in sorted(files.keys()):
                hasher.update(file_path.encode())
                hasher.update(files[file_path])

        except Exception as e:
            print(f"Error calculating remote checksum: {e}")

        return hasher.hexdigest()

    def _get_all_files(self, contents) -> Dict[str, bytes]:
        """递归获取所有文件内容"""
        files = {}

        for item in contents:
            if item.type == "file":
                files[item.path] = item.decoded_content
            elif item.type == "dir":
                sub_contents = self.repo.get_contents(item.path)
                files.update(self._get_all_files(sub_contents))

        return files

    def download_skill(self, platform: str, name: str, dest_path: Path):
        """下载 skill 到本地"""
        dest_path.mkdir(parents=True, exist_ok=True)

        try:
            contents = self.repo.get_contents(f"{platform}/{name}")
            self._download_contents(contents, dest_path)
        except Exception as e:
            print(f"Error downloading skill: {e}")
            raise

    def _download_contents(self, contents, dest_path: Path):
        """递归下载内容"""
        for item in contents:
            if item.type == "file":
                file_path = dest_path / item.name
                file_path.write_bytes(item.decoded_content)
            elif item.type == "dir":
                sub_dir = dest_path / item.name
                sub_dir.mkdir(exist_ok=True)
                sub_contents = self.repo.get_contents(item.path)
                self._download_contents(sub_contents, sub_dir)

    def upload_skill(self, platform: str, name: str, local_path: Path):
        """上传 skill 到远程"""
        for file in local_path.rglob('*'):
            if not file.is_file():
                continue

            relative_path = file.relative_to(local_path)
            remote_path = f"{platform}/{name}/{relative_path}"
            content = file.read_bytes()

            try:
                # 尝试更新已存在的文件
                existing = self.repo.get_contents(remote_path)

                # 检查内容是否相同
                if existing.decoded_content == content:
                    continue  # 跳过相同的文件

                self.repo.update_file(
                    remote_path,
                    f"Update {name}/{relative_path}",
                    content,
                    existing.sha
                )
            except:
                # 文件不存在，创建新文件
                self.repo.create_file(
                    remote_path,
                    f"Add {name}/{relative_path}",
                    content
                )
