import tkinter as tk
from tkinter import ttk, messagebox
import threading
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pycaw.constants import CLSID_MMDeviceEnumerator
from pycaw.utils import AudioDevice
import keyboard
import json
import os


class AudioSwitcher:
    def __init__(self):
        self.devices = []
        self.current_device = None
        self.config_file = "audio_config.json"
        self.load_devices()
        self.hotkeys = {}
        self.load_config()

    def load_devices(self):
        """Load all audio output devices"""
        from comtypes import CoInitialize, CoUninitialize
        CoInitialize()
        try:
            from pycaw.pycaw import AudioUtilities
            devices = AudioUtilities.GetAllDevices()
            self.devices = [d for d in devices if d.state == 1]  # Only active devices
        finally:
            CoUninitialize()

    def get_device_names(self):
        """Get list of device names"""
        return [device.FriendlyName for device in self.devices]

    def switch_to_device(self, device_name):
        """Switch audio output to specified device"""
        try:
            from comtypes import CoInitialize, CoUninitialize
            CoInitialize()
            try:
                for device in self.devices:
                    if device.FriendlyName == device_name:
                        # Set as default device
                        import subprocess
                        # Using nircmd for device switching (more reliable)
                        device_id = device.id

                        # Alternative method using PolicyConfig
                        from pycaw.api.policyconfigclient import PolicyConfigClient
                        client = PolicyConfigClient()
                        client.set_default_endpoint(device.id)

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
                    self.hotkeys = config.get('hotkeys', {})
            except:
                pass

    def save_config(self):
        """Save configuration"""
        config = {'hotkeys': self.hotkeys}
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)


class AudioSwitcherGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Audio Output Switcher")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        self.switcher = AudioSwitcher()
        self.registered_hotkeys = []
        self.recording_hotkey = False
        self.recorded_keys = []

        self.setup_ui()

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
            text="Not set",
            font=("Arial", 10),
            fg="blue"
        )
        self.current_device_label.pack()

        # Device selection frame
        device_frame = tk.LabelFrame(self.root, text="Available Devices", padx=10, pady=10)
        device_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Device list
        self.device_listbox = tk.Listbox(device_frame, height=6)
        self.device_listbox.pack(fill="both", expand=True, pady=5)

        for device_name in self.switcher.get_device_names():
            self.device_listbox.insert(tk.END, device_name)

        # Switch button
        switch_btn = tk.Button(
            device_frame,
            text="Switch to Selected Device",
            command=self.switch_device,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        switch_btn.pack(pady=5)

        # Hotkey configuration frame
        hotkey_frame = tk.LabelFrame(self.root, text="Hotkey Configuration", padx=10, pady=10)
        hotkey_frame.pack(fill="x", padx=20, pady=10)

        # Hotkey setup
        hotkey_setup_frame = tk.Frame(hotkey_frame)
        hotkey_setup_frame.pack(fill="x", pady=5)

        tk.Label(hotkey_setup_frame, text="Hotkey:").grid(row=0, column=0, padx=5, sticky="w")

        self.hotkey_display_label = tk.Label(
            hotkey_setup_frame,
            text="No hotkey recorded",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            relief="sunken",
            width=25,
            anchor="w",
            padx=5,
            pady=5
        )
        self.hotkey_display_label.grid(row=0, column=1, padx=5)

        # Button frame
        button_frame = tk.Frame(hotkey_frame)
        button_frame.pack(fill="x", pady=5)

        self.record_btn = tk.Button(
            button_frame,
            text="🎤 Record Hotkey",
            command=self.start_recording_hotkey,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            width=20
        )
        self.record_btn.pack(side="left", padx=5)

        self.apply_hotkey_btn = tk.Button(
            button_frame,
            text="✓ Apply to Selected Device",
            command=self.set_hotkey,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            width=20,
            state="disabled"
        )
        self.apply_hotkey_btn.pack(side="left", padx=5)

        # Info label
        info_label = tk.Label(
            hotkey_frame,
            text="Click 'Record Hotkey', then press your desired key combination",
            font=("Arial", 8),
            fg="gray"
        )
        info_label.pack()

        # Registered hotkeys display
        self.hotkey_text = tk.Text(hotkey_frame, height=3, state='disabled')
        self.hotkey_text.pack(fill="x", pady=5)

        self.update_hotkey_display()

        # Refresh button
        refresh_btn = tk.Button(
            self.root,
            text="Refresh Devices",
            command=self.refresh_devices,
            cursor="hand2"
        )
        refresh_btn.pack(pady=5)

    def switch_device(self):
        """Switch to selected device"""
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device first")
            return

        device_name = self.device_listbox.get(selection[0])

        if self.switcher.switch_to_device(device_name):
            self.current_device_label.config(text=device_name)
            messagebox.showinfo("Success", f"Switched to: {device_name}")
        else:
            messagebox.showerror("Error", "Failed to switch device")

    def start_recording_hotkey(self):
        """Start recording hotkey from keyboard input"""
        self.recording_hotkey = True
        self.recorded_keys = []
        self.record_btn.config(
            text="⏺ Press keys now...",
            bg="#FF5722",
            state="disabled"
        )
        self.hotkey_display_label.config(
            text="Waiting for input...",
            fg="red"
        )

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
            # If we have at least one key and no new keys for 0.5 seconds, finish
            if pressed_keys and time.time() - start_time > 0.5:
                break

        keyboard.unhook_all()

        if not self.recording_hotkey:
            return

        # Build hotkey string
        if pressed_keys:
            # Separate modifiers and regular keys
            modifiers = []
            regular_keys = []

            for key in pressed_keys:
                if key in ['ctrl', 'shift', 'alt', 'windows']:
                    modifiers.append(key)
                else:
                    regular_keys.append(key)

            # Build hotkey string: modifiers + last regular key
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
        """Finish recording and display the hotkey"""
        self.recording_hotkey = False
        self.hotkey_display_label.config(
            text=hotkey_str,
            fg="green"
        )
        self.record_btn.config(
            text="🎤 Record Hotkey",
            bg="#2196F3",
            state="normal"
        )
        self.apply_hotkey_btn.config(state="normal")
        self.recorded_hotkey = hotkey_str

    def _cancel_recording(self):
        """Cancel recording"""
        self.recording_hotkey = False
        self.record_btn.config(
            text="🎤 Record Hotkey",
            bg="#2196F3",
            state="normal"
        )
        self.hotkey_display_label.config(
            text="Recording cancelled",
            fg="orange"
        )

    def set_hotkey(self):
        """Set hotkey for selected device"""
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device first")
            return

        device_name = self.device_listbox.get(selection[0])

        if not hasattr(self, 'recorded_hotkey') or not self.recorded_hotkey:
            messagebox.showwarning("No Hotkey", "Please record a hotkey first")
            return

        hotkey = self.recorded_hotkey

        try:
            # Unregister old hotkey if exists
            for hk, dev in list(self.switcher.hotkeys.items()):
                if dev == device_name and hk in self.registered_hotkeys:
                    keyboard.remove_hotkey(hk)
                    self.registered_hotkeys.remove(hk)

            # Register new hotkey
            keyboard.add_hotkey(
                hotkey,
                lambda dn=device_name: self.hotkey_switch(dn)
            )
            self.registered_hotkeys.append(hotkey)

            self.switcher.hotkeys[hotkey] = device_name
            self.switcher.save_config()

            self.update_hotkey_display()
            messagebox.showinfo("Success", f"Hotkey '{hotkey}' assigned to {device_name}")

            # Reset for next recording
            self.recorded_hotkey = None
            self.hotkey_display_label.config(text="No hotkey recorded", fg="black")
            self.apply_hotkey_btn.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to set hotkey: {str(e)}")

    def hotkey_switch(self, device_name):
        """Switch device via hotkey"""
        if self.switcher.switch_to_device(device_name):
            self.root.after(0, lambda: self.current_device_label.config(text=device_name))

    def update_hotkey_display(self):
        """Update hotkey display"""
        self.hotkey_text.config(state='normal')
        self.hotkey_text.delete(1.0, tk.END)

        if self.switcher.hotkeys:
            for hotkey, device in self.switcher.hotkeys.items():
                self.hotkey_text.insert(tk.END, f"{hotkey} → {device}\n")
        else:
            self.hotkey_text.insert(tk.END, "No hotkeys configured")

        self.hotkey_text.config(state='disabled')

    def refresh_devices(self):
        """Refresh device list"""
        self.switcher.load_devices()
        self.device_listbox.delete(0, tk.END)

        for device_name in self.switcher.get_device_names():
            self.device_listbox.insert(tk.END, device_name)

        messagebox.showinfo("Refreshed", "Device list updated")

    def register_saved_hotkeys(self):
        """Register hotkeys from config file"""
        for hotkey, device in self.switcher.hotkeys.items():
            try:
                keyboard.add_hotkey(
                    hotkey,
                    lambda dn=device: self.hotkey_switch(dn)
                )
                self.registered_hotkeys.append(hotkey)
            except Exception as e:
                print(f"Failed to register hotkey {hotkey}: {e}")

    def run(self):
        """Start the application"""
        self.register_saved_hotkeys()
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = AudioSwitcherGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")
