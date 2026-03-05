#!/usr/bin/env python3
"""
SkillSync - 快速测试脚本

用于本地开发测试，无需安装
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from skillsync.cli import main

if __name__ == '__main__':
    main()
