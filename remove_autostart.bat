@echo off
echo ========================================
echo Audio Switcher - 移除开机启动
echo ========================================
echo.

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\AudioSwitcher.lnk"

if exist "%SHORTCUT_PATH%" (
    echo 正在删除启动快捷方式...
    del "%SHORTCUT_PATH%"

    if %errorlevel% equ 0 (
        echo.
        echo ========================================
        echo 成功！AudioSwitcher 开机启动已移除
        echo ========================================
    ) else (
        echo.
        echo 删除失败
    )
) else (
    echo.
    echo AudioSwitcher 未设置为开机启动
)

echo.
pause
