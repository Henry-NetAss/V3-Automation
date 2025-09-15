# Change default font and size in Word
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$normalTemplate = $word.NormalTemplate
$normalTemplate.OpenAsDocument()
$selection = $word.Selection
$selection.Style.Font.Name = "Aptos"
$selection.Style.Font.Size = 11
$normalTemplate.Save()
$word.Quit()

# Change default font and size in Excel
$excel = New-Object -ComObject Excel.Application
$excel.StandardFont = "Aptos"
$excel.StandardFontSize = 11
$excel.Quit()

# Change default font and size in Outlook (Mail Compose)
$regPath = "HKCU:\Software\Microsoft\Office\16.0\Common\MailSettings"
New-Item -Path $regPath -Force | Out-Null
Set-ItemProperty -Path $regPath -Name "ComposeFontComplex" -Value "Aptos"
Set-ItemProperty -Path $regPath -Name "ComposeFontSimple" -Value "Aptos"
Set-ItemProperty -Path $regPath -Name "ComposeFontSize" -Value 11

exit
