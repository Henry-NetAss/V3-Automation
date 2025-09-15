# Anydesk
$esetExePath = "C:\Program Files\ESET\ESET Security\ecmds.exe"

if (Test-Path $esetExePath) {
    set-location C:\na\v3
    ./PROTECTAgentInstaller.bat
} else {
    write-host "ESET is not installed"
}
exit



