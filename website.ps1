start microsoft-edge:http://networkassociates.co.za 
$wshell = New-Object -ComObject wscript.shell;
$wshell.AppActivate('Google - Microsoft Edge')
Sleep 2
$wshell.SendKeys('(%(" "))')
Sleep 2
$wshell.SendKeys('(x)')
