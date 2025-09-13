# Get the OS version information
$OSInfo = Get-CimInstance Win32_OperatingSystem

# Extract the OS version string
$OSVersion = $OSInfo.Version

# Extract the OS caption (e.g., "Microsoft Windows 10 Enterprise")
$OSCaption = $OSInfo.Caption

# Check the OS version or caption and conditionally run the script
if ($OSCaption -like "*Windows 10*") {
    Write-Host "Detected Windows 10"
    & Start-Process -FilePath "cscript.exe" -ArgumentList "C:\na\installation\defaultchromewin10.vbs" -NoNewWindow -Wait
} elseif ($OSCaption -like "*Windows 11*") {
    Write-Host "Detected Windows 11"
    & Start-Process -FilePath "cscript.exe" -ArgumentList "C:\na\installation\defaultchromewin11.vbs" -NoNewWindow -Wait
} else {
    Write-Host "Unsupported OS version detected: $OSCaption. Script will not run."
}