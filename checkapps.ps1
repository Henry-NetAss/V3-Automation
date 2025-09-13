# Anydesk
$anydeskExePath = "C:\Program Files (x86)\AnyDesk\AnyDesk.exe"

if (Test-Path $anydeskExePath) {
    Write-Host "AnyDesk is installed."
} else {
    write-host "Anydesk is not installed"
    Write-Output y|winget install --id anydesk.anydesk
}
# Chrome

$ChromeExePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"

if (Test-Path $ChromeExePath) {
    Write-Host "Chrome is installed."
} else {
    $Chromeexepath1 = "$env:USERPROFILE\AppData\Local\Google\Chrome\Application\chrome.exe"

    if (test-path $chromeexepath1) {
        write-host "Chrome is installed"
    } else { write-host "Chrome is not inistalled"
            write-output y|winget install --id Google.Chrome --Location "C:\Program Files\Google"
        }
    }

# TS Print

$TSPrintExePath = "C:\Program Files (x86)\TerminalWorks\TSPrint\showoptions.exe"

if (Test-Path $TSPrintExePath) {
    Write-Host "TS Print is installed."
} else {
    write-host "TS Print is not installed"
    wite-output y|winget install --id TerminalWorks.TSPrintClient
}

# Adobe

$AdobeExePath = "C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"

if (Test-Path $AdobeExePath) {
    Write-Host "Adobe is installed."

} else { write-host "Adobe is not installed"
Write-Output y|winget install --id Adobe.Acrobat.Reader.32-bit --silent
}


