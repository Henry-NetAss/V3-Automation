
$path = "C:\Na\Installation"
If(!(test-path -PathType container $path))
{
      New-Item -ItemType Directory -Path $path
}
echo y | powershell install-module -name POSHNOTIFY -Scope CurrentUser -Force
$workdir = "c:\na\installation\"
set-location C:\NA\Installation
Clear-Host
send-osnotification -body 'AnyDesk' -Title 'Network Associates'
echo y|winget install --name AnyDesk
$NewPassword = 'Supp0rt@NA123'
Invoke-Command -ScriptBlock {
    Param($NewPassword)
    $Expression = 'echo {0} | "C:\Program Files (x86)\AnyDesk\AnyDesk.exe" --set-password' -f $NewPassword
    Start-Process cmd.exe -ArgumentList "/c $Expression"
} -ArgumentList $NewPassword
send-osnotification -body 'Downloading TeamViewer' -Title 'Network Associates'
echo y|winget install --id TeamViewer.TeamViewer
send-osnotification -body 'Downloading JDK8' -Title 'Network Associates'
echo y|winget install --id EclipseAdoptium.Temurin.8.JDK
start-sleep -seconds 15
Clear-Host
send-osnotification -body 'Downloading JDK11' -Title 'Network Associates'
echo y|winget install --id EclipseAdoptium.Temurin.11.JDK
start-sleep -seconds 15
Clear-Host
send-osnotification -body 'Downloading Google Chrome' -Title 'Network Associates'
mkdir "c:\program files\Google"
echo y|winget install --id Google.Chrome --Location "C:\Program Files\Google"
start-sleep -seconds 5
Clear-Host
send-osnotification -body 'Downloading TS Print' -Title 'Network Associates'
echo y|winget install --id TerminalWorks.TSPrintClient
start-sleep -seconds 5
Clear-Host
send-osnotification -body 'Downloading NetTime' -Title 'Network Associates'
echo y|winget install --name NetTime
Clear-Host
send-osnotification -body 'Downloading Adobe' -Title 'Network Associates'
echo y|winget install --id Adobe.Acrobat.Reader.32-bit
send-osnotification -body 'Windows Scan' -Title 'Network Associates'
echo y|winget install --id 9WZDNCRFJ3PV
send-osnotification -body 'Whatsapp' -Title 'Network Associates'
#Install whatsapp
echo y|winget install --id 9NKSQGP7F2NH
echo y|winget uninstall --id Microsoft.Onedrive
start-sleep -seconds 10
echo y|winget install --id Microsoft.Onedrive

