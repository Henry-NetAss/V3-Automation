Set WshShell = WScript.CreateObject("WScript.Shell")

' Open the default settings window
WshShell.Run "%windir%\system32\control.exe /name Microsoft.DefaultPrograms /page pageDefaultProgram\pageAdvancedSettings?pszAppName=google%20chrome"
WScript.Sleep 5000 ' Wait until open (adjust if necessary)

' Adjust number of tabs until you reach the browser choice setting
WshShell.SendKeys "{TAB}" 
WshShell.SendKeys "{TAB}"
WshShell.SendKeys "{TAB}"
WshShell.SendKeys "{TAB}"
WshShell.SendKeys "{TAB}"
WshShell.SendKeys "{TAB}"
WshShell.SendKeys "{TAB}"
WshShell.SendKeys "{TAB}"
WshShell.SendKeys "{TAB}"
WshShell.SendKeys " "
WScript.Sleep 1000
WshShell.SendKeys "{TAB}"
WshShell.SendKeys "{DOWN}"
WshShell.SendKeys " "
WshShell.SendKeys "{TAB}"
WScript.Sleep 1000
WshShell.SendKeys " "
WScript.Sleep 1000
WshShell.SendKeys "{TAB}"
WshShell.SendKeys "{TAB}"
WshShell.SendKeys "{TAB}"
WshShell.SendKeys " "
WshShell.SendKeys " "

WScript.Sleep 500 ' Wait until open
' Uncomment the line below to outomatically close the settings window
WshShell.SendKeys "%{F4}" 
WScript.Quit