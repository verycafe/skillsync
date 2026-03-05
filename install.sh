#!/bin/bash
set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
   _____ _    _ _ _  _____
  / ____| |  (_) | |/ ____|
 | (___ | | ___| | | (___  _   _ _ __   ___
  \___ \| |/ / | | |\___ \| | | | '_ \ / __|
  ____) |   <| | | |____) | |_| | | | | (__
 |_____/|_|\_\_|_|_|_____/ \__, |_| |_|\___|
                            __/ |
                           |___/
EOF
echo -e "${NC}"

echo -e "${GREEN}SkillSync Installer${NC}"
echo ""

# 检测操作系统
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM="Linux";;
    Darwin*)    PLATFORM="macOS";;
    *)
        echo -e "${RED}✗ Unsupported OS: ${OS}${NC}"
        exit 1
        ;;
esac

echo -e "Platform: ${GREEN}${PLATFORM}${NC}"

# 检测 Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version | cut -d' ' -f2)
else
    echo -e "${RED}✗ Python not found${NC}"
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

echo -e "Python: ${GREEN}${PYTHON_VERSION}${NC}"

# 检查 Python 版本
PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo -e "${RED}✗ Python 3.8+ required (found ${PYTHON_VERSION})${NC}"
    exit 1
fi

# 检测 pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo -e "${YELLOW}⚠ pip not found, installing...${NC}"
    $PYTHON_CMD -m ensurepip --upgrade
fi

PIP_CMD=$(command -v pip3 || command -v pip)

echo ""
echo -e "${YELLOW}Installing SkillSync...${NC}"

# 安装方式 1: 从 PyPI 安装（发布后）
# $PIP_CMD install --upgrade skillsync

# 安装方式 2: 从 GitHub 安装（开发阶段）
$PIP_CMD install --upgrade git+https://github.com/yourusername/skillsync.git

# 验证安装
if command -v skillsync &> /dev/null; then
    echo ""
    echo -e "${GREEN}✓ SkillSync installed successfully!${NC}"
    echo ""

    # 首次配置
    echo -e "${BLUE}Starting initial setup...${NC}"
    skillsync init

    echo ""
    echo -e "${GREEN}Setup complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. skillsync start    # 启动后台同步"
    echo "  2. skillsync status   # 查看状态"
    echo ""
    echo "Run 'skillsync --help' for more commands"
else
    echo -e "${RED}✗ Installation failed${NC}"
    exit 1
fi
