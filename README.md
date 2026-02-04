# Audio Output Switcher

A simple Windows application to switch audio output devices using hotkeys.

## Features

- 🔊 Switch between audio output devices (speakers, headphones, etc.)
- 🎤 **Record hotkeys by pressing keys** - No need to type them!
- ⌨️ Configure custom hotkeys for each device
- 🖥️ Simple GUI interface
- 🌐 Runs in the background with global hotkey support
- 💾 Saves your hotkey configurations automatically
- 📦 Easy installer with setup.exe

## Requirements

- Windows 10/11
- Python 3.7 or higher
- Administrator privileges (for global hotkey registration)

## Installation

### Option 1: Using Pre-built Executable (Easiest)

1. Download `AudioSwitcher.exe` from the [Releases](../../releases) page
2. Right-click `AudioSwitcher.exe` → Properties → Check "Run as administrator"
3. Double-click to run!

### Option 2: From Source (For Developers)

#### Step 1: Install Python
If you don't have Python installed:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Complete the installation

#### Step 2: Install Dependencies
Open Command Prompt or PowerShell **as Administrator** and navigate to the project folder:

```bash
cd audio_switcher
pip install -r requirements.txt
```

#### Step 3: (Optional) Build Your Own Executable
```bash
build_exe.bat
```
The executable will be created in the `dist` folder.

## Usage

### Running the Application

**Important:** Run as Administrator to enable global hotkeys

1. Right-click on Command Prompt or PowerShell
2. Select "Run as Administrator"
3. Navigate to the project folder:
   ```bash
   cd C:\Users\Zayn\audio_switcher
   ```
4. Run the application:
   ```bash
   python audio_switcher.py
   ```

### Using the Application

1. **View Available Devices**: The application will show all available audio output devices
2. **Manual Switch**:
   - Select a device from the list
   - Click "Switch to Selected Device"
3. **Set Hotkeys** (New Recording Feature!):
   - Select a device from the list
   - Click "🎤 Record Hotkey" button
   - Press your desired key combination (e.g., hold `Ctrl+Shift+1`)
   - The keys will be automatically detected and displayed
   - Click "✓ Apply to Selected Device"
   - The hotkey is now registered and will work even when the window is minimized!

### Hotkey Examples

- `ctrl+shift+1` - Switch to first device
- `ctrl+shift+2` - Switch to second device
- `alt+s` - Switch to speakers
- `alt+h` - Switch to headphones
- `ctrl+alt+a` - Switch to any device

### Configuration

Hotkey configurations are automatically saved to `audio_config.json` and will be restored when you restart the application.

### Auto-Start on Boot

To make AudioSwitcher start automatically when Windows boots:

1. Double-click `setup_autostart.bat`
2. The program will start automatically on every boot and run in the background (system tray)

To remove auto-start:
1. Double-click `remove_autostart.bat`

## Creating a Shortcut (Optional)

To make it easier to run the application:

1. Create a batch file `run_audio_switcher.bat` with this content:
   ```batch
   @echo off
   cd C:\Users\Zayn\audio_switcher
   python audio_switcher.py
   pause
   ```
2. Right-click the batch file → Create Shortcut
3. Right-click the shortcut → Properties → Advanced → Check "Run as administrator"
4. Pin the shortcut to your taskbar or start menu

## Troubleshooting

### "Access Denied" or hotkeys not working
- Make sure you're running the application as Administrator
- Global hotkeys require elevated privileges on Windows

### Devices not appearing
- Click "Refresh Devices" button
- Make sure your audio devices are connected and enabled in Windows Sound Settings

### Cannot switch to device
- Some devices may require additional Windows permissions
- Try disconnecting and reconnecting the device
- Check Windows Sound Settings to ensure the device is enabled

### Hotkey conflicts
- If a hotkey doesn't work, it may conflict with another application
- Try a different key combination
- Close other applications that might be using the same hotkey

## How It Works

The application uses:
- **pycaw** - Python library for Windows Core Audio API control
- **keyboard** - For global hotkey registration
- **tkinter** - For the GUI interface

## License

Free to use and modify for personal use.
