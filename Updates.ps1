Function InstallWindowsModules
{
    
    Install-PackageProvider -Name NuGet -Force

    Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted
    
    Install-Module PSWindowsUpdate

    Set-Content C:\AutoUpdates\Progress.txt -Value 1
}

Function InstallWindowsUpdates
{
    Get-WindowsUpdate | Out-File C:\AutoUpdates\History\Updates_"$((Get-Date).ToString('dd-MM-yyyy_HH.mm.ss'))".txt

    Install-WindowsUpdate -Install -AcceptAll -AutoReboot
}


$ChkPath = "C:\AutoUpdates"
$PathExists = Test-Path $ChkPath
If ($PathExists -eq $false)
{
    mkdir C:\AutoUpdates
    mkdir C:\AutoUpdates\History
}
else
{
}


$ChkFile = "C:\AutoUpdates\Progress.txt"
$FileExists = Test-Path $ChkFile
If ($FileExists -eq $false)
{
    New-Item C:\AutoUpdates\Progress.txt
    Set-Content C:\AutoUpdates\Progress.txt -Value 0
}
else
{
}


$Status = Get-Content C:\AutoUpdates\Progress.txt -First 1

If ($Status -eq 0) 
{
  
    InstallWindowsModules
    InstallWindowsUpdates
}
elseif ($Status -eq 1)
{

    InstallWindowsUpdates
}
