"""
PolicyConfig implementation for setting default audio device
Based on Windows IPolicyConfig COM interface
"""

from comtypes import GUID, COMMETHOD
from comtypes.automation import VARIANT
from comtypes.client import GetModule
from ctypes import POINTER
from ctypes.wintypes import DWORD
import comtypes


class IPolicyConfig(comtypes.IUnknown):
    """IPolicyConfig COM interface for Windows 10/11"""
    _iid_ = GUID('{f8679f50-850a-41cf-9c72-430f290290c8}')
    _methods_ = [
        # Windows 10/11 methods
        COMMETHOD([], comtypes.HRESULT, 'GetMixFormat'),
        COMMETHOD([], comtypes.HRESULT, 'GetDeviceFormat'),
        COMMETHOD([], comtypes.HRESULT, 'ResetDeviceFormat'),
        COMMETHOD([], comtypes.HRESULT, 'SetDeviceFormat'),
        COMMETHOD([], comtypes.HRESULT, 'GetProcessingPeriod'),
        COMMETHOD([], comtypes.HRESULT, 'SetProcessingPeriod'),
        COMMETHOD([], comtypes.HRESULT, 'GetShareMode'),
        COMMETHOD([], comtypes.HRESULT, 'SetShareMode'),
        COMMETHOD([], comtypes.HRESULT, 'GetPropertyValue'),
        COMMETHOD([], comtypes.HRESULT, 'SetPropertyValue'),
        COMMETHOD([], comtypes.HRESULT, 'SetDefaultEndpoint',
                  (['in'], POINTER(comtypes.c_wchar), 'wszDeviceId'),
                  (['in'], DWORD, 'eRole')),
        COMMETHOD([], comtypes.HRESULT, 'SetEndpointVisibility'),
    ]


class PolicyConfigClient:
    """Client for setting default audio endpoint"""

    def __init__(self):
        # Try multiple CLSIDs for different Windows versions
        self._clsids = [
            GUID('{870af99c-171d-4f9e-af0d-e63df40c2bc9}'),  # Windows 10/11
            GUID('{294935CE-F637-4E7C-A41B-AB255460B862}'),  # Windows 7/8
        ]
        self._policy_config = None

        for clsid in self._clsids:
            try:
                self._policy_config = comtypes.CoCreateInstance(
                    clsid,
                    IPolicyConfig,
                    comtypes.CLSCTX_ALL
                )
                break
            except:
                continue

        if self._policy_config is None:
            raise Exception("Failed to create PolicyConfig instance")

    def set_default_endpoint(self, device_id, role=0):
        """
        Set the default audio endpoint
        role: 0 = eConsole (default), 1 = eMultimedia, 2 = eCommunications
        """
        try:
            # role 0 = eConsole (default device for most applications)
            self._policy_config.SetDefaultEndpoint(device_id, role)
            return True
        except Exception as e:
            print(f"Error setting default endpoint: {e}")
            return False
