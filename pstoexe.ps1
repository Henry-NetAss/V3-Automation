$path = "C:\Na\2024"
If(!(test-path -PathType container $path))
{
      New-Item -ItemType Directory -Path $path
}
set-location c:\NA\2024
invoke-webrequest -Uri 'https://github.com/Henry-NetAss/Automation/archive/refs/heads/main.zip' -outfile 'C:\na\2024\setup.zip'
expand-archive -path C:\na\2024\setup.zip -destinationpath C:\NA\Installation
get-childitem 'C:\na\installation\Automation-main'|move-item -destination 'C:\na\Installation'
Remove-Item -LiteralPath "C:\NA\Installation\Automation-main" -Force -Recurse
Remove-Item -LiteralPath "C:\NA\2024" -Force -Recurse
set-location C:\NA\Installation
.\setup.bat
exit