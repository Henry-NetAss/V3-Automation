set-location -path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
remove-itemproperty -path . -name "ScriptRunnerAppRestart"|write-output y
exit