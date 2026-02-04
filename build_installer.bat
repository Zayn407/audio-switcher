@echo off
echo ========================================
echo Audio Switcher 完整安装程序构建工具
echo ========================================
echo.

echo [步骤 1/3] 安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

echo.
echo [步骤 2/3] 构建可执行文件...
pyinstaller --noconfirm --onefile --windowed ^
  --name "AudioSwitcher" ^
  --icon=NONE ^
  --hidden-import "pycaw.pycaw" ^
  --hidden-import "pycaw.utils" ^
  --hidden-import "pycaw.constants" ^
  --hidden-import "pycaw.api.policyconfigclient" ^
  --hidden-import "comtypes" ^
  --hidden-import "keyboard" ^
  audio_switcher.py

if %errorlevel% neq 0 (
    echo 错误: 可执行文件构建失败
    pause
    exit /b 1
)

echo.
echo [步骤 3/3] 构建安装程序...
echo.
echo 请确保已安装 Inno Setup:
echo 下载地址: https://jrsoftware.org/isdl.php
echo.
echo 安装 Inno Setup 后:
echo 1. 右键点击 installer.iss
echo 2. 选择 "Compile" (编译)
echo 3. 安装程序将生成在 installer_output 文件夹
echo.
echo 或者运行以下命令 (如果 Inno Setup 在 PATH 中):
echo "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
echo.

if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo 检测到 Inno Setup，正在构建安装程序...
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
    if %errorlevel% equ 0 (
        echo.
        echo ========================================
        echo 构建完成！
        echo 可执行文件: dist\AudioSwitcher.exe
        echo 安装程序: installer_output\AudioSwitcher_Setup.exe
        echo ========================================
    ) else (
        echo 安装程序构建失败
    )
) else (
    echo.
    echo Inno Setup 未安装或未在默认路径
    echo 可执行文件已创建: dist\AudioSwitcher.exe
    echo 请手动编译 installer.iss 创建安装程序
)

echo.
pause
