import tkinter as tk
from tkinter import ttk, messagebox
import threading
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pycaw.constants import CLSID_MMDeviceEnumerator
import keyboard
import json
import os
import pystray
from PIL import Image, ImageDraw
import winsound


class AudioSwitcher:
    def __init__(self):
        self.devices = []
        self.current_device = None
        self.config_file = "audio_config.json"
        self.load_devices()
        self.device_a = None
        self.device_b = None
        self.toggle_hotkey = None
        self.load_config()

    def load_devices(self):
        """Load all audio output devices using simplified approach"""
        from comtypes import CoInitialize, CoUninitialize
        CoInitialize()
        try:
            from pycaw.utils import AudioUtilities, AudioDeviceState

            self.devices = []
            all_devices = AudioUtilities.GetAllDevices()

            for device in all_devices:
                try:
                    device_name = device.FriendlyName
                    device_id = device.id
                    device_state = device.state

                    is_active = device_state == AudioDeviceState.Active
                    is_output = device_name and ('Speaker' in device_name or
                                                 'Headphone' in device_name or
                                                 'Headset' in device_name or
                                                 'HDMI' in device_name or
                                                 'NVIDIA' in device_name or
                                                 'OMEN' in device_name or
                                                 'Monitor' in device_name or
                                                 'Output' in device_name)
                    is_microphone = device_name and 'Microphone' in device_name

                    if is_active and is_output and not is_microphone and device_name and device_id:
                        device_info = {
                            'device': device,
                            'name': device_name,
                            'id': device_id
                        }
                        self.devices.append(device_info)

                except Exception as e:
                    continue

        except Exception as e:
            print(f"Error loading devices: {e}")
        finally:
            CoUninitialize()

    def get_device_names(self):
        """Get list of device names"""
        return [device['name'] for device in self.devices]

    def get_current_device(self):
        """Get the current default audio device"""
        from comtypes import CoInitialize, CoUninitialize
        CoInitialize()
        try:
            from pycaw.pycaw import AudioUtilities
            from pycaw.constants import EDataFlow, ERole

            speakers = AudioUtilities.GetSpeakers()
            interface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            # Get device friendly name
            for device_info in self.devices:
                if speakers.GetId() == device_info['id']:
                    return device_info['name']
            return "Unknown"
        except:
            return "Unknown"
        finally:
            CoUninitialize()

    def switch_to_device(self, device_name):
        """Switch audio output to specified device"""
        try:
            from comtypes import CoInitialize, CoUninitialize
            CoInitialize()
            try:
                for device_info in self.devices:
                    if device_info['name'] == device_name:
                        from policy_config import PolicyConfigClient
                        client = PolicyConfigClient()
                        client.set_default_endpoint(device_info['id'], 0)
                        self.current_device = device_name
                        return True
                return False
            finally:
                CoUninitialize()
        except Exception as e:
            print(f"Error switching device: {e}")
            return False

    def load_config(self):
        """Load saved configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.device_a = config.get('device_a')
                    self.device_b = config.get('device_b')
                    self.toggle_hotkey = config.get('toggle_hotkey')
            except:
                pass

    def save_config(self):
        """Save configuration"""
        config = {
            'device_a': self.device_a,
            'device_b': self.device_b,
            'toggle_hotkey': self.toggle_hotkey
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)


class AudioSwitcherGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Audio Output Switcher")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        self.switcher = AudioSwitcher()
        self.recording_hotkey = False
        self.hotkey_registered = False
        self.tray_icon = None

        # Handle window close - minimize to tray instead of exit
        self.root.protocol("WM_DELETE_WINDOW", self.hide_to_tray)

        self.setup_ui()
        self.update_current_device()
        self.register_saved_hotkey()
        self.setup_tray_icon()

    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Audio Output Switcher",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Current device frame
        current_frame = tk.LabelFrame(self.root, text="Current Output Device", padx=10, pady=10)
        current_frame.pack(fill="x", padx=20, pady=10)

        self.current_device_label = tk.Label(
            current_frame,
            text="Loading...",
            font=("Arial", 12, "bold"),
            fg="blue"
        )
        self.current_device_label.pack()

        # Device selection frame
        device_frame = tk.LabelFrame(self.root, text="Select Two Devices to Toggle", padx=10, pady=10)
        device_frame.pack(fill="x", padx=20, pady=10)

        # Device A
        tk.Label(device_frame, text="Device A:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.device_a_combo = ttk.Combobox(device_frame, values=self.switcher.get_device_names(), state="readonly", width=35)
        self.device_a_combo.grid(row=0, column=1, padx=5, pady=5)
        if self.switcher.device_a:
            self.device_a_combo.set(self.switcher.device_a)

        # Device B
        tk.Label(device_frame, text="Device B:", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.device_b_combo = ttk.Combobox(device_frame, values=self.switcher.get_device_names(), state="readonly", width=35)
        self.device_b_combo.grid(row=1, column=1, padx=5, pady=5)
        if self.switcher.device_b:
            self.device_b_combo.set(self.switcher.device_b)

        # Save devices button
        save_devices_btn = tk.Button(
            device_frame,
            text="Save Device Selection",
            command=self.save_devices,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        save_devices_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Hotkey configuration frame
        hotkey_frame = tk.LabelFrame(self.root, text="Toggle Hotkey", padx=10, pady=10)
        hotkey_frame.pack(fill="x", padx=20, pady=10)

        # Current hotkey display
        tk.Label(hotkey_frame, text="Current Hotkey:", font=("Arial", 10)).pack(anchor="w", padx=5, pady=5)

        self.hotkey_display_label = tk.Label(
            hotkey_frame,
            text=self.switcher.toggle_hotkey if self.switcher.toggle_hotkey else "No hotkey set",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            relief="sunken",
            height=2
        )
        self.hotkey_display_label.pack(fill="x", padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(hotkey_frame)
        button_frame.pack(fill="x", pady=5)

        self.record_btn = tk.Button(
            button_frame,
            text="Record New Hotkey",
            command=self.start_recording_hotkey,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            width=20
        )
        self.record_btn.pack(side="left", padx=5)

        # Manual toggle button
        toggle_frame = tk.Frame(self.root)
        toggle_frame.pack(fill="x", padx=20, pady=10)

        self.toggle_btn = tk.Button(
            toggle_frame,
            text="Toggle Devices Now",
            command=self.toggle_devices,
            bg="#FF9800",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            height=2
        )
        self.toggle_btn.pack(fill="x")

        # Refresh button
        refresh_btn = tk.Button(
            self.root,
            text="Refresh",
            command=self.refresh_all,
            cursor="hand2"
        )
        refresh_btn.pack(pady=5)

    def update_current_device(self):
        """Update current device display"""
        current = self.switcher.get_current_device()
        self.current_device_label.config(text=current)

    def save_devices(self):
        """Save selected devices"""
        device_a = self.device_a_combo.get()
        device_b = self.device_b_combo.get()

        if not device_a or not device_b:
            messagebox.showwarning("Incomplete Selection", "Please select both Device A and Device B")
            return

        if device_a == device_b:
            messagebox.showwarning("Same Device", "Device A and Device B must be different")
            return

        self.switcher.device_a = device_a
        self.switcher.device_b = device_b
        self.switcher.save_config()
        messagebox.showinfo("Success", f"Devices saved!\nA: {device_a}\nB: {device_b}")

    def toggle_devices(self):
        """Toggle between device A and B"""
        if not self.switcher.device_a or not self.switcher.device_b:
            messagebox.showwarning("Not Configured", "Please select and save Device A and Device B first")
            return

        current = self.switcher.get_current_device()

        # Toggle logic
        if current == self.switcher.device_a:
            target = self.switcher.device_b
        elif current == self.switcher.device_b:
            target = self.switcher.device_a
        else:
            # If current is neither A nor B, switch to A
            target = self.switcher.device_a

        if self.switcher.switch_to_device(target):
            self.update_current_device()
            print(f"Switched to: {target}")
            # Play a subtle beep sound
            try:
                winsound.MessageBeep(winsound.MB_OK)  # System default sound
            except:
                pass
        else:
            messagebox.showerror("Error", f"Failed to switch to {target}")

    def start_recording_hotkey(self):
        """Start recording hotkey from keyboard input"""
        self.recording_hotkey = True
        self.record_btn.config(
            text="Press keys now...",
            bg="#FF5722",
            state="disabled"
        )
        self.hotkey_display_label.config(text="Waiting for input...", fg="red")

        # Start keyboard listener in a thread
        threading.Thread(target=self._record_keys, daemon=True).start()

    def _record_keys(self):
        """Record keyboard keys pressed"""
        import time

        pressed_keys = set()
        last_key = None
        start_time = time.time()

        def on_key_event(event):
            nonlocal last_key
            if event.event_type == 'down':
                pressed_keys.add(event.name)
                last_key = event.name

        # Hook keyboard events
        keyboard.hook(on_key_event)

        # Wait for key combination (max 5 seconds)
        while self.recording_hotkey and time.time() - start_time < 5:
            time.sleep(0.1)
            if pressed_keys and time.time() - start_time > 0.5:
                break

        keyboard.unhook_all()

        if not self.recording_hotkey:
            return

        # Build hotkey string
        if pressed_keys:
            modifiers = []
            regular_keys = []

            for key in pressed_keys:
                if key in ['ctrl', 'shift', 'alt', 'windows']:
                    modifiers.append(key)
                else:
                    regular_keys.append(key)

            if regular_keys and last_key in regular_keys:
                hotkey_parts = sorted(modifiers) + [last_key]
            elif modifiers:
                hotkey_parts = sorted(modifiers)
            else:
                hotkey_parts = [last_key] if last_key else list(pressed_keys)

            hotkey_str = '+'.join(hotkey_parts)
            self.root.after(0, self._finish_recording, hotkey_str)
        else:
            self.root.after(0, self._cancel_recording)

    def _finish_recording(self, hotkey_str):
        """Finish recording and apply hotkey"""
        self.recording_hotkey = False

        # Unregister old hotkey
        if self.hotkey_registered and self.switcher.toggle_hotkey:
            try:
                keyboard.remove_hotkey(self.switcher.toggle_hotkey)
            except:
                pass

        # Register new hotkey
        try:
            keyboard.add_hotkey(hotkey_str, lambda: self.root.after(0, self.toggle_devices))
            self.switcher.toggle_hotkey = hotkey_str
            self.switcher.save_config()
            self.hotkey_registered = True

            self.hotkey_display_label.config(text=hotkey_str, fg="green")
            self.record_btn.config(text="Record New Hotkey", bg="#2196F3", state="normal")
            messagebox.showinfo("Success", f"Hotkey '{hotkey_str}' registered!\nPress it anytime to toggle devices.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register hotkey: {str(e)}")
            self._cancel_recording()

    def _cancel_recording(self):
        """Cancel recording"""
        self.recording_hotkey = False
        self.record_btn.config(text="Record New Hotkey", bg="#2196F3", state="normal")
        if self.switcher.toggle_hotkey:
            self.hotkey_display_label.config(text=self.switcher.toggle_hotkey, fg="black")
        else:
            self.hotkey_display_label.config(text="No hotkey set", fg="black")

    def register_saved_hotkey(self):
        """Register hotkey from config file"""
        if self.switcher.toggle_hotkey:
            try:
                keyboard.add_hotkey(
                    self.switcher.toggle_hotkey,
                    lambda: self.root.after(0, self.toggle_devices)
                )
                self.hotkey_registered = True
            except Exception as e:
                print(f"Failed to register saved hotkey: {e}")

    def refresh_all(self):
        """Refresh everything"""
        self.switcher.load_devices()
        self.device_a_combo.config(values=self.switcher.get_device_names())
        self.device_b_combo.config(values=self.switcher.get_device_names())
        self.update_current_device()
        messagebox.showinfo("Refreshed", f"Found {len(self.switcher.devices)} devices")

    def create_tray_icon_image(self):
        """Load icon for the system tray"""
        try:
            # Try to load from icon.ico file
            import sys
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
            else:
                # Running as script
                icon_path = 'icon.ico'

            if os.path.exists(icon_path):
                return Image.open(icon_path)
        except:
            pass

        # Fallback: create simple icon
        width = 64
        height = 64
        image = Image.new('RGBA', (width, height), (52, 152, 219, 255))
        dc = ImageDraw.Draw(image)

        # Simple "A⇄B" text representation
        dc.ellipse([4, 4, 60, 60], fill=(52, 152, 219, 255))
        dc.text((15, 20), "A⇄B", fill=(255, 255, 255, 255))

        return image

    def setup_tray_icon(self):
        """Setup system tray icon"""
        def show_window(icon, item):
            self.root.after(0, self.show_from_tray)

        def quit_app(icon, item):
            icon.stop()
            self.root.after(0, self.root.quit)

        def toggle_from_tray(icon, item):
            self.root.after(0, self.toggle_devices)

        menu = pystray.Menu(
            pystray.MenuItem("Show", show_window, default=True),
            pystray.MenuItem("Toggle Devices", toggle_from_tray),
            pystray.MenuItem("Quit", quit_app)
        )

        icon_image = self.create_tray_icon_image()
        self.tray_icon = pystray.Icon("AudioSwitcher", icon_image, "Audio Switcher", menu)

        # Start tray icon in background thread
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def hide_to_tray(self):
        """Hide window to system tray"""
        self.root.withdraw()

    def show_from_tray(self):
        """Show window from system tray"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def run(self):
        """Start the application"""
        self.root.mainloop()
        if self.tray_icon:
            self.tray_icon.stop()


if __name__ == "__main__":
    try:
        app = AudioSwitcherGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
