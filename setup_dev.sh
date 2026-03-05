#!/bin/bash
# 本地开发环境设置脚本

echo "🔧 设置 SkillSync 开发环境..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装"
    exit 1
fi

echo "✓ Python: $(python3 --version)"

# 安装依赖
echo ""
echo "📦 安装依赖..."
pip3 install click rich watchdog PyGithub pyyaml requests

echo ""
echo "✅ 开发环境设置完成！"
echo ""
echo "现在可以运行:"
echo "  python3 test_cli.py --help"
echo "  python3 test_cli.py scan"
