@echo off
echo ========================================
echo Building Audio Switcher Executable
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building executable with PyInstaller...
pyinstaller --noconfirm --onefile --windowed ^
  --name "AudioSwitcher" ^
  --icon=NONE ^
  --add-data "audio_config.json;." ^
  --hidden-import "pycaw.pycaw" ^
  --hidden-import "pycaw.utils" ^
  --hidden-import "pycaw.constants" ^
  --hidden-import "pycaw.api.policyconfigclient" ^
  --hidden-import "comtypes" ^
  --hidden-import "keyboard" ^
  audio_switcher.py

echo.
echo ========================================
echo Build complete!
echo Executable located at: dist\AudioSwitcher.exe
echo ========================================
echo.
pause
