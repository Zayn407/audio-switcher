@echo off
echo ========================================
echo Audio Switcher - 设置开机启动
echo ========================================
echo.

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "EXE_PATH=%~dp0dist\AudioSwitcher.exe"

if not exist "%EXE_PATH%" (
    echo 错误: 找不到 AudioSwitcher.exe
    echo 请先运行 build_exe.bat 构建程序
    pause
    exit /b 1
)

echo 正在创建启动快捷方式...
echo.
echo 目标文件: %EXE_PATH%
echo 启动文件夹: %STARTUP_FOLDER%
echo.

powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP_FOLDER%\AudioSwitcher.lnk'); $Shortcut.TargetPath = '%EXE_PATH%'; $Shortcut.WorkingDirectory = '%~dp0dist'; $Shortcut.Save()"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 成功！AudioSwitcher 已设置为开机启动
    echo 快捷方式位置: %STARTUP_FOLDER%\AudioSwitcher.lnk
    echo ========================================
) else (
    echo.
    echo 设置失败，请以管理员身份运行此脚本
)

echo.
pause
