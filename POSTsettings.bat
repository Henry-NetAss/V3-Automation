cd c:\na\v3
powershell -command "& {Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Force}"
powershell.exe C:\NA\Installation\remove_printers.ps1
powershell.exe c:\na\Installation\Desktop_Shortcuts.ps1
powershell.exe c:\na\installation\taskbaricons.ps1
powershell.exe c:\na\Installation\DisableSearchBoxSuggestion.ps1
powershell.exe C:\NA\Installation\Region_Settings.ps1
powershell.exe C:\NA\Installation\updates.ps1
exit

