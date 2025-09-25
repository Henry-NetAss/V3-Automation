Set-location "C:\na\V3"
Invoke-WebRequest -Uri "https://downloads.dell.com/serviceability/catalog/SupportAssistBusinessInstaller.exe" -OutFile "C:\NA\V3\DELLSA.exe"
start-sleep -seconds 15
./dellsa.exe /quiet