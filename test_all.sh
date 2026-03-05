#!/bin/bash
# SkillSync 完整测试脚本

echo "🧪 SkillSync 功能测试"
echo "===================="
echo ""

# 测试 1: 帮助命令
echo "✓ 测试 1: 帮助命令"
python3 test_cli.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "  ✅ 通过"
else
    echo "  ❌ 失败"
    exit 1
fi

# 测试 2: 版本命令
echo "✓ 测试 2: 版本命令"
python3 test_cli.py --version > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "  ✅ 通过"
else
    echo "  ❌ 失败"
    exit 1
fi

# 测试 3: 扫描命令
echo "✓ 测试 3: 扫描命令"
python3 test_cli.py scan > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "  ✅ 通过"
else
    echo "  ❌ 失败"
    exit 1
fi

echo ""
echo "🎉 所有测试通过！"
echo ""
echo "项目已准备就绪，可以发布到 GitHub。"
