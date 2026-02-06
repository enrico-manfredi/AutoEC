from pyvium import Core

Core.IV_open()
print(Core.IV_VersionDll())
print(Core.IV_getdevicestatus())
Core.IV_close()