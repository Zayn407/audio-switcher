from comtypes import CoInitialize, CoUninitialize
CoInitialize()

from pycaw.utils import AudioUtilities, AudioDeviceState
from policy_config import PolicyConfigClient

# Get devices
all_devices = AudioUtilities.GetAllDevices()
output_devices = []

for device in all_devices:
    try:
        device_name = device.FriendlyName
        device_state = device.state

        is_active = device_state == AudioDeviceState.Active
        is_output = device_name and ('Speaker' in device_name or 'NVIDIA' in device_name or 'OMEN' in device_name or 'Output' in device_name)
        is_microphone = device_name and 'Microphone' in device_name

        if is_active and is_output and not is_microphone:
            output_devices.append((device_name, device.id))
            print(f'Device: {device_name}')
    except:
        pass

print(f'\nFound {len(output_devices)} devices\n')

# Test switching
if len(output_devices) >= 2:
    print(f'Switching to: {output_devices[1][0]}')
    try:
        client = PolicyConfigClient()
        result = client.set_default_endpoint(output_devices[1][1], 0)
        if result:
            print('SUCCESS!')
        else:
            print('FAILED!')
    except Exception as e:
        print(f'ERROR: {e}')
        import traceback
        traceback.print_exc()
else:
    print('Not enough devices to test switching')

CoUninitialize()
