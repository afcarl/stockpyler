import ctypes

dll = ctypes.cdll.LoadLibrary("C:/Program Files/Norgate Data Updater/bin/norgate.data.interop.x64.dll")
print(dll)
dll.