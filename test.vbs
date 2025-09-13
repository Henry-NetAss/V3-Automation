Set WshShell = WScript.CreateObject("WScript.Shell")

' Open the default settings window
WshShell.Run "%windir%\system32\control.exe /name Microsoft.DefaultPrograms /page pageDefaultProgram\pageAdvancedSettings?pszAppName=google%20chrome"
WScript.Sleep 5000 ' Wait until open (adjust if necessary)

' Adjust number of tabs until you reach the browser choice setting
WshShell.SendKeys "{TAB}"
WScript.Sleep 500 
WshShell.SendKeys "{TAB}"
WScript.Sleep 500 
WshShell.SendKeys "{TAB}"
WScript.Sleep 500 
WshShell.SendKeys "{TAB}"
WScript.Sleep 500 
WshShell.SendKeys "{TAB}"
WScript.Sleep 500 
WshShell.SendKeys "{TAB}"
WScript.Sleep 500 
WshShell.SendKeys "{TAB}"
WScript.Sleep 500 
WshShell.SendKeys "{TAB}"
WScript.Sleep 500 
WshShell.SendKeys "{TAB}"
WScript.Sleep 500 
WshShell.SendKeys " "
WScript.Sleep 1000
WshShell.SendKeys "{TAB}"
WScript.Sleep 500 
WshShell.SendKeys "{DOWN}"
WScript.Sleep 1000
WshShell.SendKeys " "
WshShell.SendKeys "{TAB}"