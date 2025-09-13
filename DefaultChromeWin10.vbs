Set WshShell = WScript.CreateObject("WScript.Shell")
WshShell.Run "%windir%\system32\control.exe /name Microsoft.DefaultPrograms /page pageDefaultProgram\pageAdvancedSettings?pszAppName=google%20chrome"
WScript.Sleep 15000
WshShell.SendKeys "{TAB}" 
WScript.Sleep 1500
WshShell.SendKeys "{TAB}"
WScript.Sleep 1500
WshShell.SendKeys "{TAB}"
WScript.Sleep 1500
WshShell.SendKeys "{TAB}"
WScript.Sleep 1500
WshShell.SendKeys "{TAB}"
WScript.Sleep 1500
WshShell.SendKeys " " 
WScript.Sleep 1500
WshShell.SendKeys "{TAB}"
WScript.Sleep 1500
WshShell.SendKeys "{TAB}"
.WScript.Sleep 1500
WshShell.SendKeys "{TAB}" 
WScript.Sleep 1500
WScript.Sleep 1500
WshShell.SendKeys "%{F4}" 
WScript.Quit