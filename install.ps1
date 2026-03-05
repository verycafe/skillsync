# SkillSync Installer for Windows

$ErrorActionPreference = "Stop"

Write-Host @"
   _____ _    _ _ _  _____
  / ____| |  (_) | |/ ____|
 | (___ | | ___| | | (___  _   _ _ __   ___
  \___ \| |/ / | | |\___ \| | | | '_ \ / __|
  ____) |   <| | | |____) | |_| | | | | (__
 |_____/|_|\_\_|_|_|_____/ \__, |_| |_|\___|
                            __/ |
                           |___/
"@ -ForegroundColor Cyan

Write-Host "SkillSync Installer" -ForegroundColor Green
Write-Host ""

# 检测 Python
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "✗ Python not found" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/"
    exit 1
}

$pythonVersion = & $pythonCmd --version
Write-Host "Python: $pythonVersion" -ForegroundColor Green

# 检测 pip
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "⚠ pip not found, installing..." -ForegroundColor Yellow
    & $pythonCmd -m ensurepip --upgrade
}

Write-Host ""
Write-Host "Installing SkillSync..." -ForegroundColor Yellow

# 安装
pip install --upgrade git+https://github.com/yourusername/skillsync.git

# 验证安装
if (Get-Command skillsync -ErrorAction SilentlyContinue) {
    Write-Host ""
    Write-Host "✓ SkillSync installed successfully!" -ForegroundColor Green
    Write-Host ""

    # 首次配置
    Write-Host "Starting initial setup..." -ForegroundColor Cyan
    skillsync init

    Write-Host ""
    Write-Host "Setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. skillsync start    # 启动后台同步"
    Write-Host "  2. skillsync status   # 查看状态"
    Write-Host ""
    Write-Host "Run 'skillsync --help' for more commands"
} else {
    Write-Host "✗ Installation failed" -ForegroundColor Red
    exit 1
}
