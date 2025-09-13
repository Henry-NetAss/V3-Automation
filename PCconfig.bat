powershell -command "& {Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Force}"
powercfg -setdcvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 5ca83367-6e45-459f-a27b-476b1d01c936 2
powercfg -setacvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 5ca83367-6e45-459f-a27b-476b1d01c936 2
powercfg -setdcvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 7648efa3-dd9c-4e3e-b566-50f929386280 2
powercfg -setacvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 7648efa3-dd9c-4e3e-b566-50f929386280 2
powercfg -setdcvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 96996bc0-ad50-47ec-923b-6f41874dd9eb 0
powercfg -setacvalueindex SCHEME_CURRENT 4f971e89-eebd-4455-a8de-9e59040e7347 96996bc0-ad50-47ec-923b-6f41874dd9eb 0
powercfg -change -monitor-timeout-ac 15
powercfg -change -standby-timeout-ac 0
powercfg -change -hibernate-timeout-ac 0
powercfg -change -monitor-timeout-dc 10
powercfg -change -standby-timeout-dc 30
powercfg -change -hibernate-timeout-dc 30
powershell.exe c:\na\v3\winget_enable.ps1
powershell.exe c:\na\v3\VisualFX.ps1
powershell.exe C:\NA\v3\UAC_Disable.ps1
powershell.exe C:\NA\v3\DarkMode.ps1
powershell.exe C:\NA\v3\Disable_Fast_Boot.ps1
powershell.exe C:\NA\v3\RemoveCapabilities.ps1
powershell.exe C:\NA\v3\Removefeatures.ps1
powershell.exe C:\NA\v3\RemovePackages.ps1
powershell.exe C:\NA\v3\UserOnce.ps1
tzutil /s "South Africa Standard Time"
exit
